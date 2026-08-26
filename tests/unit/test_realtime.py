from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any

from volcano_sdk import VolcanoClient


@dataclass(frozen=True)
class Response:
    status_code: int
    payload: Any
    content: bytes = b""
    headers: dict[str, str] | None = None


class AuthTransport:
    def __init__(self) -> None:
        self.access_token = "access-1"

    def auth_signin(self, **kwargs: Any) -> Response:
        del kwargs
        return Response(
            200,
            {
                "access_token": self.access_token,
                "refresh_token": "refresh-token",
                "user": {"id": "user-123"},
            },
        )


class FakeSubscription:
    def __init__(self, events: Any) -> None:
        self.events = events
        self.calls: list[tuple[str, Any]] = []

    async def subscribe(self) -> None:
        self.calls.append(("subscribe", None))

    async def publish(self, data: Any) -> None:
        self.calls.append(("publish", data))

    async def unsubscribe(self) -> None:
        self.calls.append(("unsubscribe", None))

    async def emit(self, data: Any) -> None:
        await self.events.on_publication(SimpleNamespace(pub=SimpleNamespace(data=data)))


class FakeCentrifugeClient:
    def __init__(self) -> None:
        self.calls: list[str] = []
        self.subscription: FakeSubscription | None = None
        self._subs: dict[str, FakeSubscription] = {}

    async def connect(self) -> None:
        self.calls.append("connect")

    async def disconnect(self) -> None:
        self.calls.append("disconnect")

    def new_subscription(self, name: str, *, events: Any) -> FakeSubscription:
        self.calls.append(f"channel:{name}")
        self.subscription = FakeSubscription(events)
        self._subs[name] = self.subscription
        return self.subscription

    async def emit_wire_publication(self, name: str, data: Any) -> None:
        subscription = self._subs.get(name)
        if subscription is not None:
            await subscription.emit(data)


def test_realtime_wraps_official_client_without_exposing_it() -> None:
    transport = AuthTransport()
    official = FakeCentrifugeClient()
    factory_arguments: dict[str, Any] = {}

    def factory(
        address: str,
        *,
        token: str,
        get_token: Callable[[], Awaitable[str]],
    ) -> FakeCentrifugeClient:
        factory_arguments.update(
            address=address,
            token=token,
            get_token=get_token,
        )
        return official

    client = VolcanoClient(
        api_url="https://api.test.volcano.dev",
        anon_key="anon key",
        _transport=transport,
        _realtime_client_factory=factory,
    )
    client.auth.sign_in(email="user@example.com", password="secret")
    received: list[dict[str, str]] = []

    async def scenario() -> None:
        channel = client.realtime.channel("contract")
        assert channel.on("message", received.append) is channel
        assert await channel.subscribe() is None
        assert official.subscription is not None
        await official.emit_wire_publication(
            "project-id:broadcast:contract",
            {"event": "message", "value": "contract"},
        )
        assert received == [{"event": "message", "value": "contract"}]
        assert await channel.send({"event": "message", "value": "contract"}) is None
        assert await channel.unsubscribe() is None

        transport.access_token = "access-2"
        client.auth.sign_in(email="user@example.com", password="secret")
        assert await factory_arguments["get_token"]() == "access-2"
        assert await client.realtime.disconnect() is None

    asyncio.run(scenario())

    assert factory_arguments["address"] == (
        "wss://api.test.volcano.dev/realtime/v1/websocket?apikey=anon%20key"
    )
    assert factory_arguments["token"] == "access-1"
    assert official.calls == ["connect", "channel:broadcast:contract", "disconnect"]
    assert official.subscription is not None
    assert official.subscription.calls == [
        ("subscribe", None),
        ("publish", {"event": "message", "value": "contract"}),
        ("unsubscribe", None),
    ]
    assert received == [{"event": "message", "value": "contract"}]
