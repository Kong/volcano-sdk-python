"""Realtime broadcast facade."""

from __future__ import annotations

import asyncio
import importlib
import inspect
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Literal, Protocol, TypeAlias, cast
from urllib.parse import quote, urlsplit, urlunsplit

from .database import Database
from .errors import VolcanoError
from .models import JSONValue, Session, _freeze_json

if TYPE_CHECKING:
    from ._transport import Transport

MessageCallback = Callable[[Any], Any]
RealtimeCallback = Callable[[Any], Any]
UnsubscribeCallback = Callable[[], None]
ChannelType: TypeAlias = Literal["broadcast", "presence", "postgres"]
PostgresEvent: TypeAlias = Literal["INSERT", "UPDATE", "DELETE"]
PostgresListenerEvent: TypeAlias = Literal["INSERT", "UPDATE", "DELETE", "*"]
PostgresChangeCallback = Callable[["PostgresChange"], Any]
SUPPORTED_CHANNEL_TYPES = frozenset({"broadcast", "presence", "postgres"})
POSTGRES_EVENTS = frozenset({"INSERT", "UPDATE", "DELETE"})
POSTGRES_CHANNEL_SEGMENTS = 3
POSTGRES_PUBLICATION_SEGMENTS = 5
CENTRIFUGE_ERROR = cast(
    "type[Exception]",
    importlib.import_module("centrifuge").CentrifugeError,
)
CALLBACK_QUEUE_LIMIT = 128
POSTGRES_QUEUE_LIMIT = 128
NO_PENDING_CALLBACK = object()
CALLBACK_QUEUE_FULL_MESSAGE = (
    "Volcano realtime callback queue is full; publication dropped"
)
CHANNEL_NOT_SUBSCRIBED = "Channel must be subscribed before sending"
CHANNEL_REMOVAL_IN_PROGRESS = "realtime channel removal is in progress"
CHANNEL_NOT_MANAGED = "realtime channel is no longer managed"
PRESENCE_ONLY = "operation is only available for presence channels"
BROADCAST_ONLY = "send is only available for broadcast channels"
POSTGRES_ONLY = "operation is only available for postgres channels"
CALLBACK_NOT_CALLABLE = "callback must be callable"
SUBSCRIPTION_REGISTRY_UNAVAILABLE = (
    "centrifuge client subscription registry is unavailable"
)
AUTOFETCH_ERRORS = (
    VolcanoError,
    RuntimeError,
    LookupError,
    TypeError,
    ValueError,
)


def _empty_presence_data() -> Mapping[str, JSONValue]:
    return MappingProxyType({})


def _validate_channel_type(channel_type: str) -> ChannelType:
    if channel_type not in SUPPORTED_CHANNEL_TYPES:
        message = f"unsupported realtime channel type: {channel_type}"
        raise ValueError(message)
    return cast("ChannelType", channel_type)


def _postgres_route_matches(candidate: str, publication: str) -> bool:
    candidate_parts = candidate.split(":")
    publication_parts = publication.split(":")
    return (
        len(candidate_parts) == POSTGRES_CHANNEL_SEGMENTS
        and candidate_parts[0] == "postgres"
        and len(publication_parts) == POSTGRES_PUBLICATION_SEGMENTS
        and publication_parts[1:4] == candidate_parts
    )


@dataclass(frozen=True, slots=True)
class RealtimeConnectContext:
    """Details reported after a realtime transport connects."""

    client: str | None = None


@dataclass(frozen=True, slots=True)
class RealtimeDisconnectContext:
    """Details reported after a realtime transport disconnects."""

    code: int | None = None
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class RealtimeErrorContext:
    """Details reported when the realtime transport emits an error."""

    code: int | None = None
    message: str | None = None
    error: Exception | None = None


@dataclass(frozen=True, slots=True)
class RealtimePresenceInfo:
    """Immutable identity and metadata for one present realtime client."""

    client: str
    user: str | None = None
    data: Mapping[str, JSONValue] = field(
        default_factory=_empty_presence_data,
        hash=False,
    )

    def __post_init__(self) -> None:
        """Defensively freeze nested connection metadata."""
        frozen = _freeze_json(cast("JSONValue", dict(self.data)))
        object.__setattr__(self, "data", cast("Mapping[str, JSONValue]", frozen))


@dataclass(frozen=True, slots=True)
class PostgresChange:
    """Immutable RLS-scoped Postgres row-change notification."""

    type: PostgresEvent
    schema: str
    table: str
    record: Mapping[str, JSONValue] | None = field(default=None, hash=False)
    old_record: Mapping[str, JSONValue] | None = field(default=None, hash=False)
    columns: tuple[str, ...] | None = None
    timestamp: str = ""
    id: JSONValue = field(default=None, hash=False)
    mode: Literal["lightweight"] | None = None

    def __post_init__(self) -> None:
        """Defensively freeze nested row and identifier values."""
        if self.record is not None:
            frozen_record = _freeze_json(cast("JSONValue", dict(self.record)))
            object.__setattr__(self, "record", frozen_record)
        if self.old_record is not None:
            frozen_old_record = _freeze_json(cast("JSONValue", dict(self.old_record)))
            object.__setattr__(self, "old_record", frozen_old_record)
        object.__setattr__(self, "id", _freeze_json(self.id))


@dataclass(frozen=True, slots=True)
class _PostgresDelivery:
    change: PostgresChange
    database_name: str | None
    access_token: str | None
    session_generation: int
    user_id: str | None
    subscription_epoch: int


@dataclass(frozen=True, slots=True)
class _CallbackDelivery:
    event: str
    data: Any
    postgres_request: _PostgresDelivery | None = None


@dataclass(slots=True)
class _SessionBoundDatabaseContext:
    _transport: Transport
    access_token: str

    def _session_token(self) -> str:
        return self.access_token


def _postgres_change(data: Any) -> PostgresChange | None:
    if not isinstance(data, Mapping):
        return None
    typed_data = cast("Mapping[str, object]", data)
    event = typed_data.get("type")
    schema = typed_data.get("schema")
    table = typed_data.get("table")
    timestamp = typed_data.get("timestamp")
    mode = typed_data.get("mode")
    record = typed_data.get("record")
    old_record = typed_data.get("old_record")
    raw_columns = typed_data.get("columns")
    if (
        event not in POSTGRES_EVENTS
        or not isinstance(schema, str)
        or not isinstance(table, str)
        or not isinstance(timestamp, str)
        or (record is not None and not isinstance(record, Mapping))
        or (old_record is not None and not isinstance(old_record, Mapping))
    ):
        return None
    typed_mode: Literal["lightweight"] | None
    if mode is None:
        typed_mode = None
    elif mode == "lightweight":
        typed_mode = "lightweight"
    else:
        return None
    if raw_columns is None:
        columns = None
    elif isinstance(raw_columns, (list, tuple)):
        untyped_columns = cast("list[object] | tuple[object, ...]", raw_columns)
        if not all(isinstance(column, str) for column in untyped_columns):
            return None
        columns = tuple(cast("list[str] | tuple[str, ...]", raw_columns))
    else:
        return None
    return PostgresChange(
        type=cast("PostgresEvent", event),
        schema=schema,
        table=table,
        record=cast("Mapping[str, JSONValue] | None", record),
        old_record=cast("Mapping[str, JSONValue] | None", old_record),
        columns=columns,
        timestamp=timestamp,
        id=cast("JSONValue", typed_data.get("id")),
        mode=typed_mode,
    )


class RealtimeContext(Protocol):
    """Client capabilities required by realtime connections."""

    _transport: Transport

    def _anon_token(self) -> str: ...

    def _session_token(self) -> str: ...

    def _capture_session(self) -> tuple[int, Session | None]: ...


class CentrifugeSubscription(Protocol):
    """Centrifuge subscription operations used by the SDK."""

    async def subscribe(self) -> None:
        """Subscribe to the remote channel."""
        ...

    async def publish(self, data: Any) -> Any:
        """Publish a payload to the remote channel."""
        ...

    async def unsubscribe(self) -> None:
        """Unsubscribe from the remote channel."""
        ...

    async def presence(self) -> Any:
        """Return the clients currently present on the channel."""
        ...


class CentrifugeConnection(Protocol):
    """Centrifuge connection operations used by the SDK."""

    state: Any

    async def connect(self) -> None:
        """Open the remote connection."""
        ...

    async def disconnect(self) -> None:
        """Close the remote connection."""
        ...

    def new_subscription(
        self,
        name: str,
        *,
        events: Any,
        join_leave: bool = False,
        recoverable: bool = False,
    ) -> CentrifugeSubscription:
        """Create a subscription for a remote channel."""
        ...

    def remove_subscription(self, subscription: Any) -> None:
        """Remove an unsubscribed channel from the connection registry."""
        ...


class CentrifugeFactory(Protocol):
    """Construct a typed Centrifuge connection."""

    def __call__(
        self,
        address: str,
        *,
        events: Any,
        token: str,
        get_token: Callable[[], Awaitable[str]],
    ) -> CentrifugeConnection:
        """Construct a Centrifuge connection."""
        ...


class CentrifugeConstructor(Protocol):
    """Describe the dynamically imported Centrifuge client constructor."""

    def __call__(
        self,
        address: str,
        *,
        events: Any,
        token: str,
        get_token: Callable[[], Awaitable[str]],
    ) -> object:
        """Construct the dynamically imported Centrifuge client."""
        ...


class Publication(Protocol):
    """Publication payload received from Centrifuge."""

    data: Any


class PublicationContext(Protocol):
    """Centrifuge callback context containing a publication."""

    pub: Publication


def _centrifuge_client(
    address: str,
    *,
    events: Any,
    token: str,
    get_token: Callable[[], Awaitable[str]],
) -> CentrifugeConnection:
    module = importlib.import_module("centrifuge")
    constructor = cast("CentrifugeConstructor", module.Client)
    return cast(
        "CentrifugeConnection",
        constructor(address, events=events, token=token, get_token=get_token),
    )


class _ProjectAwareSubscriptions(dict[str, Any]):
    def get(self, key: str, default: Any = None) -> Any:
        subscription = super().get(key)
        if subscription is not None:
            return subscription
        matches = [
            (channel, candidate)
            for channel, candidate in self.items()
            if key.endswith(f":{channel}") or _postgres_route_matches(channel, key)
        ]
        return max(matches, key=lambda match: len(match[0]))[1] if matches else default


class _VolcanoCentrifugeConnection:
    def __init__(self, connection: CentrifugeConnection) -> None:
        self._connection = connection
        state = vars(connection)
        subscriptions = state.get("_subs")
        if not isinstance(subscriptions, dict):
            raise TypeError(SUBSCRIPTION_REGISTRY_UNAVAILABLE)
        typed_subscriptions = cast("dict[str, Any]", subscriptions)
        state["_subs"] = _ProjectAwareSubscriptions(typed_subscriptions)

    async def connect(self) -> None:
        await self._connection.connect()

    async def disconnect(self) -> None:
        await self._connection.disconnect()

    @property
    def is_connected(self) -> bool:
        state = self._connection.state
        return getattr(state, "value", None) == "connected"

    def new_subscription(
        self,
        name: str,
        *,
        events: Any,
        join_leave: bool = False,
        recoverable: bool = False,
    ) -> CentrifugeSubscription:
        return self._connection.new_subscription(
            name,
            events=events,
            join_leave=join_leave,
            recoverable=recoverable,
        )

    def remove_subscription(self, subscription: CentrifugeSubscription) -> None:
        self._connection.remove_subscription(subscription)


class _ChannelEvents:
    def __init__(self, channel: Channel) -> None:
        self._channel = channel

    async def on_publication(self, ctx: PublicationContext) -> None:
        if self._channel._type == "postgres":
            await self._channel._receive_postgres_change(ctx.pub.data)
            return
        await self._channel._emit("message", ctx.pub.data)

    async def on_subscribing(self, ctx: Any) -> None:
        del ctx
        self._channel._subscribed = False
        await self._channel._end_postgres_epoch()
        await self._channel._presence_unsubscribed()

    async def on_subscribed(self, ctx: Any) -> None:
        del ctx
        self._channel._subscribed = True
        self._channel._begin_postgres_epoch()
        if self._channel._type == "presence":
            self._channel._schedule_presence_sync()

    async def on_unsubscribed(self, ctx: Any) -> None:
        del ctx
        self._channel._subscribed = False
        await self._channel._end_postgres_epoch()
        await self._channel._presence_unsubscribed()

    async def on_join(self, ctx: Any) -> None:
        await self._channel._presence_join(getattr(ctx, "info", None))

    async def on_leave(self, ctx: Any) -> None:
        await self._channel._presence_leave(getattr(ctx, "info", None))

    async def on_error(self, ctx: Any) -> None:
        del ctx


class _ClientEvents:
    def __init__(self, realtime: Realtime) -> None:
        self._realtime = realtime

    async def on_connecting(self, ctx: Any) -> None:
        del ctx

    async def on_connected(self, ctx: Any) -> None:
        self._realtime._enqueue_connection_callbacks(
            "connect",
            RealtimeConnectContext(client=getattr(ctx, "client", None)),
        )

    async def on_disconnected(self, ctx: Any) -> None:
        self._realtime._enqueue_connection_callbacks(
            "disconnect",
            RealtimeDisconnectContext(
                code=getattr(ctx, "code", None),
                reason=getattr(ctx, "reason", None),
            ),
        )

    async def on_error(self, ctx: Any) -> None:
        error = getattr(ctx, "error", None)
        self._realtime._enqueue_connection_callbacks(
            "error",
            RealtimeErrorContext(
                code=getattr(ctx, "code", None),
                message=str(error) if error is not None else None,
                error=error if isinstance(error, Exception) else None,
            ),
        )

    async def on_subscribed(self, ctx: Any) -> None:
        del ctx

    async def on_subscribing(self, ctx: Any) -> None:
        del ctx

    async def on_unsubscribed(self, ctx: Any) -> None:
        del ctx

    async def on_publication(self, ctx: Any) -> None:
        del ctx

    async def on_join(self, ctx: Any) -> None:
        del ctx

    async def on_leave(self, ctx: Any) -> None:
        del ctx


class Channel:
    """Realtime broadcast, presence, or Postgres channel."""

    def __init__(
        self,
        realtime: Realtime,
        name: str,
        channel_type: ChannelType,
        *,
        auto_fetch: bool,
    ) -> None:
        """Create a channel managed by a realtime facade."""
        self._realtime = realtime
        self._name = name
        self._type = channel_type
        self._auto_fetch = auto_fetch
        self._callbacks: dict[str, list[MessageCallback]] = {}
        self._presence_state: dict[str, RealtimePresenceInfo] = {}
        self._presence_events: list[tuple[str, RealtimePresenceInfo]] = []
        self._presence_syncing = False
        self._tracked_state: Mapping[str, JSONValue] = MappingProxyType({})
        self._subscription: CentrifugeSubscription | None = None
        self._subscribed = False
        self._presence_lock = asyncio.Lock()
        self._presence_sync_task: asyncio.Task[None] | None = None
        self._presence_sync_pending = False
        self._callback_queue: asyncio.Queue[_CallbackDelivery] = asyncio.Queue(
            maxsize=CALLBACK_QUEUE_LIMIT
        )
        self._callback_task: asyncio.Task[None] | None = None
        self._active_callback_task: asyncio.Task[None] | None = None
        self._callback_stop: asyncio.Event | None = None
        self._pending_presence_sync: Any = NO_PENDING_CALLBACK
        self._postgres_filters: dict[
            MessageCallback,
            tuple[PostgresListenerEvent, str, str],
        ] = {}
        self._postgres_queue: asyncio.Queue[_PostgresDelivery | None] = asyncio.Queue(
            maxsize=POSTGRES_QUEUE_LIMIT
        )
        self._postgres_task: asyncio.Task[None] | None = None
        self._postgres_epoch = 0
        self._postgres_session_generation = 0
        self._postgres_access_token: str | None = None
        self._postgres_user_id: str | None = None

    @property
    def name(self) -> str:
        """Return the canonical channel name sent to realtime."""
        return self._name

    def on(self, event: str, callback: MessageCallback) -> Channel:
        """Register a callback for messages or presence events."""
        allowed_events = {
            "broadcast": {"message"},
            "presence": {"message", "join", "leave", "presence_sync"},
            "postgres": {"*"},
        }[self._type]
        if event not in allowed_events:
            message = f"unsupported realtime event: {event}"
            raise ValueError(message)
        self._callbacks.setdefault(event, []).append(callback)
        return self

    def on_postgres_changes(
        self,
        event: PostgresListenerEvent,
        *,
        schema: str,
        table: str,
        callback: PostgresChangeCallback,
    ) -> UnsubscribeCallback:
        """Observe Postgres changes filtered by event, schema, and table."""
        if self._type != "postgres":
            raise ValueError(POSTGRES_ONLY)
        if event not in {*POSTGRES_EVENTS, "*"}:
            message = f"unsupported Postgres change event: {event}"
            raise ValueError(message)

        def filtered(change: PostgresChange) -> Any:
            if change.schema != schema or change.table != table:
                return None
            if event not in ("*", change.type):
                return None
            return callback(change)

        self._callbacks.setdefault("*", []).append(filtered)
        self._postgres_filters[filtered] = (event, schema, table)

        def unsubscribe() -> None:
            callbacks = self._callbacks.get("*", [])
            if filtered in callbacks:
                callbacks.remove(filtered)
            self._postgres_filters.pop(filtered, None)

        return unsubscribe

    def on_presence_sync(self, callback: MessageCallback) -> UnsubscribeCallback:
        """Observe immutable snapshots of a presence channel's current state."""
        self._ensure_presence()
        self._callbacks.setdefault("presence_sync", []).append(callback)

        def unsubscribe() -> None:
            callbacks = self._callbacks.get("presence_sync", [])
            if callback in callbacks:
                callbacks.remove(callback)

        return unsubscribe

    async def track(self, state: Mapping[str, JSONValue] | None = None) -> None:
        """Store local presence state while server identity remains authoritative."""
        self._ensure_presence()
        if not self._subscribed:
            raise RuntimeError(CHANNEL_NOT_SUBSCRIBED)
        frozen = _freeze_json(cast("JSONValue", dict(state or {})))
        self._tracked_state = cast("Mapping[str, JSONValue]", frozen)

    def get_presence_state(self) -> Mapping[str, RealtimePresenceInfo]:
        """Return an immutable snapshot of the clients currently present."""
        self._ensure_presence()
        return MappingProxyType(dict(self._presence_state))

    @property
    def tracked_state(self) -> Mapping[str, JSONValue]:
        """Return an immutable snapshot of this client's local presence state."""
        self._ensure_presence()
        return MappingProxyType(dict(self._tracked_state))

    def _ensure_presence(self) -> None:
        if self._type != "presence":
            raise ValueError(PRESENCE_ONLY)

    async def _receive_postgres_change(self, data: Any) -> None:
        if not self._subscribed:
            return
        change = _postgres_change(data)
        if change is None or not self._has_postgres_listener(change):
            return
        self._refresh_postgres_session_binding()
        database_name = self._realtime._database_name
        fetch = (
            change.mode == "lightweight"
            and change.type != "DELETE"
            and self._auto_fetch
            and database_name is not None
            and self._postgres_access_token is not None
        )
        self._start_postgres_worker()
        await self._postgres_queue.put(
            _PostgresDelivery(
                change=change,
                database_name=database_name if fetch else None,
                access_token=self._postgres_access_token if fetch else None,
                session_generation=self._postgres_session_generation,
                user_id=self._postgres_user_id,
                subscription_epoch=self._postgres_epoch,
            )
        )

    def _has_postgres_listener(self, change: PostgresChange) -> bool:
        callbacks = self._callbacks.get("*", ())
        if any(callback not in self._postgres_filters for callback in callbacks):
            return True
        return any(
            listener_schema == change.schema
            and listener_table == change.table
            and listener_event in ("*", change.type)
            for listener_event, listener_schema, listener_table in (
                self._postgres_filters.values()
            )
        )

    def _refresh_postgres_session_binding(self) -> None:
        generation, session = self._realtime._client_context._capture_session()
        if generation == self._postgres_session_generation:
            return
        if session is None or session.user_id != self._postgres_user_id:
            return
        self._postgres_session_generation = generation
        self._postgres_access_token = session.access_token

    def _start_postgres_worker(self) -> None:
        task = self._postgres_task
        if task is None or task.done():
            self._postgres_task = asyncio.create_task(self._run_postgres_fetches())

    async def _run_postgres_fetches(self) -> None:
        try:
            while True:
                request = await self._postgres_queue.get()
                try:
                    if request is None:
                        return
                    await self._deliver_postgres_change(request)
                finally:
                    self._postgres_queue.task_done()
        finally:
            if asyncio.current_task() is self._postgres_task:
                self._postgres_task = None

    async def _deliver_postgres_change(self, request: _PostgresDelivery) -> None:
        if not self._postgres_request_is_current(request):
            return
        change = request.change
        if change.mode != "lightweight":
            await self._emit("*", change, postgres_request=request)
            return
        if change.type == "DELETE":
            old_record = change.old_record
            if old_record is None and change.id is not None:
                old_record = {"id": change.id}
            await self._emit(
                "*",
                replace(change, old_record=old_record, id=None, mode=None),
                postgres_request=request,
            )
            return
        if request.database_name is None or request.access_token is None:
            await self._emit("*", change, postgres_request=request)
            return
        try:
            row = await asyncio.to_thread(
                self._realtime._fetch_postgres_row,
                change,
                request.database_name,
                request.access_token,
            )
            if row is None:
                identity = f"{change.schema}.{change.table}:{change.id}"
                message = f"Postgres row not found: {identity}"
                raise LookupError(message)
            delivered = replace(request.change, record=row, id=None, mode=None)
        except AUTOFETCH_ERRORS as error:
            if not self._postgres_request_is_current(request):
                return
            asyncio.get_running_loop().call_exception_handler(
                {
                    "message": "Volcano realtime Postgres auto-fetch failed",
                    "exception": error,
                    "channel": self._name,
                }
            )
            delivered = request.change
        if self._postgres_request_is_current(request):
            await self._emit("*", delivered, postgres_request=request)

    def _postgres_request_is_current(self, request: _PostgresDelivery) -> bool:
        return (
            self._subscribed
            and request.subscription_epoch == self._postgres_epoch
            and self._postgres_auth_is_current(request)
        )

    def _postgres_auth_is_current(self, request: _PostgresDelivery) -> bool:
        session_generation, session = self._realtime._client_context._capture_session()
        if request.session_generation == session_generation:
            return True
        return (
            request.user_id is not None
            and session is not None
            and request.user_id == session.user_id
        )

    def _begin_postgres_epoch(self) -> None:
        if self._type == "postgres":
            self._postgres_epoch += 1
            generation, session = self._realtime._client_context._capture_session()
            self._postgres_session_generation = generation
            self._postgres_access_token = session.access_token if session else None
            self._postgres_user_id = session.user_id if session else None

    async def _end_postgres_epoch(self) -> None:
        if self._type != "postgres":
            return
        self._postgres_epoch += 1
        self._postgres_access_token = None
        self._postgres_user_id = None
        while not self._postgres_queue.empty():
            self._postgres_queue.get_nowait()
            self._postgres_queue.task_done()
        task = self._postgres_task
        if task is None or task.done():
            self._postgres_task = None
            return
        await self._postgres_queue.put(None)
        await asyncio.shield(task)
        while not self._postgres_queue.empty():
            self._postgres_queue.get_nowait()
            self._postgres_queue.task_done()

    async def subscribe(self) -> None:
        """Subscribe to this channel."""
        await self._realtime._subscribe(self)

    async def send(self, data: Any) -> None:
        """Publish a broadcast payload to this channel."""
        await self._realtime._publish(self, data)

    async def unsubscribe(self) -> None:
        """Unsubscribe from this channel."""
        await self._realtime._unsubscribe(self)

    async def _emit(
        self,
        event: str,
        data: Any,
        *,
        postgres_request: _PostgresDelivery | None = None,
    ) -> None:
        if not self._callbacks.get(event):
            return
        if event == "presence_sync":
            self._pending_presence_sync = NO_PENDING_CALLBACK
        task = self._callback_task
        if task is None or task.done():
            self._start_callback_dispatcher()
        elif self._callback_stop is not None and self._callback_stop.is_set():
            self._callback_task = asyncio.create_task(
                self._restart_callback_dispatcher(task)
            )
            self._callback_stop = None
        try:
            self._callback_queue.put_nowait(
                _CallbackDelivery(event, data, postgres_request)
            )
        except asyncio.QueueFull:
            if event == "presence_sync":
                self._pending_presence_sync = data
                return
            asyncio.get_running_loop().call_exception_handler(
                {
                    "message": CALLBACK_QUEUE_FULL_MESSAGE,
                    "channel": self._name,
                }
            )

    def _start_callback_dispatcher(self) -> None:
        stop = asyncio.Event()
        self._callback_stop = stop
        self._callback_task = asyncio.create_task(self._dispatch_callbacks(stop))

    async def _restart_callback_dispatcher(self, previous: asyncio.Task[None]) -> None:
        await asyncio.gather(previous, return_exceptions=True)
        stop = asyncio.Event()
        self._callback_stop = stop
        await self._dispatch_callbacks(stop)

    async def _dispatch_callbacks(self, stop: asyncio.Event) -> None:
        while not stop.is_set():
            delivery = await self._callback_queue.get()
            try:
                if not self._callback_delivery_is_current(delivery):
                    continue
                for callback in tuple(self._callbacks.get(delivery.event, [])):
                    if not self._callback_delivery_is_current(delivery):
                        break
                    active_task = asyncio.create_task(
                        self._run_callback(callback, delivery)
                    )
                    self._active_callback_task = active_task
                    try:
                        (error,) = await asyncio.gather(
                            active_task, return_exceptions=True
                        )
                    finally:
                        self._active_callback_task = None
                    if isinstance(error, BaseException):
                        asyncio.get_running_loop().call_exception_handler(
                            {
                                "message": "Volcano realtime callback failed",
                                "exception": error,
                                "channel": self._name,
                            }
                        )
            finally:
                self._callback_queue.task_done()
                self._enqueue_pending_presence_sync()

    def _callback_delivery_is_current(self, delivery: _CallbackDelivery) -> bool:
        request = delivery.postgres_request
        return request is None or self._postgres_request_is_current(request)

    def _enqueue_pending_presence_sync(self) -> None:
        pending = self._pending_presence_sync
        if pending is NO_PENDING_CALLBACK or self._callback_queue.full():
            return
        self._pending_presence_sync = NO_PENDING_CALLBACK
        self._callback_queue.put_nowait(_CallbackDelivery("presence_sync", pending))

    async def _run_callback(
        self,
        callback: MessageCallback,
        delivery: _CallbackDelivery,
    ) -> None:
        if not self._callback_delivery_is_current(delivery):
            return
        result = callback(delivery.data)
        if inspect.isawaitable(result):
            await result

    def _replace_presence(self, clients: Mapping[str, Any]) -> None:
        self._presence_state = {
            client_id: self._presence_info(info) for client_id, info in clients.items()
        }

    async def _begin_presence_sync(self) -> None:
        async with self._presence_lock:
            self._presence_syncing = True
            self._presence_events.clear()

    async def _complete_presence_sync(self, clients: Mapping[str, Any]) -> None:
        async with self._presence_lock:
            if not self._subscribed:
                self._discard_presence_sync()
                return
            self._replace_presence(clients)
            for event, presence in self._presence_events:
                self._apply_presence_event(event, presence)
            self._discard_presence_sync()
            await self._emit("presence_sync", self.get_presence_state())

    async def _abort_presence_sync(self) -> None:
        async with self._presence_lock:
            self._discard_presence_sync()

    async def _fail_presence_sync(self) -> None:
        async with self._presence_lock:
            self._discard_presence_sync()
            if not self._subscribed:
                return
            self._presence_state.clear()
            await self._emit("presence_sync", self.get_presence_state())

    def _discard_presence_sync(self) -> None:
        self._presence_syncing = False
        self._presence_events.clear()

    def _apply_presence_event(
        self,
        event: str,
        presence: RealtimePresenceInfo,
    ) -> None:
        if event == "join":
            self._presence_state[presence.client] = presence
        else:
            self._presence_state.pop(presence.client, None)

    async def _presence_join(self, info: Any) -> None:
        if self._type != "presence" or info is None:
            return
        async with self._presence_lock:
            if not self._subscribed:
                return
            presence = self._presence_info(info)
            if self._presence_syncing:
                self._presence_events.append(("join", presence))
            self._apply_presence_event("join", presence)
            await self._emit("join", presence)
            await self._emit("presence_sync", self.get_presence_state())

    async def _presence_leave(self, info: Any) -> None:
        if self._type != "presence" or info is None:
            return
        async with self._presence_lock:
            if not self._subscribed:
                return
            presence = self._presence_info(info)
            if self._presence_syncing:
                self._presence_events.append(("leave", presence))
            self._apply_presence_event("leave", presence)
            await self._emit("leave", presence)
            await self._emit("presence_sync", self.get_presence_state())

    async def _presence_unsubscribed(self) -> None:
        if self._type != "presence":
            return
        await self._cancel_presence_sync()
        async with self._presence_lock:
            self._discard_presence_sync()
            self._presence_state.clear()
            self._tracked_state = MappingProxyType({})
            await self._emit("presence_sync", self.get_presence_state())

    def _presence_info(self, info: Any) -> RealtimePresenceInfo:
        data = getattr(info, "conn_info", None)
        typed_data = (
            cast("Mapping[str, JSONValue]", data)
            if isinstance(data, Mapping)
            else _empty_presence_data()
        )
        return RealtimePresenceInfo(
            client=str(getattr(info, "client", "")),
            user=getattr(info, "user", None),
            data=typed_data,
        )

    def _schedule_presence_sync(self) -> None:
        task = self._presence_sync_task
        if task is not None and not task.done():
            self._presence_sync_pending = True
            return
        self._presence_sync_pending = False
        self._presence_sync_task = asyncio.create_task(self._run_presence_sync())

    async def _run_presence_sync(self) -> None:
        try:
            while self._subscribed:
                await self._realtime._sync_presence(self)
                if not self._presence_sync_pending:
                    return
                self._presence_sync_pending = False
        finally:
            if asyncio.current_task() is self._presence_sync_task:
                self._presence_sync_task = None

    async def _wait_presence_sync(self) -> None:
        task = self._presence_sync_task
        if task is not None:
            await asyncio.shield(task)

    async def _cancel_presence_sync(self) -> None:
        task = self._presence_sync_task
        self._presence_sync_task = None
        self._presence_sync_pending = False
        if task is None or task.done():
            return
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)

    async def _reset(self) -> None:
        self._subscription = None
        await self._cancel_presence_sync()
        await self._end_postgres_epoch()
        task = self._callback_task
        active_task = self._active_callback_task
        if self._callback_stop is not None:
            self._callback_stop.set()
        current_task = asyncio.current_task()
        called_from_dispatcher = current_task is task or current_task is active_task
        if task is not None and not called_from_dispatcher:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)
            self._callback_task = None
        while not self._callback_queue.empty():
            self._callback_queue.get_nowait()
            self._callback_queue.task_done()
        self._pending_presence_sync = NO_PENDING_CALLBACK
        self._presence_state.clear()
        self._discard_presence_sync()
        self._tracked_state = MappingProxyType({})
        self._subscribed = False


class Realtime:
    """Manage project realtime connections and channels."""

    def __init__(
        self,
        client: RealtimeContext,
        *,
        api_url: str,
        client_factory: CentrifugeFactory = _centrifuge_client,
    ) -> None:
        """Create a lazily connected realtime facade."""
        self._client_context = client
        self._api_url = api_url
        self._client_factory = client_factory
        self._connection: _VolcanoCentrifugeConnection | None = None
        self._connection_lock = asyncio.Lock()
        self._channels: dict[str, Channel] = {}
        self._removing_channels: set[str] = set()
        self._connection_callbacks: dict[str, dict[int, RealtimeCallback]] = {
            "connect": {},
            "disconnect": {},
            "error": {},
        }
        self._next_callback_id = 0
        self._connection_callback_queue: asyncio.Queue[
            tuple[str, Any, tuple[int, ...]]
        ] = asyncio.Queue(maxsize=CALLBACK_QUEUE_LIMIT)
        self._connection_callback_task: asyncio.Task[None] | None = None
        self._database_name: str | None = None

    def set_database_name(self, name: str | None) -> None:
        """Configure the database used for lightweight Postgres auto-fetch."""
        self._database_name = name

    def on_connect(self, callback: RealtimeCallback) -> UnsubscribeCallback:
        """Register a connection callback and return its unsubscribe function."""
        return self._register_connection_callback("connect", callback)

    def on_disconnect(self, callback: RealtimeCallback) -> UnsubscribeCallback:
        """Register a disconnection callback and return its unsubscribe function."""
        return self._register_connection_callback("disconnect", callback)

    def on_error(self, callback: RealtimeCallback) -> UnsubscribeCallback:
        """Register a transport-error callback and return its unsubscribe function."""
        return self._register_connection_callback("error", callback)

    def _register_connection_callback(
        self,
        event: str,
        callback: RealtimeCallback,
    ) -> UnsubscribeCallback:
        if not callable(callback):
            raise TypeError(CALLBACK_NOT_CALLABLE)
        self._next_callback_id += 1
        callback_id = self._next_callback_id
        self._connection_callbacks[event][callback_id] = callback

        def unsubscribe() -> None:
            self._connection_callbacks[event].pop(callback_id, None)

        return unsubscribe

    def _enqueue_connection_callbacks(self, event: str, context: Any) -> None:
        callback_ids = tuple(self._connection_callbacks[event])
        if not callback_ids:
            return
        try:
            self._connection_callback_queue.put_nowait((event, context, callback_ids))
        except asyncio.QueueFull:
            asyncio.get_running_loop().call_exception_handler(
                {"message": "Volcano realtime connection callback queue is full"}
            )
            return
        task = self._connection_callback_task
        if task is None or task.done():
            self._connection_callback_task = asyncio.create_task(
                self._drain_connection_callbacks()
            )

    async def _drain_connection_callbacks(self) -> None:
        while not self._connection_callback_queue.empty():
            event, context, callback_ids = self._connection_callback_queue.get_nowait()
            try:
                callbacks = self._connection_callbacks[event]
                for callback_id in callback_ids:
                    callback = callbacks.get(callback_id)
                    if callback is None:
                        continue
                    (error,) = await asyncio.gather(
                        self._run_connection_callback(callback, context),
                        return_exceptions=True,
                    )
                    if isinstance(error, BaseException):
                        asyncio.get_running_loop().call_exception_handler(
                            {
                                "message": (
                                    "Volcano realtime connection callback failed"
                                ),
                                "exception": error,
                                "event": event,
                            }
                        )
            finally:
                self._connection_callback_queue.task_done()

    async def _run_connection_callback(
        self,
        callback: RealtimeCallback,
        context: Any,
    ) -> None:
        result = callback(context)
        if inspect.isawaitable(result):
            await result

    def channel(
        self,
        name: str,
        *,
        channel_type: ChannelType = "broadcast",
        auto_fetch: bool = True,
    ) -> Channel:
        """Return a stable channel facade for a realtime name and type."""
        channel_type = _validate_channel_type(channel_type)
        wire_name = f"{channel_type}:{name}"
        if wire_name in self._removing_channels:
            raise RuntimeError(CHANNEL_REMOVAL_IN_PROGRESS)
        if wire_name not in self._channels:
            self._channels[wire_name] = Channel(
                self,
                wire_name,
                channel_type,
                auto_fetch=auto_fetch,
            )
        channel = self._channels[wire_name]
        if channel._auto_fetch != auto_fetch:
            message = f"conflicting auto_fetch option for {wire_name}"
            raise ValueError(message)
        return channel

    def _fetch_postgres_row(
        self,
        change: PostgresChange,
        database_name: str,
        access_token: str,
    ) -> dict[str, Any] | None:
        table = (
            change.table
            if change.schema == "public"
            else f"{change.schema}.{change.table}"
        )
        context = _SessionBoundDatabaseContext(
            self._client_context._transport,
            access_token,
        )
        rows = (
            Database(context, database_name)
            .from_(table)
            .select("*")
            .eq("id", change.id)
            .limit(1)
            .execute()
        )
        return rows[0] if rows else None

    @property
    def is_connected(self) -> bool:
        """Return whether the realtime transport is connected."""
        return self._connection is not None and self._connection.is_connected

    async def remove_channel(
        self,
        name: str,
        *,
        channel_type: ChannelType = "broadcast",
    ) -> None:
        """Unsubscribe and forget one broadcast or presence channel."""
        channel_type = _validate_channel_type(channel_type)
        wire_name = f"{channel_type}:{name}"
        async with self._connection_lock:
            channel = self._channels.get(wire_name)
            if channel is None:
                return
            self._removing_channels.add(wire_name)
            try:
                await self._remove_channel(channel)
                self._channels.pop(wire_name, None)
            finally:
                self._removing_channels.remove(wire_name)

    async def remove_all_channels(self) -> None:
        """Unsubscribe and forget every managed channel."""
        async with self._connection_lock:
            first_error: Exception | None = None
            for wire_name, channel in tuple(self._channels.items()):
                self._removing_channels.add(wire_name)
                try:
                    await self._remove_channel(channel)
                except CENTRIFUGE_ERROR as error:
                    first_error = first_error or error
                else:
                    if self._channels.get(wire_name) is channel:
                        del self._channels[wire_name]
                finally:
                    self._removing_channels.remove(wire_name)
            if first_error is not None:
                raise first_error

    async def _remove_channel(self, channel: Channel) -> None:
        subscription = channel._subscription
        if subscription is not None:
            await subscription.unsubscribe()
            if self._connection is not None:
                self._connection.remove_subscription(subscription)
        await channel._reset()

    async def _token(self) -> str:
        return self._client_context._session_token()

    def _address(self) -> str:
        parsed = urlsplit(self._api_url)
        scheme = "wss" if parsed.scheme == "https" else "ws"
        query = f"apikey={quote(self._client_context._anon_token(), safe='')}"
        return urlunsplit((scheme, parsed.netloc, "/realtime/v1/websocket", query, ""))

    async def _connect(self) -> _VolcanoCentrifugeConnection:
        async with self._connection_lock:
            return await self._connect_locked()

    async def _connect_locked(self) -> _VolcanoCentrifugeConnection:
        if self._connection is not None:
            return self._connection
        connection = _VolcanoCentrifugeConnection(
            self._client_factory(
                self._address(),
                events=_ClientEvents(self),
                token=self._client_context._session_token(),
                get_token=self._token,
            )
        )
        await connection.connect()
        self._connection = connection
        return connection

    async def _subscribe(self, channel: Channel) -> None:
        async with self._connection_lock:
            if self._channels.get(channel._name) is not channel:
                raise RuntimeError(CHANNEL_NOT_MANAGED)
            connection = await self._connect_locked()
            if channel._subscription is None:
                channel._subscription = connection.new_subscription(
                    channel._name,
                    events=_ChannelEvents(channel),
                    join_leave=channel._type == "presence",
                    recoverable=channel._type == "presence",
                )
            await channel._subscription.subscribe()
            if channel._type == "presence":
                await channel._wait_presence_sync()

    async def _sync_presence(self, channel: Channel) -> None:
        if channel._subscription is None:
            return
        await channel._begin_presence_sync()
        query_succeeded = False
        try:
            result = await channel._subscription.presence()
            query_succeeded = True
        except CENTRIFUGE_ERROR as error:
            await channel._fail_presence_sync()
            query_succeeded = True
            self._enqueue_connection_callbacks(
                "error",
                RealtimeErrorContext(
                    code=getattr(error, "code", None),
                    message=str(error),
                    error=error,
                ),
            )
            return
        finally:
            if not query_succeeded:
                await channel._abort_presence_sync()
        clients = getattr(result, "clients", None)
        if isinstance(clients, Mapping):
            await channel._complete_presence_sync(cast("Mapping[str, Any]", clients))
        else:
            await channel._abort_presence_sync()

    async def _publish(self, channel: Channel, data: Any) -> None:
        async with self._connection_lock:
            if channel._type != "broadcast":
                raise ValueError(BROADCAST_ONLY)
            subscription = channel._subscription
            if not channel._subscribed or subscription is None:
                raise RuntimeError(CHANNEL_NOT_SUBSCRIBED)
            await subscription.publish(data)

    async def _unsubscribe(self, channel: Channel) -> None:
        async with self._connection_lock:
            if channel._subscription is not None:
                await channel._subscription.unsubscribe()

    async def disconnect(self) -> None:
        """Disconnect and reset every channel managed by this facade."""
        async with self._connection_lock:
            connection = self._connection
            self._connection = None
            try:
                if connection is not None:
                    await connection.disconnect()
            finally:
                for channel in tuple(self._channels.values()):
                    await channel._reset()
