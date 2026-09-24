"""Realtime broadcast facade."""

from __future__ import annotations

import asyncio
import inspect
from collections.abc import Callable, Iterator, Mapping
from dataclasses import dataclass, field, replace
from itertools import count
from types import MappingProxyType
from typing import (
    TYPE_CHECKING,
    Literal,
    TypeAlias,
    TypeVar,
)
from urllib.parse import quote, urlencode, urlsplit, urlunsplit

from centrifuge import CentrifugeError, ClientEventHandler
from typing_extensions import override

from ._database_response import database_rows
from ._json_values import freeze_json
import volcano_sdk._realtime_transport as _native

from ._realtime_callbacks import (
    CallbackBatch,
    ConnectionDelivery,
    DynamicCallback,
    Invocation,
    register_callback,
)
from ._realtime_fetch_worker import (
    PostgresFetchJob,
    PostgresFetchOutcome,
    PostgresFetchRequest,
    PostgresFetchWorker,
)
from ._transport import (
    AsyncDatabaseSelectTransport,
    invoke_async,
    response_payload,
)
from .models import JSONValue

if TYPE_CHECKING:
    from typing import TypeGuard

    from ._session_operations import SessionOperations
    from .models import Session

CentrifugeConnection: TypeAlias = _native.CentrifugeConnection
CentrifugeFactory: TypeAlias = _native.CentrifugeFactory
CentrifugeSubscription: TypeAlias = _native.CentrifugeSubscription
Publication: TypeAlias = _native.Publication
PublicationContext: TypeAlias = _native.PublicationContext
RealtimeContext: TypeAlias = _native.RealtimeContext

_PostgresFetchRequest: TypeAlias = PostgresFetchRequest
_MessageT = TypeVar("_MessageT")

MessageCallback: TypeAlias = Callable[[_MessageT], object]
RealtimeCallback: TypeAlias = Callable[[_MessageT], object]
UnsubscribeCallback = Callable[[], None]
ChannelType: TypeAlias = Literal["broadcast", "presence", "postgres"]
PostgresEvent: TypeAlias = Literal["INSERT", "UPDATE", "DELETE"]
PostgresListenerEvent: TypeAlias = Literal["INSERT", "UPDATE", "DELETE", "*"]
PostgresChangeCallback = Callable[["PostgresChange"], object]
POSTGRES_EVENTS = frozenset({"INSERT", "UPDATE", "DELETE"})
POSTGRES_CHANNEL_SEGMENTS = 3
POSTGRES_PUBLICATION_SEGMENTS = 5
CENTRIFUGE_ERROR: type[Exception] = CentrifugeError
CALLBACK_QUEUE_LIMIT = 128
POSTGRES_QUEUE_LIMIT = 128
POSTGRES_BATCH_WINDOW_MS = 20
POSTGRES_MAX_BATCH_SIZE = 50
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
NO_ACTIVE_SESSION = "No active session"
CONNECTION_SESSION_UNAVAILABLE = "Realtime connection has no session binding"
CONNECTION_SESSION_CHANGED = "Realtime connection session changed"
POSTGRES_FETCH_FAILED_MESSAGE = "Volcano realtime Postgres row fetch failed"
_POSTGRES_QUERY_UNAVAILABLE = "Transport does not support realtime Postgres row fetch"
_INVALID_POSTGRES_ROW_VALUE = "Realtime Postgres row contains a non-JSON value"


def _empty_presence_data() -> Mapping[str, JSONValue]:
    return MappingProxyType({})


def _freeze_mapping(value: Mapping[str, JSONValue]) -> Mapping[str, JSONValue]:
    return MappingProxyType({key: freeze_json(item) for key, item in value.items()})


def _validate_channel_type(channel_type: str) -> ChannelType:
    if channel_type == "broadcast":
        return "broadcast"
    if channel_type == "presence":
        return "presence"
    if channel_type == "postgres":
        return "postgres"
    message = f"unsupported realtime channel type: {channel_type}"
    raise ValueError(message)


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
        object.__setattr__(self, "data", _freeze_mapping(self.data))


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
            object.__setattr__(self, "record", _freeze_mapping(self.record))
        if self.old_record is not None:
            object.__setattr__(self, "old_record", _freeze_mapping(self.old_record))
        object.__setattr__(self, "id", freeze_json(self.id))


def _normalize_postgres_delete(change: PostgresChange) -> PostgresChange:
    if change.mode != "lightweight" or change.type != "DELETE":
        return change
    old_record = change.old_record
    if old_record is None and change.id is not None:
        old_record = {"id": change.id}
    return replace(change, old_record=old_record, id=None, mode=None)


def _filter_postgres_changes(
    event: PostgresListenerEvent,
    schema: str,
    table: str,
    callback: PostgresChangeCallback,
) -> PostgresChangeCallback:
    def filtered(change: PostgresChange) -> object:
        if change.schema != schema or change.table != table:
            return None
        if event not in {"*", change.type}:
            return None
        return callback(change)

    return filtered


@dataclass(frozen=True, slots=True)
class _PostgresFetchConfig:
    enabled: bool
    batch_window_ms: int
    max_batch_size: int

    @property
    def batch_window_seconds(self) -> float:
        return self.batch_window_ms / 1_000


def _postgres_fetch_config(
    *,
    auto_fetch: bool,
    fetch_batch_window_ms: object,
    fetch_max_batch_size: object,
) -> _PostgresFetchConfig:
    if type(fetch_batch_window_ms) is not int or fetch_batch_window_ms <= 0:
        message = "fetch_batch_window_ms must be a positive integer"
        raise ValueError(message)
    if (
        type(fetch_max_batch_size) is not int
        or not 1 <= fetch_max_batch_size <= POSTGRES_QUEUE_LIMIT
    ):
        message = (
            f"fetch_max_batch_size must be an integer between 1 and "
            f"{POSTGRES_QUEUE_LIMIT}"
        )
        raise ValueError(message)
    return _PostgresFetchConfig(
        enabled=auto_fetch,
        batch_window_ms=fetch_batch_window_ms,
        max_batch_size=fetch_max_batch_size,
    )


@dataclass(frozen=True, slots=True)
class _PostgresDeliveryIdentity:
    session_lineage: SessionOperations | None
    subscription_epoch: object


@dataclass(frozen=True, slots=True)
class _PostgresDelivery:
    change: PostgresChange
    identity: _PostgresDeliveryIdentity


@dataclass(frozen=True, slots=True)
class _CallbackDelivery:
    event: str
    data: object
    postgres_identity: _PostgresDeliveryIdentity | None = None
    delivery_epoch: object | None = None


def _is_postgres_event(value: object) -> TypeGuard[PostgresEvent]:
    return isinstance(value, str) and value in POSTGRES_EVENTS


def _is_object_sequence(value: object) -> TypeGuard[list[object] | tuple[object, ...]]:
    return isinstance(value, (list, tuple))


def _postgres_change(data: object) -> PostgresChange | None:
    if not _native.is_object_mapping(data):
        return None
    event = data.get("type")
    schema = data.get("schema")
    table = data.get("table")
    timestamp = data.get("timestamp")
    mode = data.get("mode")
    record = data.get("record")
    old_record = data.get("old_record")
    raw_columns = data.get("columns")
    identifier = data.get("id")
    if not _is_json_record_or_none(record) or not _is_json_record_or_none(old_record):
        return None
    if (
        not _is_postgres_event(event)
        or not isinstance(schema, str)
        or not isinstance(table, str)
        or not isinstance(timestamp, str)
        or not _is_json_value(identifier)
        or not _postgres_mode(mode)
    ):
        return None
    valid_columns, columns = _postgres_columns(raw_columns)
    if not valid_columns:
        return None
    return PostgresChange(
        type=event,
        schema=schema,
        table=table,
        record=record,
        old_record=old_record,
        columns=columns,
        timestamp=timestamp,
        id=identifier,
        mode=mode,
    )


def _is_json_record_or_none(value: object) -> TypeGuard[Mapping[str, JSONValue] | None]:
    return value is None or _is_json_record(value)


def _postgres_mode(value: object) -> TypeGuard[Literal["lightweight"] | None]:
    return value is None or value == "lightweight"


def _postgres_columns(value: object) -> tuple[bool, tuple[str, ...] | None]:
    if value is None:
        return True, None
    if not _is_object_sequence(value):
        return False, None
    columns: list[str] = []
    for column in value:
        if not isinstance(column, str):
            return False, None
        columns.append(column)
    return True, tuple(columns)


def _is_json_value(value: object) -> TypeGuard[JSONValue]:
    if value is None or isinstance(value, (str, int, float, bool)):
        return True
    if _is_object_sequence(value):
        return all(_is_json_value(item) for item in value)
    if _native.is_object_mapping(value):
        return all(
            isinstance(key, str) and _is_json_value(item) for key, item in value.items()
        )
    return False


def _is_json_record(value: object) -> TypeGuard[Mapping[str, JSONValue]]:
    return _native.is_object_mapping(value) and all(
        isinstance(key, str) and _is_json_value(item) for key, item in value.items()
    )


def _checked_postgres_row(row: dict[str, object]) -> Mapping[str, JSONValue]:
    if not _is_json_record(row):
        raise TypeError(_INVALID_POSTGRES_ROW_VALUE)
    return row


class _ChannelEvents:
    def __init__(self, channel: Channel) -> None:
        self._channel: Channel = channel

    def _is_current(self) -> bool:
        return self._channel._subscription_events is self

    async def on_publication(self, ctx: PublicationContext) -> None:
        if (
            not self._is_current()
            or self._channel._paused
            or not self._channel._subscribed
        ):
            return
        if self._channel._type == "postgres":
            await self._channel._receive_postgres_change(ctx.pub.data)
            return
        await self._channel._emit("message", ctx.pub.data)

    async def on_subscribing(self, ctx: object) -> None:
        del ctx
        if self._is_current():
            await self._channel._transport_lost()

    async def on_subscribed(self, ctx: object) -> None:
        del ctx
        if not self._is_current() or self._channel._paused:
            return
        self._channel._subscribed = True
        await self._channel._begin_postgres_epoch()
        if self._channel._type == "presence":
            self._channel._schedule_presence_sync()

    async def on_unsubscribed(self, ctx: object) -> None:
        del ctx
        if self._is_current():
            await self._channel._transport_lost()

    async def on_join(self, ctx: object) -> None:
        if self._is_current():
            await self._channel._presence_join(
                _native.native_attribute(ctx, "info")
            )

    async def on_leave(self, ctx: object) -> None:
        if self._is_current():
            await self._channel._presence_leave(
                _native.native_attribute(ctx, "info")
            )

    async def on_error(self, ctx: object) -> None:
        del ctx


class _ClientEvents(ClientEventHandler):
    def __init__(self, realtime: Realtime) -> None:
        self._realtime: Realtime = realtime

    @override
    async def on_connected(self, ctx: object) -> None:
        client = _native.native_attribute(ctx, "client")
        self._realtime._enqueue_connection_callbacks(
            RealtimeConnectContext(client=client if isinstance(client, str) else None),
        )

    @override
    async def on_disconnected(self, ctx: object) -> None:
        code = _native.native_attribute(ctx, "code")
        reason = _native.native_attribute(ctx, "reason")
        self._realtime._enqueue_connection_callbacks(
            RealtimeDisconnectContext(
                code=code if isinstance(code, int) else None,
                reason=reason if isinstance(reason, str) else None,
            ),
        )

    @override
    async def on_error(self, ctx: object) -> None:
        code = _native.native_attribute(ctx, "code")
        error = _native.native_attribute(ctx, "error")
        self._realtime._enqueue_connection_callbacks(
            RealtimeErrorContext(
                code=code if isinstance(code, int) else None,
                message=str(error) if error is not None else None,
                error=error if isinstance(error, Exception) else None,
            ),
        )


def _presence_info(info: object) -> RealtimePresenceInfo:
    data = _native.native_attribute(info, "conn_info")
    user = _native.native_attribute(info, "user")
    typed_data = data if _is_json_record(data) else _empty_presence_data()
    return RealtimePresenceInfo(
        client=str(_native.native_attribute(info, "client", "")),
        user=user if isinstance(user, str) else None,
        data=typed_data,
    )


async def _run_connection_callback(
    callback: Invocation,
) -> None:
    result = callback()
    if inspect.isawaitable(result):
        await result


async def _wait_subscription(
    channel: Channel, subscription: CentrifugeSubscription
) -> None:
    await subscription.ready()
    if channel._type == "presence":
        await channel._wait_presence_sync()
    if channel._subscription is not subscription or not channel._subscribed:
        message = "realtime subscription was interrupted"
        raise RuntimeError(message)


class Channel:
    """Realtime broadcast, presence, or Postgres channel."""

    def __init__(
        self,
        realtime: Realtime,
        name: str,
        channel_type: ChannelType,
        *,
        fetch_config: _PostgresFetchConfig,
    ) -> None:
        """Create a channel managed by a realtime facade."""
        self._realtime: Realtime = realtime
        self._name: str = name
        self._type: ChannelType = channel_type
        self._fetch_config: _PostgresFetchConfig = fetch_config
        self._callbacks: dict[str, list[DynamicCallback]] = {}
        self._presence_state: dict[str, RealtimePresenceInfo] = {}
        self._presence_events: list[tuple[str, RealtimePresenceInfo]] = []
        self._presence_syncing: bool = False
        self._tracked_state: Mapping[str, JSONValue] = MappingProxyType({})
        self._subscribe_lock: asyncio.Lock = asyncio.Lock()
        # Fresh identities invalidate stale work without implying an order.
        self._subscribe_generation: object
        self._supersede_subscribe_intent()
        self._readiness_task: asyncio.Task[None] | None = None
        self._subscription: CentrifugeSubscription | None = None
        self._subscription_events: _ChannelEvents | None = None
        self._subscribed: bool
        self._paused: bool
        self._delivery_epoch: object
        self._presence_epoch: object
        self._presence_lock: asyncio.Lock = asyncio.Lock()
        self._presence_sync_task: asyncio.Task[None] | None = None
        self._presence_sync_pending: bool = False
        self._callback_queue: asyncio.Queue[_CallbackDelivery] = asyncio.Queue(
            maxsize=CALLBACK_QUEUE_LIMIT
        )
        self._callback_task: asyncio.Task[None] | None = None
        self._pending_presence_sync: object
        self._postgres_epoch: object
        self._rotate_postgres_epoch()
        self._postgres_session_lineage: SessionOperations | None = None
        self._postgres_lock: asyncio.Lock = asyncio.Lock()
        self._postgres_worker: PostgresFetchWorker[_PostgresDelivery] | None = None
        self._postgres_filters: dict[
            int,
            tuple[PostgresListenerEvent, str, str],
        ] = {}
        self._pause_delivery()

    def _supersede_subscribe_intent(self) -> None:
        self._subscribe_generation = object()

    def _rotate_postgres_epoch(self) -> None:
        self._postgres_epoch = object()

    def _clear_readiness_task(self) -> None:
        self._readiness_task = None

    @property
    def name(self) -> str:
        """Canonical channel name sent to realtime."""
        return self._name

    def on(self, event: str, callback: Callable[[_MessageT], object]) -> Channel:
        """Register a callback for messages or presence events.

        Returns
        -------
        Channel
            This channel, for chaining listener registrations.

        Raises
        ------
        ValueError
            The event is not supported by this channel type.

        """
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
        """Observe Postgres changes filtered by event, schema, and table.

        Returns
        -------
        UnsubscribeCallback
            An idempotent function that removes this listener.

        Raises
        ------
        ValueError
            The channel is not a Postgres channel or the event is unsupported.

        """
        if self._type != "postgres":
            raise ValueError(POSTGRES_ONLY)
        if event not in {*POSTGRES_EVENTS, "*"}:
            message = f"unsupported Postgres change event: {event}"
            raise ValueError(message)

        filtered = _filter_postgres_changes(event, schema, table, callback)

        self._callbacks.setdefault("*", []).append(filtered)
        self._postgres_filters[id(filtered)] = (event, schema, table)

        def unsubscribe() -> None:
            callbacks = self._callbacks["*"]
            if filtered in callbacks:
                callbacks.remove(filtered)
            _ = self._postgres_filters.pop(id(filtered), None)

        return unsubscribe

    def on_presence_sync(
        self, callback: Callable[[Mapping[str, RealtimePresenceInfo]], object]
    ) -> UnsubscribeCallback:
        """Observe immutable snapshots of a presence channel's current state.

        Requires a presence channel.

        Returns
        -------
        UnsubscribeCallback
            A function that removes this listener.

        """
        self._ensure_presence()
        self._callbacks.setdefault("presence_sync", []).append(callback)

        def unsubscribe() -> None:
            callbacks = self._callbacks["presence_sync"]
            if callback in callbacks:
                callbacks.remove(callback)

        return unsubscribe

    async def track(self, state: Mapping[str, JSONValue] | None = None) -> None:
        """Store local presence state while server identity remains authoritative.

        Requires a presence channel.

        Raises
        ------
        RuntimeError
            The channel is not subscribed.

        """
        self._ensure_presence()
        if not self._subscribed:
            raise RuntimeError(CHANNEL_NOT_SUBSCRIBED)
        self._tracked_state = _freeze_mapping(state or {})

    def get_presence_state(self) -> Mapping[str, RealtimePresenceInfo]:
        """Read the clients currently present.

        Requires a presence channel.

        Returns
        -------
        Mapping[str, RealtimePresenceInfo]
            An immutable snapshot indexed by client identifier.

        """
        self._ensure_presence()
        return MappingProxyType(dict(self._presence_state))

    @property
    def tracked_state(self) -> Mapping[str, JSONValue]:
        """Immutable snapshot of this client's local presence state."""
        self._ensure_presence()
        return MappingProxyType(dict(self._tracked_state))

    def _ensure_presence(self) -> None:
        if self._type != "presence":
            raise ValueError(PRESENCE_ONLY)

    def _capture_postgres_delivery_identity(self) -> _PostgresDeliveryIdentity:
        return _PostgresDeliveryIdentity(
            session_lineage=self._postgres_session_lineage,
            subscription_epoch=self._postgres_epoch,
        )

    async def _begin_postgres_epoch(self) -> None:
        if self._type != "postgres":
            return
        await self._stop_postgres_worker()
        self._rotate_postgres_epoch()
        self._postgres_session_lineage = self._realtime._connection_lineage()

    async def _end_postgres_epoch(self) -> None:
        if self._type != "postgres":
            return
        self._rotate_postgres_epoch()
        await self._stop_postgres_worker()

    async def _stop_postgres_worker(self) -> None:
        async with self._postgres_lock:
            worker = self._postgres_worker
            self._postgres_worker = None
        if worker is not None:
            await worker.abort()

    def _postgres_delivery_is_current(
        self,
        identity: _PostgresDeliveryIdentity,
    ) -> bool:
        _generation, lineage, session = (
            self._realtime._client_context.capture_session_binding()
        )
        return (
            self._subscribed
            and session is not None
            and identity.subscription_epoch is self._postgres_epoch
            and identity.session_lineage == lineage
        )

    def _has_postgres_listener(self, change: PostgresChange) -> bool:
        for callback in self._callbacks.get("*", []):
            listener_filter = self._postgres_filters.get(id(callback))
            if listener_filter is None:
                return True
            event, schema, table = listener_filter
            if (
                event in {"*", change.type}
                and schema == change.schema
                and table == change.table
            ):
                return True
        return False

    def _postgres_fetch_request(
        self,
        change: PostgresChange,
    ) -> _PostgresFetchRequest | None:
        database_name = self._realtime.database_name
        if (
            not self._fetch_config.enabled
            or change.mode != "lightweight"
            or change.type == "DELETE"
            or change.id is None
            or database_name is None
        ):
            return None
        return _PostgresFetchRequest(
            database_name=database_name,
            access_token=self._realtime._connection_token(),
            table=(
                change.table
                if change.schema == "public"
                else f"{change.schema}.{change.table}"
            ),
            row_id=change.id,
        )

    def _postgres_delivery(self, data: object) -> _PostgresDelivery | None:
        change = _postgres_change(data)
        if change is None or not self._has_postgres_listener(change):
            return None
        change = _normalize_postgres_delete(change)
        identity = self._capture_postgres_delivery_identity()
        if not self._postgres_delivery_is_current(identity):
            return None
        return _PostgresDelivery(change=change, identity=identity)

    async def _postgres_delivery_worker(
        self,
        identity: _PostgresDeliveryIdentity,
    ) -> PostgresFetchWorker[_PostgresDelivery] | None:
        async with self._postgres_lock:
            if not self._postgres_delivery_is_current(identity):
                return None
            if self._postgres_worker is None:
                self._postgres_worker = PostgresFetchWorker(
                    self._realtime._fetch_postgres_rows,
                    self._deliver_postgres,
                    queue_limit=POSTGRES_QUEUE_LIMIT,
                    batch_window_seconds=self._fetch_config.batch_window_seconds,
                    max_batch_size=self._fetch_config.max_batch_size,
                )
            return self._postgres_worker

    async def _receive_postgres_change(self, data: object) -> None:
        delivery = self._postgres_delivery(data)
        if delivery is None:
            return
        request = self._postgres_fetch_request(delivery.change)
        worker = await self._postgres_delivery_worker(delivery.identity)
        if worker is None:
            return
        try:
            await worker.enqueue(PostgresFetchJob(request=request, fallback=delivery))
        except RuntimeError:
            if self._postgres_delivery_is_current(delivery.identity):
                raise

    async def _deliver_postgres(
        self,
        outcome: PostgresFetchOutcome[_PostgresDelivery],
    ) -> None:
        delivery = outcome.job.fallback
        if not self._postgres_delivery_is_current(delivery.identity):
            return
        change = delivery.change
        if outcome.record is not None:
            change = replace(change, record=outcome.record, id=None, mode=None)
        elif outcome.job.request is not None:
            self._report_postgres_fetch_failure(
                change,
                outcome.job.request,
                outcome.error,
            )
        if self._postgres_delivery_is_current(delivery.identity):
            await self._emit(
                "*",
                change,
                postgres_identity=delivery.identity,
            )

    def _report_postgres_fetch_failure(
        self,
        change: PostgresChange,
        request: _PostgresFetchRequest,
        error: Exception | None,
    ) -> None:
        if error is None:
            identifier = f"{change.schema}.{change.table}:{request.row_id}"
            message = f"Postgres row not found: {identifier}"
            error = LookupError(message)
        asyncio.get_running_loop().call_exception_handler(
            {
                "message": POSTGRES_FETCH_FAILED_MESSAGE,
                "exception": error,
                "channel": self._name,
            }
        )

    async def subscribe(self) -> None:
        """Wait until this channel is subscribed and ready for use."""
        await self._realtime._subscribe(self)

    async def send(self, data: object) -> None:
        """Publish a broadcast payload to this channel."""
        await self._realtime._publish(self, data)

    async def unsubscribe(self) -> None:
        """Unsubscribe from this channel."""
        await self._realtime._unsubscribe(self)

    async def _emit(
        self,
        event: str,
        data: object,
        *,
        postgres_identity: _PostgresDeliveryIdentity | None = None,
    ) -> None:
        if not self._callbacks.get(event):
            return
        if event == "presence_sync":
            self._pending_presence_sync = NO_PENDING_CALLBACK
        delivery = _CallbackDelivery(
            event,
            data,
            postgres_identity,
            self._callback_epoch(event) if postgres_identity is None else None,
        )
        if not self._queue_callback(delivery):
            return
        task = self._callback_task
        if task is None or task.done():
            self._start_callback_dispatcher()

    def _queue_callback(self, delivery: _CallbackDelivery) -> bool:
        try:
            self._callback_queue.put_nowait(delivery)
        except asyncio.QueueFull:
            if delivery.event == "presence_sync":
                self._pending_presence_sync = delivery.data
                return False
            asyncio.get_running_loop().call_exception_handler(
                {
                    "message": CALLBACK_QUEUE_FULL_MESSAGE,
                    "channel": self._name,
                }
            )
        return True

    def _start_callback_dispatcher(self) -> None:
        task = asyncio.create_task(self._dispatch_callbacks())
        self._callback_task = task
        # Retain running application work even if its channel is removed.
        self._realtime._callback_tasks.add(task)
        task.add_done_callback(self._callback_dispatcher_finished)

    def _callback_dispatcher_finished(self, task: asyncio.Task[None]) -> None:
        self._realtime._callback_tasks.discard(task)
        if self._callback_task is task:
            self._callback_task = None
        if not task.cancelled() and (error := task.exception()) is not None:
            asyncio.get_running_loop().call_exception_handler(
                {
                    "message": "Volcano realtime callback dispatcher failed",
                    "exception": error,
                    "channel": self._name,
                }
            )

    async def _dispatch_callbacks(self) -> None:
        try:
            # Register the worker before user code can re-enter through eager tasks.
            await asyncio.sleep(0)
            while not self._callback_queue.empty():
                delivery = self._callback_queue.get_nowait()
                try:
                    await self._dispatch_delivery(delivery)
                finally:
                    self._callback_queue.task_done()
                    self._enqueue_pending_presence_sync()
        finally:
            # Event-loop cancellation must not leave queued delivery to restart.
            self._discard_callbacks()

    async def _dispatch_delivery(self, delivery: _CallbackDelivery) -> None:
        if not self._callback_delivery_is_current(delivery):
            return
        for callback in tuple(self._callbacks.get(delivery.event, [])):
            if not self._callback_delivery_is_current(delivery):
                return
            # Isolate a callback's own cancellation from later delivery.
            (error,) = await asyncio.gather(
                self._run_callback(callback, delivery),
                return_exceptions=True,
            )
            if isinstance(error, BaseException):
                asyncio.get_running_loop().call_exception_handler(
                    {
                        "message": "Volcano realtime callback failed",
                        "exception": error,
                        "channel": self._name,
                    }
                )

    def _callback_delivery_is_current(self, delivery: _CallbackDelivery) -> bool:
        if delivery.delivery_epoch is not None:
            return (
                not self._paused or delivery.event == "presence_sync"
            ) and delivery.delivery_epoch is self._callback_epoch(delivery.event)
        identity = delivery.postgres_identity
        return identity is None or self._postgres_delivery_is_current(identity)

    def _callback_epoch(self, event: str) -> object:
        if event in {"join", "leave", "presence_sync"}:
            return self._presence_epoch
        return self._delivery_epoch

    def _enqueue_pending_presence_sync(self) -> None:
        pending = self._pending_presence_sync
        if pending is NO_PENDING_CALLBACK or self._callback_queue.full():
            return
        self._pending_presence_sync = NO_PENDING_CALLBACK
        self._callback_queue.put_nowait(
            _CallbackDelivery(
                "presence_sync", pending, delivery_epoch=self._presence_epoch
            )
        )

    async def _run_callback(
        self,
        callback: DynamicCallback,
        delivery: _CallbackDelivery,
    ) -> None:
        if not self._callback_delivery_is_current(delivery):
            return
        result = callback(delivery.data)
        if inspect.isawaitable(result):
            await result

    def _replace_presence(self, clients: Mapping[str, object]) -> None:
        self._presence_state = {
            client_id: _presence_info(info) for client_id, info in clients.items()
        }

    async def _begin_presence_sync(self) -> None:
        async with self._presence_lock:
            self._presence_syncing = True
            self._presence_events.clear()

    async def _complete_presence_sync(self, clients: Mapping[str, object]) -> None:
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
        if event == "leave":
            _ = self._presence_state.pop(presence.client, None)

    async def _presence_join(self, info: object) -> None:
        if self._type != "presence" or info is None:
            return
        async with self._presence_lock:
            if not self._subscribed:
                return
            presence = _presence_info(info)
            if self._presence_syncing:
                self._presence_events.append(("join", presence))
            self._apply_presence_event("join", presence)
            await self._emit("join", presence)
            await self._emit("presence_sync", self.get_presence_state())

    async def _presence_leave(self, info: object) -> None:
        if self._type != "presence" or info is None:
            return
        async with self._presence_lock:
            if not self._subscribed:
                return
            presence = _presence_info(info)
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
                # A synchronous native reply must not starve cancellation or callbacks.
                await asyncio.sleep(0)
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
        if task is None or task.done():
            return
        _ = task.cancel()
        _ = await asyncio.gather(task, return_exceptions=True)

    async def _reset(self) -> None:
        self._invalidate()
        await self._end_postgres_epoch()
        await self._cancel_presence_sync()
        self._presence_state.clear()
        self._discard_presence_sync()
        self._tracked_state = MappingProxyType({})
        self._subscribed = False

    def _invalidate(self) -> None:
        if self._readiness_task is not None:
            _ = self._readiness_task.cancel()
        self._subscription = None
        self._subscription_events = None
        self._pause_delivery()

    def _pause_delivery(self) -> None:
        self._paused = True
        self._subscribed = False
        self._discard_callbacks()

    def _discard_callbacks(self, *, presence_only: bool = False) -> None:
        self._presence_epoch = object()
        if not presence_only:
            self._delivery_epoch = object()
        # Free capacity before recovered publications arrive behind a slow callback.
        for _ in range(self._callback_queue.qsize()):
            delivery = self._callback_queue.get_nowait()
            if presence_only and delivery.event == "message":
                # Requeue before task_done so queue.join cannot finish prematurely.
                self._callback_queue.put_nowait(delivery)
            self._callback_queue.task_done()
        self._pending_presence_sync = NO_PENDING_CALLBACK

    async def _transport_lost(self) -> None:
        self._subscribed = False
        # Recoverable channels already include queued messages in their offsets.
        if not self._paused and self._type != "broadcast":
            self._discard_callbacks(presence_only=self._type == "presence")
        await self._end_postgres_epoch()
        await self._presence_unsubscribed()


async def _reset_realtime_channels(
    channels: tuple[Channel, ...],
) -> asyncio.CancelledError | None:
    cancelled: asyncio.CancelledError | None = None
    for channel in channels:
        try:
            await channel._reset()
        except asyncio.CancelledError as error:
            cancelled = error
    return cancelled


class Realtime:
    """Manage project realtime connections and channels."""

    def __init__(
        self,
        client: RealtimeContext,
        *,
        api_url: str,
        client_factory: CentrifugeFactory = _native.centrifuge_client,
    ) -> None:
        """Create a lazily connected realtime facade."""
        self._client_context: RealtimeContext = client
        self._api_url: str = api_url
        self._client_factory: CentrifugeFactory = client_factory
        self._connection: _native.VolcanoCentrifugeConnection | None = None
        self._connection_session_lineage: SessionOperations | None = None
        self._connection_access_token: str | None = None
        self._connection_lock: asyncio.Lock = asyncio.Lock()
        self._channels: dict[str, Channel] = {}
        self._callback_tasks: set[asyncio.Task[None]] = set()
        self._removing_channels: set[str] = set()
        self._connect_callbacks: dict[
            int, Callable[[RealtimeConnectContext], object]
        ] = {}
        self._disconnect_callbacks: dict[
            int, Callable[[RealtimeDisconnectContext], object]
        ] = {}
        self._error_callbacks: dict[int, Callable[[RealtimeErrorContext], object]] = {}
        self._callback_ids: Iterator[int] = count()
        self._connection_callback_queue: asyncio.Queue[ConnectionDelivery] = (
            asyncio.Queue(maxsize=CALLBACK_QUEUE_LIMIT)
        )
        self._connection_callback_task: asyncio.Task[None] | None = None
        self._database_name: str | None = None

    @property
    def database_name(self) -> str | None:
        """Database bound to lightweight Postgres changes, or None if unbound."""
        return self._database_name

    def set_database_name(self, name: str | None) -> None:
        """Bind lightweight Postgres changes to a project database."""
        self._database_name = name

    async def _fetch_postgres_rows(
        self,
        requests: tuple[_PostgresFetchRequest, ...],
    ) -> tuple[Mapping[str, JSONValue] | None, ...]:
        first = requests[0]
        row_ids = [request.row_id for request in requests]
        transport = self._client_context.transport()
        if not isinstance(transport, AsyncDatabaseSelectTransport):
            raise TypeError(_POSTGRES_QUERY_UNAVAILABLE)
        response = await invoke_async(
            transport.query_database_select_async,
            authorization=first.access_token,
            database_name=first.database_name,
            body={
                "table": first.table,
                "filters": [{"column": "id", "operator": "in", "value": row_ids}],
                "limit": len(row_ids),
            },
        )
        rows = tuple(
            _checked_postgres_row(row)
            for row in database_rows(response_payload(response, 200))
        )
        return tuple(
            next(
                (row for row in rows if row.get("id") == request.row_id),
                None,
            )
            for request in requests
        )

    def on_connect(
        self, callback: Callable[[RealtimeConnectContext], object]
    ) -> UnsubscribeCallback:
        """Register a connection callback.

        Returns
        -------
        UnsubscribeCallback
            An idempotent function that removes this callback.

        """
        return register_callback(
            self._connect_callbacks, self._callback_ids, callback, CALLBACK_NOT_CALLABLE
        )

    def on_disconnect(
        self, callback: Callable[[RealtimeDisconnectContext], object]
    ) -> UnsubscribeCallback:
        """Register a disconnection callback.

        Returns
        -------
        UnsubscribeCallback
            An idempotent function that removes this callback.

        """
        return register_callback(
            self._disconnect_callbacks,
            self._callback_ids,
            callback,
            CALLBACK_NOT_CALLABLE,
        )

    def on_error(
        self, callback: Callable[[RealtimeErrorContext], object]
    ) -> UnsubscribeCallback:
        """Register a transport-error callback.

        Returns
        -------
        UnsubscribeCallback
            An idempotent function that removes this callback.

        """
        return register_callback(
            self._error_callbacks, self._callback_ids, callback, CALLBACK_NOT_CALLABLE
        )

    def _connection_delivery(
        self,
        context: RealtimeConnectContext
        | RealtimeDisconnectContext
        | RealtimeErrorContext,
    ) -> ConnectionDelivery:
        if isinstance(context, RealtimeConnectContext):
            return CallbackBatch(
                "connect",
                self._connect_callbacks,
                tuple(self._connect_callbacks),
                context,
            )
        if isinstance(context, RealtimeDisconnectContext):
            return CallbackBatch(
                "disconnect",
                self._disconnect_callbacks,
                tuple(self._disconnect_callbacks),
                context,
            )
        return CallbackBatch(
            "error", self._error_callbacks, tuple(self._error_callbacks), context
        )

    def _enqueue_connection_callbacks(
        self,
        context: RealtimeConnectContext
        | RealtimeDisconnectContext
        | RealtimeErrorContext,
    ) -> None:
        batch = self._connection_delivery(context)
        if batch.empty:
            return
        try:
            self._connection_callback_queue.put_nowait(batch)
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
            batch = self._connection_callback_queue.get_nowait()
            try:
                for callback in batch.invocations():
                    (error,) = await asyncio.gather(
                        _run_connection_callback(callback),
                        return_exceptions=True,
                    )
                    if isinstance(error, BaseException):
                        asyncio.get_running_loop().call_exception_handler(
                            {
                                "message": (
                                    "Volcano realtime connection callback failed"
                                ),
                                "exception": error,
                                "event": batch.event,
                            }
                        )
            finally:
                self._connection_callback_queue.task_done()

    def channel(
        self,
        name: str,
        *,
        channel_type: ChannelType = "broadcast",
        auto_fetch: bool = True,
        fetch_batch_window_ms: int = POSTGRES_BATCH_WINDOW_MS,
        fetch_max_batch_size: int = POSTGRES_MAX_BATCH_SIZE,
    ) -> Channel:
        """Get a stable channel facade for a realtime name and configuration.

        Returns
        -------
        Channel
            The existing channel for this type and name, or a newly created one.

        Raises
        ------
        ValueError
            The type or fetch settings are invalid, or the existing channel
            uses different fetch settings.
        RuntimeError
            Removal of this channel is still in progress.

        """
        channel_type = _validate_channel_type(channel_type)
        fetch_config = _postgres_fetch_config(
            auto_fetch=auto_fetch,
            fetch_batch_window_ms=fetch_batch_window_ms,
            fetch_max_batch_size=fetch_max_batch_size,
        )
        wire_name = f"{channel_type}:{name}"
        if wire_name in self._removing_channels:
            raise RuntimeError(CHANNEL_REMOVAL_IN_PROGRESS)
        channel = self._channels.get(wire_name)
        if channel is None:
            channel = Channel(
                self,
                wire_name,
                channel_type,
                fetch_config=fetch_config,
            )
            self._channels[wire_name] = channel
        elif channel._fetch_config != fetch_config:
            message = (
                f"channel {wire_name!r} already uses a different fetch configuration"
            )
            raise ValueError(message)
        return channel

    @property
    def is_connected(self) -> bool:
        """Whether the realtime transport is connected."""
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
                del self._channels[wire_name]
            finally:
                self._removing_channels.remove(wire_name)

    async def remove_all_channels(self) -> None:
        """Unsubscribe and forget every managed channel."""
        async with self._connection_lock:
            first_error: Exception | None = None
            for wire_name, channel in tuple(self._channels.items()):
                error = await self._remove_registered_channel(wire_name, channel)
                first_error = first_error or error
            if first_error is not None:
                raise first_error

    async def _remove_registered_channel(
        self,
        wire_name: str,
        channel: Channel,
    ) -> Exception | None:
        self._removing_channels.add(wire_name)
        try:
            await self._remove_channel(channel)
        except CENTRIFUGE_ERROR as error:
            return error
        else:
            if self._channels.get(wire_name) is channel:
                del self._channels[wire_name]
        finally:
            self._removing_channels.remove(wire_name)
        return None

    async def _remove_channel(self, channel: Channel) -> None:
        channel._supersede_subscribe_intent()
        await self._discard_subscription(channel)
        await channel._reset()

    async def _discard_subscription(self, channel: Channel) -> None:
        subscription = channel._subscription
        channel._subscription_events = None
        channel._pause_delivery()
        try:
            if subscription is not None:
                # Native state must change before any cancellable local cleanup.
                await _native.unsubscribe_native(subscription)
        finally:
            await channel._transport_lost()
        if subscription is not None and self._connection is not None:
            self._connection.remove_subscription(subscription)
        channel._subscription = None

    async def _token(self) -> str:
        lineage = self._connection_lineage()
        session = self._session_for_lineage(lineage)
        self._connection_access_token = session.access_token
        return session.access_token

    def _session_for_lineage(self, expected_lineage: SessionOperations) -> Session:
        _generation, lineage, session = self._client_context.capture_session_binding()
        if session is None:
            raise RuntimeError(NO_ACTIVE_SESSION)
        if lineage != expected_lineage:
            raise RuntimeError(CONNECTION_SESSION_CHANGED)
        return session

    def _connection_lineage(self) -> SessionOperations:
        lineage = self._connection_session_lineage
        if lineage is None:
            raise RuntimeError(CONNECTION_SESSION_UNAVAILABLE)
        return lineage

    def _connection_token(self) -> str:
        token = self._connection_access_token
        if token is None:
            raise RuntimeError(CONNECTION_SESSION_UNAVAILABLE)
        return token

    def _address(self) -> str:
        parsed = urlsplit(self._api_url)
        scheme = "wss" if parsed.scheme == "https" else "ws"
        query = urlencode(
            {"apikey": self._client_context.anon_token()}, quote_via=quote
        )
        return urlunsplit((scheme, parsed.netloc, "/realtime/v1/websocket", query, ""))

    async def _connect(self) -> _native.VolcanoCentrifugeConnection:
        async with self._connection_lock:
            return await self._connect_locked()

    async def _connect_locked(self) -> _native.VolcanoCentrifugeConnection:
        if self._connection is not None:
            _ = self._session_for_lineage(self._connection_lineage())
            return self._connection
        _generation, lineage, session = self._client_context.capture_session_binding()
        if session is None:
            raise RuntimeError(NO_ACTIVE_SESSION)
        connection = _native.VolcanoCentrifugeConnection(
            self._client_factory(
                self._address(),
                events=_ClientEvents(self),
                token=session.access_token,
                get_token=self._token,
            )
        )
        self._connection_session_lineage = lineage
        self._connection_access_token = session.access_token
        try:
            await connection.connect()
        except BaseException:
            self._connection_session_lineage = None
            self._connection_access_token = None
            raise
        try:
            current_session = self._session_for_lineage(lineage)
        except RuntimeError:
            self._connection = connection
            await connection.disconnect()
            self._connection = None
            self._connection_session_lineage = None
            self._connection_access_token = None
            raise
        self._connection_access_token = current_session.access_token
        self._connection = connection
        return connection

    async def _subscribe(self, channel: Channel) -> None:
        # A later stop supersedes this request, including time spent waiting for locks.
        generation = channel._subscribe_generation
        async with channel._subscribe_lock:
            subscription = None
            try:
                async with self._connection_lock:
                    subscription = await self._prepare_subscription(channel, generation)
                    if channel._subscribed:
                        return
                    await self._resume_subscription(channel, subscription)
                await self._wait_subscription_readiness(channel, subscription)
            except BaseException as error:
                await self._cleanup_failed_subscription(channel, subscription, error)
                raise

    @staticmethod
    async def _resume_subscription(
        channel: Channel, subscription: CentrifugeSubscription
    ) -> None:
        channel._paused = False
        await subscription.subscribe()

    @staticmethod
    async def _wait_subscription_readiness(
        channel: Channel, subscription: CentrifugeSubscription
    ) -> None:
        channel._readiness_task = asyncio.create_task(
            _wait_subscription(channel, subscription)
        )
        try:
            await channel._readiness_task
        finally:
            channel._clear_readiness_task()

    async def _cleanup_failed_subscription(
        self,
        channel: Channel,
        subscription: CentrifugeSubscription | None,
        error: BaseException,
    ) -> None:
        if (
            subscription is None
            or channel._subscription is not subscription
            or channel._paused
        ):
            # An explicit pause or removal owns the newer subscription intent.
            return
        channel._supersede_subscribe_intent()
        channel._subscription_events = None
        channel._pause_delivery()
        try:
            async with self._connection_lock:
                if channel._subscription is subscription:
                    await self._discard_subscription(channel)
        except CENTRIFUGE_ERROR:
            error.add_note("Failed to clean up the realtime subscription")

    async def _prepare_subscription(
        self, channel: Channel, generation: object
    ) -> CentrifugeSubscription:
        if generation is not channel._subscribe_generation:
            raise asyncio.CancelledError
        if self._channels.get(channel._name) is not channel:
            raise RuntimeError(CHANNEL_NOT_MANAGED)
        connection = await self._connect_locked()
        if channel._subscription is not None and channel._subscription_events is None:
            await self._discard_subscription(channel)
        if channel._subscription is None:
            channel._subscription_events = _ChannelEvents(channel)
            channel._subscription = connection.new_subscription(
                channel._name,
                events=channel._subscription_events,
                join_leave=channel._type == "presence",
                recoverable=channel._type != "postgres",
            )
        return channel._subscription

    async def _sync_presence(self, channel: Channel) -> None:
        if channel._subscription is None:
            return
        await channel._begin_presence_sync()
        try:
            # Native replies must settle even after the roster refresh is cancelled.
            query = asyncio.create_task(channel._subscription.presence())
            query.add_done_callback(_native.consume_presence_result)
            result = await asyncio.shield(query)
        except CENTRIFUGE_ERROR as error:
            await self._report_presence_sync_failure(channel, error)
            return
        except BaseException:
            await channel._abort_presence_sync()
            raise
        clients = _native.native_presence_clients(
            _native.native_attribute(result, "clients")
        )
        if clients is not None:
            await channel._complete_presence_sync(clients)
        else:
            await channel._abort_presence_sync()

    async def _report_presence_sync_failure(
        self, channel: Channel, error: Exception
    ) -> None:
        try:
            await channel._fail_presence_sync()
        except BaseException:
            await channel._abort_presence_sync()
            raise
        code = _native.native_attribute(error, "code")
        self._enqueue_connection_callbacks(
            RealtimeErrorContext(
                code=code if isinstance(code, int) else None,
                message=str(error),
                error=error,
            ),
        )

    async def _publish(self, channel: Channel, data: object) -> None:
        async with self._connection_lock:
            if channel._type != "broadcast":
                raise ValueError(BROADCAST_ONLY)
            subscription = channel._subscription
            if not channel._subscribed or subscription is None:
                raise RuntimeError(CHANNEL_NOT_SUBSCRIBED)
            _ = await subscription.publish(data)

    async def _unsubscribe(self, channel: Channel) -> None:
        async with self._connection_lock:
            channel._supersede_subscribe_intent()
            if not channel._paused:
                channel._pause_delivery()
            if channel._subscription is not None:
                await _native.unsubscribe_native(channel._subscription)

    async def disconnect(self) -> None:
        """Disconnect and reset every channel managed by this facade."""
        async with self._connection_lock:
            connection = self._connection
            self._connection = None
            channels = tuple(self._channels.values())
            for channel in channels:
                channel._supersede_subscribe_intent()
                channel._invalidate()
            try:
                cancelled = await _reset_realtime_channels(channels)
            finally:
                try:
                    if connection is not None:
                        await connection.disconnect()
                finally:
                    self._connection_session_lineage = None
                    self._connection_access_token = None
            if cancelled is not None:
                raise cancelled
