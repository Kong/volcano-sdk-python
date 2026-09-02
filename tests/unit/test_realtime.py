from __future__ import annotations

import asyncio
import importlib
from dataclasses import dataclass
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, cast

import pytest

from volcano_sdk import VolcanoClient

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

UNEXPECTED_TRANSPORT_CALL = "unexpected transport operation"


def centrifuge_error(message: str) -> Exception:
    error_type = cast(
        "type[Exception]",
        importlib.import_module("centrifuge").CentrifugeError,
    )
    return error_type(message)


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
                "user": {"id": "user-123"},
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

    def query_database_insert(
        self,
        *,
        authorization: str,
        database_name: str,
        body: dict[str, Any],
    ) -> Response:
        del authorization, database_name, body
        raise AssertionError(UNEXPECTED_TRANSPORT_CALL)

    def query_database_update(
        self,
        *,
        authorization: str,
        database_name: str,
        body: dict[str, Any],
    ) -> Response:
        del authorization, database_name, body
        raise AssertionError(UNEXPECTED_TRANSPORT_CALL)

    def query_database_delete(
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
        byte_range: str | None = None,
    ) -> Response:
        del authorization, bucket_name, path, byte_range
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
    def __init__(self, name: str, events: Any) -> None:
        self.name = name
        self.events = events
        self.calls: list[tuple[str, Any]] = []
        self.unsubscribe_error: Exception | None = None
        self.unsubscribe_entered: asyncio.Event | None = None
        self.unsubscribe_release: asyncio.Event | None = None

    async def subscribe(self) -> None:
        self.calls.append(("subscribe", None))

    async def publish(self, data: Any) -> None:
        self.calls.append(("publish", data))

    async def unsubscribe(self) -> None:
        self.calls.append(("unsubscribe", None))
        if self.unsubscribe_entered is not None:
            self.unsubscribe_entered.set()
        if self.unsubscribe_release is not None:
            await self.unsubscribe_release.wait()
        if self.unsubscribe_error is not None:
            raise self.unsubscribe_error

    async def emit(self, data: Any) -> None:
        await self.events.on_publication(
            SimpleNamespace(pub=SimpleNamespace(data=data))
        )


class FakeCentrifugeClient:
    def __init__(self) -> None:
        self.calls: list[str] = []
        self.state = SimpleNamespace(value="disconnected")
        self.subscription: FakeSubscription | None = None
        self._subs: dict[str, FakeSubscription] = {}

    async def connect(self) -> None:
        self.calls.append("connect")
        self.state = SimpleNamespace(value="connected")

    async def disconnect(self) -> None:
        self.calls.append("disconnect")
        self.state = SimpleNamespace(value="disconnected")
        self._subs.clear()

    def new_subscription(self, name: str, *, events: Any) -> FakeSubscription:
        if name in self._subs:
            message = f"duplicate subscription: {name}"
            raise RuntimeError(message)
        self.calls.append(f"channel:{name}")
        self.subscription = FakeSubscription(name, events)
        self._subs[name] = self.subscription
        return self.subscription

    def remove_subscription(self, subscription: Any) -> None:
        name = next(
            name for name, candidate in self._subs.items() if candidate is subscription
        )
        del self._subs[name]

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


def test_realtime_channel_exposes_its_canonical_name() -> None:
    client = VolcanoClient(anon_key="anon-key", _transport=AuthTransport())

    assert client.realtime.channel("contract").name == "broadcast:contract"


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
        assert await factory_arguments["get_token"]() == "access-2"
        await client.realtime.disconnect()

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


def test_realtime_reports_connection_state_and_removes_one_channel() -> None:
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
        assert client.realtime.is_connected is False
        await channel.subscribe()
        assert client.realtime.is_connected is True

        await client.realtime.remove_channel("contract")

        assert official.subscription is not None
        assert official.subscription.calls[-1] == ("unsubscribe", None)
        replacement = client.realtime.channel("contract")
        assert replacement is not channel
        await replacement.subscribe()
        assert client.realtime.is_connected is True
        await client.realtime.remove_channel("missing")
        await client.realtime.disconnect()
        assert client.realtime.is_connected is False

    asyncio.run(scenario())


def test_realtime_connection_state_tracks_transport_disconnects() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        await client.realtime.channel("contract").subscribe()
        assert client.realtime.is_connected is True

        official.state = SimpleNamespace(value="connecting")

        assert client.realtime.is_connected is False
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_retains_channel_when_removal_fails() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        channel = client.realtime.channel("contract")
        await channel.subscribe()
        assert official.subscription is not None
        error = centrifuge_error("unsubscribe failed")
        official.subscription.unsubscribe_error = error

        with pytest.raises(type(error), match="unsubscribe failed"):
            await client.realtime.remove_channel("contract")

        assert client.realtime.channel("contract") is channel
        official.subscription.unsubscribe_error = None
        await client.realtime.remove_channel("contract")
        assert client.realtime.channel("contract") is not channel
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_continues_removing_channels_after_one_failure() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        first = client.realtime.channel("first")
        second = client.realtime.channel("second")
        await first.subscribe()
        await second.subscribe()
        error = centrifuge_error("unsubscribe failed")
        official._subs["broadcast:first"].unsubscribe_error = error

        with pytest.raises(type(error), match="unsubscribe failed"):
            await client.realtime.remove_all_channels()

        assert client.realtime.channel("first") is first
        assert client.realtime.channel("second") is not second
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_rejects_channel_lookup_during_removal() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        channel = client.realtime.channel("contract")
        await channel.subscribe()
        assert official.subscription is not None
        official.subscription.unsubscribe_entered = asyncio.Event()
        official.subscription.unsubscribe_release = asyncio.Event()
        removing = asyncio.create_task(client.realtime.remove_channel("contract"))
        await official.subscription.unsubscribe_entered.wait()

        with pytest.raises(RuntimeError, match="removal is in progress"):
            client.realtime.channel("contract")

        official.subscription.unsubscribe_release.set()
        await removing
        assert client.realtime.channel("contract") is not channel
        with pytest.raises(RuntimeError, match="no longer managed"):
            await channel.subscribe()
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_can_remove_all_channels_from_a_message_callback() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        removed = asyncio.Event()
        channel = client.realtime.channel("contract")

        async def remove_channels(_: Any) -> None:
            await client.realtime.remove_all_channels()
            removed.set()

        channel.on("message", remove_channels)
        await channel.subscribe()
        assert official.subscription is not None
        await official.subscription.emit({"event": "message"})

        await asyncio.wait_for(removed.wait(), timeout=0.2)
        replacement = client.realtime.channel("contract")
        assert replacement is not channel
        await replacement.subscribe()
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_removes_all_channels_without_disconnecting() -> None:
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
        second = client.realtime.channel("second")
        await first.subscribe()
        await second.subscribe()
        subscriptions = tuple(official._subs.values())

        await client.realtime.remove_all_channels()

        assert all(
            subscription.calls[-1] == ("unsubscribe", None)
            for subscription in subscriptions
        )
        assert client.realtime.channel("first") is not first
        assert client.realtime.channel("second") is not second
        assert client.realtime.is_connected is True
        await client.realtime.disconnect()

    asyncio.run(scenario())


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


def test_realtime_callback_failure_does_not_stop_later_callbacks() -> None:
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
        received: list[str] = []
        errors: list[dict[str, Any]] = []
        loop = asyncio.get_running_loop()
        previous_handler = loop.get_exception_handler()
        loop.set_exception_handler(lambda _loop, context: errors.append(context))

        def callback(data: dict[str, str]) -> None:
            if data["value"] == "first":
                message = "callback failed"
                raise RuntimeError(message)
            received.append(data["value"])

        try:
            channel.on("message", callback)
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

    asyncio.run(scenario())


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
        async def subscribe(self) -> None:
            entered.set()
            await release.wait()
            await super().subscribe()

    def new_subscription(name: str, *, events: Any) -> FakeSubscription:
        official.calls.append(f"channel:{name}")
        official.subscription = BlockingSubscription(name, events)
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
