"""Realtime broadcast facade."""

from __future__ import annotations

import asyncio
import importlib
import inspect
from collections.abc import Awaitable, Callable
from typing import Any, Protocol, cast
from urllib.parse import quote, urlsplit, urlunsplit

from typing_extensions import override

MessageCallback = Callable[[Any], Any]
CALLBACK_QUEUE_LIMIT = 128
CALLBACK_QUEUE_FULL_MESSAGE = (
    "Volcano realtime callback queue is full; publication dropped"
)
CHANNEL_NOT_SUBSCRIBED = "Channel must be subscribed before sending"
SUBSCRIPTION_REGISTRY_UNAVAILABLE = (
    "centrifuge client subscription registry is unavailable"
)


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


class CentrifugeConnection(Protocol):
    """Centrifuge connection operations used by the SDK."""

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
    ) -> CentrifugeSubscription:
        """Create a subscription for a remote channel."""
        ...


class CentrifugeFactory(Protocol):
    """Construct a typed Centrifuge connection."""

    def __call__(
        self,
        address: str,
        *,
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
    token: str,
    get_token: Callable[[], Awaitable[str]],
) -> CentrifugeConnection:
    module = importlib.import_module("centrifuge")
    constructor = cast("CentrifugeConstructor", module.Client)
    return cast(
        "CentrifugeConnection",
        constructor(address, token=token, get_token=get_token),
    )


class _ProjectAwareSubscriptions(dict[str, Any]):
    @override
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

    def new_subscription(
        self,
        name: str,
        *,
        events: Any,
    ) -> CentrifugeSubscription:
        return self._connection.new_subscription(name, events=events)


class _ChannelEvents:
    def __init__(self, channel: Channel) -> None:
        self._channel = channel

    async def on_publication(self, ctx: PublicationContext) -> None:
        await self._channel._emit(ctx.pub.data)

    async def on_subscribing(self, ctx: Any) -> None:
        del ctx

    async def on_subscribed(self, ctx: Any) -> None:
        del ctx

    async def on_unsubscribed(self, ctx: Any) -> None:
        del ctx

    async def on_join(self, ctx: Any) -> None:
        del ctx

    async def on_leave(self, ctx: Any) -> None:
        del ctx

    async def on_error(self, ctx: Any) -> None:
        del ctx


class Channel:
    """Realtime broadcast channel."""

    def __init__(self, realtime: Realtime, name: str) -> None:
        """Create a channel managed by a realtime facade."""
        self._realtime = realtime
        self._name = name
        self._message_callbacks: list[MessageCallback] = []
        self._subscription: CentrifugeSubscription | None = None
        self._callback_queue: asyncio.Queue[Any] = asyncio.Queue(
            maxsize=CALLBACK_QUEUE_LIMIT
        )
        self._callback_task: asyncio.Task[None] | None = None
        self._active_callback_task: asyncio.Task[None] | None = None
        self._callback_stop: asyncio.Event | None = None

    def on(self, event: str, callback: MessageCallback) -> Channel:
        """Register a callback for broadcast messages."""
        if event != "message":
            message = f"unsupported realtime event: {event}"
            raise ValueError(message)
        self._message_callbacks.append(callback)
        return self

    async def subscribe(self) -> None:
        """Subscribe to this channel."""
        await self._realtime._subscribe(self)

    async def send(self, data: Any) -> None:
        """Publish a broadcast payload to this channel."""
        await self._realtime._publish(self, data)

    async def unsubscribe(self) -> None:
        """Unsubscribe from this channel."""
        await self._realtime._unsubscribe(self)

    async def _emit(self, data: Any) -> None:
        task = self._callback_task
        if task is None or task.done():
            self._start_callback_dispatcher()
        elif self._callback_stop is not None and self._callback_stop.is_set():
            self._callback_task = asyncio.create_task(
                self._restart_callback_dispatcher(task)
            )
            self._callback_stop = None
        try:
            self._callback_queue.put_nowait(data)
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
            data = await self._callback_queue.get()
            try:
                for callback in tuple(self._message_callbacks):
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
        self._connection: CentrifugeConnection | None = None
        self._connection_lock = asyncio.Lock()
        self._channels: dict[str, Channel] = {}

    def channel(self, name: str) -> Channel:
        """Return a stable channel facade for a broadcast name."""
        wire_name = f"broadcast:{name}"
        if wire_name not in self._channels:
            self._channels[wire_name] = Channel(self, wire_name)
        return self._channels[wire_name]

    async def _token(self) -> str:
        return self._client_context._session_token()

    def _address(self) -> str:
        parsed = urlsplit(self._api_url)
        scheme = "wss" if parsed.scheme == "https" else "ws"
        query = f"apikey={quote(self._client_context._anon_token(), safe='')}"
        return urlunsplit((scheme, parsed.netloc, "/realtime/v1/websocket", query, ""))

    async def _connect(self) -> CentrifugeConnection:
        async with self._connection_lock:
            return await self._connect_locked()

    async def _connect_locked(self) -> CentrifugeConnection:
        if self._connection is not None:
            return self._connection
        connection = _VolcanoCentrifugeConnection(
            self._client_factory(
                self._address(),
                token=self._client_context._session_token(),
                get_token=self._token,
            )
        )
        await connection.connect()
        self._connection = connection
        return connection

    async def _subscribe(self, channel: Channel) -> None:
        async with self._connection_lock:
            connection = await self._connect_locked()
            if channel._subscription is None:
                channel._subscription = connection.new_subscription(
                    channel._name,
                    events=_ChannelEvents(channel),
                )
            await channel._subscription.subscribe()

    async def _publish(self, channel: Channel, data: Any) -> None:
        async with self._connection_lock:
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
