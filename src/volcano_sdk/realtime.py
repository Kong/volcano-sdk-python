"""Realtime broadcast facade."""

from __future__ import annotations

import asyncio
import importlib
import inspect
import logging
from collections.abc import Awaitable, Callable
from threading import Lock
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
_LOGGER = logging.getLogger(__name__)


def _current_task() -> asyncio.Task[Any] | None:
    try:
        return asyncio.current_task()
    except RuntimeError:
        return None


def _running_loop() -> asyncio.AbstractEventLoop | None:
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        return None


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
    def __init__(
        self,
        channel: Channel,
        channel_generation: int,
        auth_generation: int,
    ) -> None:
        self._channel = channel
        self._channel_generation = channel_generation
        self._auth_generation = auth_generation

    async def on_publication(self, ctx: PublicationContext) -> None:
        if (
            self._channel_generation == self._channel._auth_generation
            and self._auth_generation
            == self._channel._realtime._auth_generation_snapshot()
        ):
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
        self._subscription_auth_generation: int | None = None
        self._callback_queue: asyncio.Queue[tuple[int, int, Any]] = asyncio.Queue(
            maxsize=CALLBACK_QUEUE_LIMIT
        )
        self._callback_task: asyncio.Task[None] | None = None
        self._active_callback_task: asyncio.Task[None] | None = None
        self._active_callback_auth_generation: int | None = None
        self._callback_stop: asyncio.Event | None = None
        self._auth_generation = 0

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
            self._callback_queue.put_nowait(
                (
                    self._auth_generation,
                    self._realtime._auth_generation_snapshot(),
                    data,
                )
            )
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
            generation, auth_generation, data = await self._callback_queue.get()
            try:
                for callback in tuple(self._message_callbacks):
                    if not await self._dispatch_callback(
                        callback,
                        data,
                        generation,
                        auth_generation,
                    ):
                        break
            finally:
                self._callback_queue.task_done()

    async def _dispatch_callback(
        self,
        callback: MessageCallback,
        data: Any,
        generation: int,
        auth_generation: int,
    ) -> bool:
        if (
            generation != self._auth_generation
            or auth_generation != self._realtime._auth_generation_snapshot()
        ):
            return False
        active_task = asyncio.create_task(self._run_callback(callback, data))
        self._active_callback_task = active_task
        self._active_callback_auth_generation = auth_generation
        try:
            (error,) = await asyncio.gather(active_task, return_exceptions=True)
        finally:
            self._active_callback_task = None
            self._active_callback_auth_generation = None
        if (
            generation != self._auth_generation
            or auth_generation != self._realtime._auth_generation_snapshot()
        ):
            return False
        if isinstance(error, BaseException):
            asyncio.get_running_loop().call_exception_handler(
                {
                    "message": "Volcano realtime callback failed",
                    "exception": error,
                    "channel": self._name,
                }
            )
        return True

    async def _run_callback(self, callback: MessageCallback, data: Any) -> None:
        result = callback(data)
        if inspect.isawaitable(result):
            await result

    async def _reset(self) -> None:
        self._invalidate_authentication()
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

    def _invalidate_authentication(self) -> None:
        self._auth_generation += 1
        self._subscription = None
        self._subscription_auth_generation = None
        if (
            self._active_callback_task is not None
            and self._active_callback_task is not _current_task()
        ):
            self._active_callback_task.cancel()
        while not self._callback_queue.empty():
            self._callback_queue.get_nowait()
            self._callback_queue.task_done()

    def _invalidate_authentication_before(self, auth_generation: int) -> None:
        self._discard_callbacks_before(auth_generation)
        subscription_generation = self._subscription_auth_generation
        if (
            subscription_generation is not None
            and subscription_generation >= auth_generation
        ):
            return
        self._invalidate_authentication()

    def _discard_callbacks_before(self, auth_generation: int) -> None:
        active_generation = self._active_callback_auth_generation
        active_task = self._active_callback_task
        if (
            active_generation is not None
            and active_generation < auth_generation
            and active_task is not None
            and active_task is not _current_task()
        ):
            active_task.cancel()
        current_items: list[tuple[int, int, Any]] = []
        while not self._callback_queue.empty():
            item = self._callback_queue.get_nowait()
            self._callback_queue.task_done()
            if item[1] >= auth_generation:
                current_items.append(item)
        for item in current_items:
            self._callback_queue.put_nowait(item)

    def _discard_closed_loop_authentication(self) -> None:
        self._auth_generation += 1
        self._subscription = None
        self._subscription_auth_generation = None
        self._callback_task = None
        self._active_callback_task = None
        self._active_callback_auth_generation = None
        self._callback_stop = None
        self._callback_queue = asyncio.Queue(maxsize=CALLBACK_QUEUE_LIMIT)


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
        self._connection_auth_generation: int | None = None
        self._connection_lock = asyncio.Lock()
        self._loop: asyncio.AbstractEventLoop | None = None
        self._auth_generation = 0
        self._auth_generation_lock = Lock()
        self._channels: dict[str, Channel] = {}
        self._auth_cleanup_tasks: set[asyncio.Task[None]] = set()
        self._in_flight_publishes: dict[asyncio.Task[Any], int] = {}

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
        generation = self._auth_generation_snapshot()
        existing_connection = await self._connection_for_generation(generation)
        if existing_connection is not None:
            return existing_connection
        self._loop = asyncio.get_running_loop()
        while self._connection is None:
            generation = self._auth_generation_snapshot()
            connection = await self._open_connection(generation)
            if connection is not None:
                self._connection = connection
                self._connection_auth_generation = generation
        return self._connection

    async def _connection_for_generation(
        self,
        generation: int,
    ) -> CentrifugeConnection | None:
        connection = self._connection
        if connection is None or self._connection_auth_generation == generation:
            return connection
        self._connection = None
        self._connection_auth_generation = None
        await self._close_invalidated(connection)
        return None

    async def _open_connection(
        self,
        generation: int,
    ) -> CentrifugeConnection | None:
        connection = _VolcanoCentrifugeConnection(
            self._client_factory(
                self._address(),
                token=self._client_context._session_token(),
                get_token=self._token,
            )
        )
        try:
            await connection.connect()
        except Exception:
            if generation == self._auth_generation_snapshot():
                raise
            await self._close_invalidated(connection)
            return None
        if generation == self._auth_generation_snapshot():
            return connection
        await self._close_invalidated(connection)
        return None

    async def _subscribe(self, channel: Channel) -> None:
        async with self._connection_lock:
            await self._subscribe_locked(channel)

    async def _subscribe_locked(self, channel: Channel) -> None:
        while True:
            generation = channel._auth_generation
            subscription = channel._subscription
            if subscription is None:
                connection = await self._connect_locked()
                auth_generation = self._auth_generation_snapshot()
                subscription = connection.new_subscription(
                    channel._name,
                    events=_ChannelEvents(channel, generation, auth_generation),
                )
                channel._subscription = subscription
                channel._subscription_auth_generation = auth_generation
            if await self._subscribe_current_generation(
                channel, subscription, generation
            ):
                return
            if channel._subscription is subscription:
                channel._subscription = None

    async def _subscribe_current_generation(
        self,
        channel: Channel,
        subscription: CentrifugeSubscription,
        generation: int,
    ) -> bool:
        try:
            await subscription.subscribe()
        except Exception:
            if self._subscription_is_current(channel, subscription, generation):
                raise
        return self._subscription_is_current(channel, subscription, generation)

    def _subscription_is_current(
        self,
        channel: Channel,
        subscription: CentrifugeSubscription,
        generation: int,
    ) -> bool:
        return (
            generation == channel._auth_generation
            and channel._subscription is subscription
            and channel._subscription_auth_generation
            == self._auth_generation_snapshot()
        )

    async def _publish(self, channel: Channel, data: Any) -> None:
        generation = self._auth_generation_snapshot()
        async with self._connection_lock:
            if (
                generation != self._auth_generation_snapshot()
                or channel._subscription is None
                or channel._subscription_auth_generation != generation
            ):
                raise RuntimeError(CHANNEL_NOT_SUBSCRIBED)
            task = asyncio.current_task()
            if task is not None:
                self._in_flight_publishes[task] = generation
            try:
                await channel._subscription.publish(data)
            finally:
                if task is not None:
                    self._in_flight_publishes.pop(task, None)

    async def _unsubscribe(self, channel: Channel) -> None:
        async with self._connection_lock:
            if channel._subscription is not None:
                await channel._subscription.unsubscribe()

    async def disconnect(self) -> None:
        """Disconnect and reset every channel managed by this facade."""
        async with self._connection_lock:
            connection = self._connection
            self._connection = None
            self._connection_auth_generation = None
            try:
                if connection is not None:
                    await connection.disconnect()
            finally:
                await self._await_auth_cleanup()
                for channel in tuple(self._channels.values()):
                    await channel._reset()
            self._loop = None

    async def _await_auth_cleanup(self) -> None:
        while self._auth_cleanup_tasks:
            tasks = tuple(self._auth_cleanup_tasks)
            await asyncio.gather(*tasks, return_exceptions=True)
            self._auth_cleanup_tasks.difference_update(tasks)

    def on_auth_change(self) -> None:
        """Immediately invalidate work authenticated by the previous session."""
        auth_generation = self._advance_auth_generation()
        loop = self._loop
        if loop is not None and loop.is_closed():
            self._discard_closed_loop_authentication()
            return
        if loop is not None and _running_loop() is not loop:
            self._schedule_auth_invalidation(loop, auth_generation)
            return
        self._invalidate_authentication(auth_generation)

    def _schedule_auth_invalidation(
        self,
        loop: asyncio.AbstractEventLoop,
        auth_generation: int,
    ) -> None:
        try:
            loop.call_soon_threadsafe(self._invalidate_authentication, auth_generation)
        except RuntimeError:
            self._discard_closed_loop_authentication()

    def _invalidate_authentication(self, auth_generation: int) -> None:
        connection = self._connection
        connection_generation = self._connection_auth_generation
        if connection_generation is None or connection_generation < auth_generation:
            self._connection = None
            self._connection_auth_generation = None
        else:
            connection = None
        channels = tuple(self._channels.values())
        for task, generation in tuple(self._in_flight_publishes.items()):
            if generation < auth_generation:
                task.cancel()
        for channel in channels:
            channel._invalidate_authentication_before(auth_generation)
        if connection is None or self._loop is None:
            return
        task = self._loop.create_task(self._close_invalidated(connection))
        self._auth_cleanup_tasks.add(task)
        task.add_done_callback(self._auth_cleanup_tasks.discard)

    def _discard_closed_loop_authentication(self) -> None:
        self._connection = None
        self._connection_auth_generation = None
        self._connection_lock = asyncio.Lock()
        self._loop = None
        self._auth_cleanup_tasks.clear()
        self._in_flight_publishes.clear()
        for channel in tuple(self._channels.values()):
            channel._discard_closed_loop_authentication()

    def _advance_auth_generation(self) -> int:
        with self._auth_generation_lock:
            self._auth_generation += 1
            return self._auth_generation

    def _auth_generation_snapshot(self) -> int:
        with self._auth_generation_lock:
            return self._auth_generation

    async def _close_invalidated(
        self,
        connection: CentrifugeConnection,
    ) -> None:
        try:
            await connection.disconnect()
        except Exception:
            _LOGGER.exception("Volcano realtime disconnect failed after auth change")
