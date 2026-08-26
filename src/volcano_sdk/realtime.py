from __future__ import annotations

import importlib
import inspect
from collections.abc import Awaitable, Callable
from typing import Any, Protocol, cast
from urllib.parse import quote, urlsplit, urlunsplit

MessageCallback = Callable[[Any], Any]


class RealtimeContext(Protocol):
    def _anon_token(self) -> str: ...

    def _session_token(self) -> str: ...


class CentrifugeSubscription(Protocol):
    async def subscribe(self) -> None: ...

    async def publish(self, data: Any) -> Any: ...

    async def unsubscribe(self) -> None: ...


class CentrifugeConnection(Protocol):
    async def connect(self) -> None: ...

    async def disconnect(self) -> None: ...

    def new_subscription(
        self,
        name: str,
        *,
        events: Any,
    ) -> CentrifugeSubscription: ...


class CentrifugeFactory(Protocol):
    def __call__(
        self,
        address: str,
        *,
        token: str,
        get_token: Callable[[], Awaitable[str]],
    ) -> CentrifugeConnection: ...


class CentrifugeConstructor(Protocol):
    def __call__(
        self,
        address: str,
        *,
        token: str,
        get_token: Callable[[], Awaitable[str]],
    ) -> object: ...


class Publication(Protocol):
    data: Any


class PublicationContext(Protocol):
    pub: Publication


def _centrifuge_client(
    address: str,
    *,
    token: str,
    get_token: Callable[[], Awaitable[str]],
) -> CentrifugeConnection:
    module = importlib.import_module("centrifuge")
    constructor = cast(CentrifugeConstructor, module.Client)
    return cast(
        CentrifugeConnection,
        constructor(address, token=token, get_token=get_token),
    )


class _ProjectAwareSubscriptions(dict[str, Any]):
    def get(self, key: str, default: Any = None) -> Any:
        subscription = super().get(key)
        if subscription is not None:
            return subscription
        for channel, candidate in self.items():
            if key.endswith(f":{channel}"):
                return candidate
        return default


class _VolcanoCentrifugeConnection:
    def __init__(self, connection: CentrifugeConnection) -> None:
        self._connection = connection
        state = vars(connection)
        subscriptions = state.get("_subs")
        if not isinstance(subscriptions, dict):
            raise TypeError("centrifuge client subscription registry is unavailable")
        state["_subs"] = _ProjectAwareSubscriptions(subscriptions)

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
    def __init__(self, realtime: Realtime, name: str) -> None:
        self._realtime = realtime
        self._name = name
        self._message_callbacks: list[MessageCallback] = []
        self._subscription: CentrifugeSubscription | None = None

    def on(self, event: str, callback: MessageCallback) -> Channel:
        if event != "message":
            raise ValueError(f"unsupported realtime event: {event}")
        self._message_callbacks.append(callback)
        return self

    async def subscribe(self) -> None:
        connection = await self._realtime._connect()
        if self._subscription is None:
            self._subscription = connection.new_subscription(
                self._name,
                events=_ChannelEvents(self),
            )
        await self._subscription.subscribe()

    async def send(self, data: Any) -> None:
        if self._subscription is None:
            raise RuntimeError("Channel must be subscribed before sending")
        await self._subscription.publish(data)

    async def unsubscribe(self) -> None:
        if self._subscription is None:
            return
        await self._subscription.unsubscribe()

    async def _emit(self, data: Any) -> None:
        for callback in tuple(self._message_callbacks):
            result = callback(data)
            if inspect.isawaitable(result):
                await result

    def _reset(self) -> None:
        self._subscription = None


class Realtime:
    def __init__(
        self,
        client: RealtimeContext,
        *,
        api_url: str,
        client_factory: CentrifugeFactory = _centrifuge_client,
    ) -> None:
        self._client_context = client
        self._api_url = api_url
        self._client_factory = client_factory
        self._connection: CentrifugeConnection | None = None
        self._channels: dict[str, Channel] = {}

    def channel(self, name: str) -> Channel:
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
        if self._connection is None:
            self._connection = _VolcanoCentrifugeConnection(
                self._client_factory(
                    self._address(),
                    token=self._client_context._session_token(),
                    get_token=self._token,
                )
            )
            await self._connection.connect()
        return self._connection

    async def disconnect(self) -> None:
        if self._connection is None:
            return
        await self._connection.disconnect()
        self._connection = None
        for channel in self._channels.values():
            channel._reset()
