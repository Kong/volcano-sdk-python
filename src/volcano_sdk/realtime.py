"""Realtime broadcast facade."""

from __future__ import annotations

import asyncio
import importlib
import inspect
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Literal, Protocol, TypeAlias, cast
from urllib.parse import quote, urlsplit, urlunsplit

from .models import JSONValue, _freeze_json

MessageCallback = Callable[[Any], Any]
RealtimeCallback = Callable[[Any], Any]
UnsubscribeCallback = Callable[[], None]
ChannelType: TypeAlias = Literal["broadcast", "presence"]
SUPPORTED_CHANNEL_TYPES = frozenset({"broadcast", "presence"})
CENTRIFUGE_ERROR = cast(
    "type[Exception]",
    importlib.import_module("centrifuge").CentrifugeError,
)
CALLBACK_QUEUE_LIMIT = 128
CALLBACK_QUEUE_FULL_MESSAGE = (
    "Volcano realtime callback queue is full; publication dropped"
)
CHANNEL_NOT_SUBSCRIBED = "Channel must be subscribed before sending"
CHANNEL_REMOVAL_IN_PROGRESS = "realtime channel removal is in progress"
CHANNEL_NOT_MANAGED = "realtime channel is no longer managed"
PRESENCE_ONLY = "operation is only available for presence channels"
BROADCAST_ONLY = "send is only available for broadcast channels"
CALLBACK_NOT_CALLABLE = "callback must be callable"
SUBSCRIPTION_REGISTRY_UNAVAILABLE = (
    "centrifuge client subscription registry is unavailable"
)


def _empty_presence_data() -> Mapping[str, JSONValue]:
    return MappingProxyType({})


def _validate_channel_type(channel_type: str) -> ChannelType:
    if channel_type not in SUPPORTED_CHANNEL_TYPES:
        message = f"unsupported realtime channel type: {channel_type}"
        raise ValueError(message)
    return cast("ChannelType", channel_type)


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


class RealtimeContext(Protocol):
    """Client capabilities required by realtime connections."""

    def _anon_token(self) -> str: ...

    def _session_token(self) -> str: ...


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
            if key.endswith(f":{channel}")
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
        await self._channel._emit("message", ctx.pub.data)

    async def on_subscribing(self, ctx: Any) -> None:
        del ctx

    async def on_subscribed(self, ctx: Any) -> None:
        del ctx
        if self._channel._type == "presence":
            await self._channel._realtime._sync_presence(self._channel)

    async def on_unsubscribed(self, ctx: Any) -> None:
        del ctx
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
    """Realtime broadcast or presence channel."""

    def __init__(
        self,
        realtime: Realtime,
        name: str,
        channel_type: ChannelType,
    ) -> None:
        """Create a channel managed by a realtime facade."""
        self._realtime = realtime
        self._name = name
        self._type = channel_type
        self._callbacks: dict[str, list[MessageCallback]] = {}
        self._presence_state: dict[str, RealtimePresenceInfo] = {}
        self._tracked_state: Mapping[str, JSONValue] = MappingProxyType({})
        self._subscription: CentrifugeSubscription | None = None
        self._callback_queue: asyncio.Queue[tuple[str, Any]] = asyncio.Queue(
            maxsize=CALLBACK_QUEUE_LIMIT
        )
        self._callback_task: asyncio.Task[None] | None = None
        self._active_callback_task: asyncio.Task[None] | None = None
        self._callback_stop: asyncio.Event | None = None

    @property
    def name(self) -> str:
        """Return the canonical channel name sent to realtime."""
        return self._name

    def on(self, event: str, callback: MessageCallback) -> Channel:
        """Register a callback for messages or presence events."""
        allowed_events = (
            {"message"}
            if self._type == "broadcast"
            else {"message", "join", "leave", "presence_sync"}
        )
        if event not in allowed_events:
            message = f"unsupported realtime event: {event}"
            raise ValueError(message)
        self._callbacks.setdefault(event, []).append(callback)
        return self

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
        if self._subscription is None:
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

    async def subscribe(self) -> None:
        """Subscribe to this channel."""
        await self._realtime._subscribe(self)

    async def send(self, data: Any) -> None:
        """Publish a broadcast payload to this channel."""
        await self._realtime._publish(self, data)

    async def unsubscribe(self) -> None:
        """Unsubscribe from this channel."""
        await self._realtime._unsubscribe(self)

    async def _emit(self, event: str, data: Any) -> None:
        task = self._callback_task
        if task is None or task.done():
            self._start_callback_dispatcher()
        elif self._callback_stop is not None and self._callback_stop.is_set():
            self._callback_task = asyncio.create_task(
                self._restart_callback_dispatcher(task)
            )
            self._callback_stop = None
        try:
            self._callback_queue.put_nowait((event, data))
        except asyncio.QueueFull:
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
            event, data = await self._callback_queue.get()
            try:
                for callback in tuple(self._callbacks.get(event, [])):
                    active_task = asyncio.create_task(
                        self._run_callback(callback, data)
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

    async def _run_callback(self, callback: MessageCallback, data: Any) -> None:
        result = callback(data)
        if inspect.isawaitable(result):
            await result

    async def _replace_presence(self, clients: Mapping[str, Any]) -> None:
        self._presence_state = {
            client_id: self._presence_info(info) for client_id, info in clients.items()
        }
        await self._emit("presence_sync", self.get_presence_state())

    async def _presence_join(self, info: Any) -> None:
        if self._type != "presence" or info is None:
            return
        presence = self._presence_info(info)
        self._presence_state[presence.client] = presence
        await self._emit("join", presence)
        await self._emit("presence_sync", self.get_presence_state())

    async def _presence_leave(self, info: Any) -> None:
        if self._type != "presence" or info is None:
            return
        presence = self._presence_info(info)
        self._presence_state.pop(presence.client, None)
        await self._emit("leave", presence)
        await self._emit("presence_sync", self.get_presence_state())

    async def _presence_unsubscribed(self) -> None:
        if self._type != "presence":
            return
        self._presence_state.clear()
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

    async def _reset(self) -> None:
        self._subscription = None
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
        self._presence_state.clear()
        self._tracked_state = MappingProxyType({})


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
    ) -> Channel:
        """Return a stable channel facade for a broadcast or presence name."""
        channel_type = _validate_channel_type(channel_type)
        wire_name = f"{channel_type}:{name}"
        if wire_name in self._removing_channels:
            raise RuntimeError(CHANNEL_REMOVAL_IN_PROGRESS)
        if wire_name not in self._channels:
            self._channels[wire_name] = Channel(self, wire_name, channel_type)
        return self._channels[wire_name]

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

    async def _sync_presence(self, channel: Channel) -> None:
        if channel._subscription is None:
            return
        try:
            result = await channel._subscription.presence()
        except CENTRIFUGE_ERROR as error:
            await channel._replace_presence({})
            self._enqueue_connection_callbacks(
                "error",
                RealtimeErrorContext(
                    code=getattr(error, "code", None),
                    message=str(error),
                    error=error,
                ),
            )
            return
        clients = getattr(result, "clients", None)
        if isinstance(clients, Mapping):
            await channel._replace_presence(cast("Mapping[str, Any]", clients))

    async def _publish(self, channel: Channel, data: Any) -> None:
        async with self._connection_lock:
            if channel._type != "broadcast":
                raise ValueError(BROADCAST_ONLY)
            if channel._subscription is None:
                raise RuntimeError(CHANNEL_NOT_SUBSCRIBED)
            await channel._subscription.publish(data)

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
