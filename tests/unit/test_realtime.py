from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any

import pytest
from typing_extensions import override

from volcano_sdk import VolcanoClient

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

UNEXPECTED_TRANSPORT_CALL = "unexpected transport operation"


@dataclass(frozen=True)
class Response:
    status_code: int
    payload: Any
    content: bytes = b""
    headers: dict[str, str] | None = None


class AuthTransport:
    def __init__(self) -> None:
        self.access_token = "access-1"

    def auth_signin(
        self,
        *,
        authorization: str,
        email: str,
        password: str,
    ) -> Response:
        del authorization, email, password
        return Response(
            200,
            {
                "access_token": self.access_token,
                "refresh_token": "refresh-token",
                "user": {
                    "id": "user-123",
                    "email": "user@example.com",
                },
            },
        )

    def query_database_select(
        self,
        *,
        authorization: str,
        database_name: str,
        body: dict[str, Any],
    ) -> Response:
        del authorization, database_name, body
        raise AssertionError(UNEXPECTED_TRANSPORT_CALL)

    def upload_storage_object(
        self,
        *,
        authorization: str,
        bucket_name: str,
        path: str,
        data: bytes,
    ) -> Response:
        del authorization, bucket_name, path, data
        raise AssertionError(UNEXPECTED_TRANSPORT_CALL)

    def download_storage_object(
        self,
        *,
        authorization: str,
        bucket_name: str,
        path: str,
    ) -> Response:
        del authorization, bucket_name, path
        raise AssertionError(UNEXPECTED_TRANSPORT_CALL)

    def acquire_project_lock(
        self,
        *,
        authorization: str,
        key: str,
        ttl: int,
        token: str,
    ) -> Response:
        del authorization, key, ttl, token
        raise AssertionError(UNEXPECTED_TRANSPORT_CALL)

    def release_project_lock(
        self,
        *,
        authorization: str,
        key: str,
        token: str,
    ) -> Response:
        del authorization, key, token
        raise AssertionError(UNEXPECTED_TRANSPORT_CALL)


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
        await self.events.on_publication(
            SimpleNamespace(pub=SimpleNamespace(data=data))
        )


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


@dataclass(frozen=True)
class FakeCentrifugeFactory:
    client: FakeCentrifugeClient

    def __call__(
        self,
        address: str,
        *,
        token: str,
        get_token: Callable[[], Awaitable[str]],
    ) -> FakeCentrifugeClient:
        del address, token, get_token
        return self.client


@dataclass
class CapturingCentrifugeFactory:
    client: FakeCentrifugeClient
    address: str | None = field(default=None, init=False)
    token: str | None = field(default=None, init=False)
    get_token: Callable[[], Awaitable[str]] | None = field(default=None, init=False)

    def __call__(
        self,
        address: str,
        *,
        token: str,
        get_token: Callable[[], Awaitable[str]],
    ) -> FakeCentrifugeClient:
        self.address = address
        self.token = token
        self.get_token = get_token
        return self.client


async def _exercise_realtime_facade(
    client: VolcanoClient,
    official: FakeCentrifugeClient,
    transport: AuthTransport,
    received: list[dict[str, str]],
    factory: CapturingCentrifugeFactory,
) -> None:
    channel = client.realtime.channel("contract")
    assert channel.on("message", received.append) is channel
    await channel.subscribe()
    assert official.subscription is not None
    await official.emit_wire_publication(
        "project-id:broadcast:contract",
        {"event": "message", "value": "contract"},
    )
    for _ in range(10):
        if received:
            break
        await asyncio.sleep(0)
    assert received == [{"event": "message", "value": "contract"}]
    await channel.send({"event": "message", "value": "contract"})
    await channel.unsubscribe()
    transport.access_token = "access-2"
    client.auth.sign_in(email="user@example.com", password="secret")
    assert factory.get_token is not None
    assert await factory.get_token() == "access-2"
    await client.realtime.disconnect()


def test_realtime_wraps_official_client_without_exposing_it() -> None:
    transport = AuthTransport()
    official = FakeCentrifugeClient()
    factory = CapturingCentrifugeFactory(official)
    client = VolcanoClient(
        api_url="https://api.test.volcano.dev",
        anon_key="anon key",
        _transport=transport,
        _realtime_client_factory=factory,
    )
    client.auth.sign_in(email="user@example.com", password="secret")
    received: list[dict[str, str]] = []
    asyncio.run(
        _exercise_realtime_facade(client, official, transport, received, factory)
    )

    assert factory.address == (
        "wss://api.test.volcano.dev/realtime/v1/websocket?apikey=anon%20key"
    )
    assert factory.token == "access-1"
    assert official.calls == ["connect", "channel:broadcast:contract", "disconnect"]
    assert official.subscription is not None
    assert official.subscription.calls == [
        ("subscribe", None),
        ("publish", {"event": "message", "value": "contract"}),
        ("unsubscribe", None),
    ]
    assert received == [{"event": "message", "value": "contract"}]


def test_realtime_callbacks_run_outside_the_message_processor() -> None:
    transport = AuthTransport()
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=transport,
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        channel = client.realtime.channel("contract")
        started = asyncio.Event()
        release = asyncio.Event()

        async def callback(data: Any) -> None:
            del data
            started.set()
            await release.wait()

        channel.on("message", callback)
        await channel.subscribe()
        await asyncio.wait_for(
            official.emit_wire_publication(
                "broadcast:contract",
                {"event": "message"},
            ),
            timeout=0.1,
        )
        await asyncio.wait_for(started.wait(), timeout=0.1)
        release.set()
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_routes_overlapping_channel_suffixes_to_the_longest_match() -> None:
    transport = AuthTransport()
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=transport,
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        received: list[str] = []
        short = client.realtime.channel("foo").on(
            "message", lambda _data: received.append("short")
        )
        long = client.realtime.channel("x:broadcast:foo").on(
            "message", lambda _data: received.append("long")
        )
        await short.subscribe()
        await long.subscribe()
        await official.emit_wire_publication(
            "project-id:broadcast:x:broadcast:foo",
            {"event": "message"},
        )
        for _ in range(10):
            if received:
                break
            await asyncio.sleep(0)
        assert received == ["long"]
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_opens_one_connection_when_first_used_concurrently(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    transport = AuthTransport()
    official = FakeCentrifugeClient()
    entered = asyncio.Event()
    release = asyncio.Event()
    created = 0

    async def connect() -> None:
        entered.set()
        await release.wait()
        official.calls.append("connect")

    monkeypatch.setattr(official, "connect", connect)

    def factory(*args: Any, **kwargs: Any) -> FakeCentrifugeClient:
        nonlocal created
        del args, kwargs
        created += 1
        return official

    client = VolcanoClient(
        anon_key="anon-key",
        _transport=transport,
        _realtime_client_factory=factory,
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        first = asyncio.create_task(client.realtime._connect())
        await entered.wait()
        second = asyncio.create_task(client.realtime._connect())
        await asyncio.sleep(0)
        release.set()
        assert await first is await second
        assert created == 1
        await client.realtime.disconnect()

    asyncio.run(scenario())


@dataclass
class FailingFirstCallback:
    received: list[str]

    def __call__(self, data: dict[str, str]) -> None:
        if data["value"] == "first":
            message = "callback failed"
            raise RuntimeError(message)
        self.received.append(data["value"])


async def _exercise_callback_failure(
    client: VolcanoClient,
    official: FakeCentrifugeClient,
) -> None:
    channel = client.realtime.channel("contract")
    received: list[str] = []
    errors: list[dict[str, Any]] = []
    loop = asyncio.get_running_loop()
    previous_handler = loop.get_exception_handler()
    loop.set_exception_handler(lambda _loop, context: errors.append(context))
    try:
        channel.on("message", FailingFirstCallback(received))
        await channel.subscribe()
        await official.emit_wire_publication(
            "broadcast:contract",
            {"event": "message", "value": "first"},
        )
        await official.emit_wire_publication(
            "broadcast:contract",
            {"event": "message", "value": "second"},
        )
        for _ in range(10):
            if received:
                break
            await asyncio.sleep(0)
        assert received == ["second"]
        assert len(errors) == 1
        assert isinstance(errors[0].get("exception"), RuntimeError)
    finally:
        loop.set_exception_handler(previous_handler)
        await client.realtime.disconnect()


def test_realtime_callback_failure_does_not_stop_later_callbacks() -> None:
    transport = AuthTransport()
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=transport,
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")
    asyncio.run(_exercise_callback_failure(client, official))


def test_realtime_callback_can_disconnect_its_own_client() -> None:
    transport = AuthTransport()
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=transport,
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        channel = client.realtime.channel("contract")
        disconnected = asyncio.Event()

        async def callback(data: dict[str, str]) -> None:
            if data["value"] == "first":
                await client.realtime.disconnect()
                await channel.subscribe()
                await official.emit_wire_publication(
                    "broadcast:contract", {"event": "message", "value": "second"}
                )
            else:
                disconnected.set()

        channel.on("message", callback)
        await channel.subscribe()
        await official.emit_wire_publication(
            "broadcast:contract", {"event": "message", "value": "first"}
        )
        await asyncio.wait_for(disconnected.wait(), timeout=0.1)
        await client.realtime.disconnect()

    asyncio.run(scenario())
    assert official.calls == [
        "connect",
        "channel:broadcast:contract",
        "disconnect",
        "connect",
        "channel:broadcast:contract",
        "disconnect",
    ]


def test_realtime_disconnect_excludes_a_concurrent_first_connect(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    transport = AuthTransport()
    official = FakeCentrifugeClient()
    entered = asyncio.Event()
    release = asyncio.Event()

    async def connect() -> None:
        entered.set()
        await release.wait()
        official.calls.append("connect")

    monkeypatch.setattr(official, "connect", connect)
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=transport,
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        channel = client.realtime.channel("contract")
        subscribing = asyncio.create_task(channel.subscribe())
        await entered.wait()
        disconnecting = asyncio.create_task(client.realtime.disconnect())
        await asyncio.sleep(0)
        release.set()
        await subscribing
        await disconnecting
        assert channel._subscription is None

    asyncio.run(scenario())
    assert official.calls == ["connect", "channel:broadcast:contract", "disconnect"]


def test_realtime_disconnect_resets_channels_after_transport_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    transport = AuthTransport()
    first = FakeCentrifugeClient()
    second = FakeCentrifugeClient()
    clients = iter((first, second))

    async def failing_disconnect() -> None:
        first.calls.append("disconnect")
        message = "disconnect failed"
        raise RuntimeError(message)

    monkeypatch.setattr(first, "disconnect", failing_disconnect)

    def factory(*args: Any, **kwargs: Any) -> FakeCentrifugeClient:
        del args, kwargs
        return next(clients)

    client = VolcanoClient(
        anon_key="anon-key",
        _transport=transport,
        _realtime_client_factory=factory,
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        channel = client.realtime.channel("contract")
        await channel.subscribe()
        with pytest.raises(RuntimeError, match="disconnect failed"):
            await client.realtime.disconnect()

        assert channel._subscription is None
        await channel.subscribe()
        await client.realtime.disconnect()

    asyncio.run(scenario())
    assert first.calls == ["connect", "channel:broadcast:contract", "disconnect"]
    assert second.calls == ["connect", "channel:broadcast:contract", "disconnect"]


def test_realtime_disconnect_excludes_subscription_on_an_existing_connection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    transport = AuthTransport()
    official = FakeCentrifugeClient()
    entered = asyncio.Event()
    release = asyncio.Event()

    class BlockingSubscription(FakeSubscription):
        @override
        async def subscribe(self) -> None:
            entered.set()
            await release.wait()
            await super().subscribe()

    def new_subscription(name: str, *, events: Any) -> FakeSubscription:
        official.calls.append(f"channel:{name}")
        official.subscription = BlockingSubscription(events)
        official._subs[name] = official.subscription
        return official.subscription

    monkeypatch.setattr(official, "new_subscription", new_subscription)
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=transport,
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        await client.realtime._connect()
        channel = client.realtime.channel("contract")
        subscribing = asyncio.create_task(channel.subscribe())
        await entered.wait()
        disconnecting = asyncio.create_task(client.realtime.disconnect())
        await asyncio.sleep(0)
        assert "disconnect" not in official.calls
        release.set()
        await subscribing
        await disconnecting
        assert channel._subscription is None

    asyncio.run(scenario())
    assert official.calls == ["connect", "channel:broadcast:contract", "disconnect"]


def test_realtime_disconnect_snapshots_channels_before_resetting(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    transport = AuthTransport()
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=transport,
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        first = client.realtime.channel("first")
        await first.subscribe()
        entered = asyncio.Event()
        release = asyncio.Event()
        original_reset = first._reset

        async def blocking_reset() -> None:
            entered.set()
            await release.wait()
            await original_reset()

        monkeypatch.setattr(first, "_reset", blocking_reset)
        disconnecting = asyncio.create_task(client.realtime.disconnect())
        await entered.wait()
        second = client.realtime.channel("second")
        release.set()
        await disconnecting
        assert second._subscription is None

    asyncio.run(scenario())
