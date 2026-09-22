from __future__ import annotations

import asyncio
import base64
import importlib
import json
from dataclasses import dataclass
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, cast
from unittest.mock import AsyncMock, create_autospec

import pytest
from state_assertions import assert_same

from volcano_sdk import (
    AuthenticationError,
    PostgresChange,
    RealtimeConnectContext,
    RealtimeDisconnectContext,
    RealtimeErrorContext,
    RealtimePresenceInfo,
    Session,
    VolcanoClient,
)
from volcano_sdk import realtime as realtime_module

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

UNEXPECTED_TRANSPORT_CALL = "unexpected transport operation"


def centrifuge_error(message: str) -> Exception:
    error_type = cast(
        "type[Exception]",
        importlib.import_module("centrifuge").CentrifugeError,
    )
    return error_type(message)


def test_realtime_database_binding_can_be_replaced_and_cleared() -> None:
    client = VolcanoClient(anon_key="anon-key", _transport=AuthTransport())

    assert_same(client.realtime.database_name, expected=None)

    client.realtime.set_database_name("app")
    assert client.realtime.database_name == "app"

    client.realtime.set_database_name(None)
    assert_same(client.realtime.database_name, expected=None)


def test_realtime_fetches_session_bound_postgres_rows() -> None:
    transport = RealtimeDatabaseTransport([{"id": 42, "body": "fetched"}])
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    request = realtime_module._PostgresFetchRequest(
        database_name="app",
        access_token="captured-token",
        table="messages",
        row_id=42,
    )

    assert asyncio.run(client.realtime._fetch_postgres_rows((request,))) == (
        {"id": 42, "body": "fetched"},
    )
    assert transport.queries == [
        {
            "authorization": "captured-token",
            "database_name": "app",
            "body": {
                "table": "messages",
                "filters": [{"column": "id", "operator": "in", "value": [42]}],
                "limit": 1,
            },
        }
    ]


def test_realtime_row_fetch_returns_none_when_the_row_is_absent() -> None:
    transport = RealtimeDatabaseTransport([])
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    request = realtime_module._PostgresFetchRequest(
        database_name="app",
        access_token="captured-token",
        table="messages",
        row_id=42,
    )

    assert asyncio.run(client.realtime._fetch_postgres_rows((request,))) == (None,)
    assert transport.queries[0]["body"]["table"] == "messages"


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
        content_type: str = "application/octet-stream",
    ) -> Response:
        del authorization, bucket_name, path, data, content_type
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
        request_id: str | None = None,
    ) -> Response:
        del authorization, key, ttl, token, request_id
        raise AssertionError(UNEXPECTED_TRANSPORT_CALL)

    def release_project_lock(
        self,
        *,
        authorization: str,
        key: str,
        token: str,
        request_id: str | None = None,
    ) -> Response:
        del authorization, key, token, request_id
        raise AssertionError(UNEXPECTED_TRANSPORT_CALL)


class RealtimeDatabaseTransport(AuthTransport):
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        super().__init__()
        self.rows = rows
        self.queries: list[dict[str, Any]] = []

    def query_database_select(
        self,
        *,
        authorization: str,
        database_name: str,
        body: dict[str, Any],
    ) -> Response:
        self.queries.append(
            {
                "authorization": authorization,
                "database_name": database_name,
                "body": body,
            }
        )
        return Response(200, {"data": self.rows})

    async def query_database_select_async(
        self,
        *,
        authorization: str,
        database_name: str,
        body: dict[str, Any],
    ) -> Response:
        return self.query_database_select(
            authorization=authorization,
            database_name=database_name,
            body=body,
        )


class BlockingRealtimeDatabaseTransport(RealtimeDatabaseTransport):
    def __init__(self) -> None:
        super().__init__([{"id": 42, "body": "fetched"}])
        self.started = asyncio.Event()
        self.release = asyncio.Event()
        self.cancelled = asyncio.Event()

    async def query_database_select_async(
        self,
        *,
        authorization: str,
        database_name: str,
        body: dict[str, Any],
    ) -> Response:
        self.started.set()
        try:
            await self.release.wait()
        except asyncio.CancelledError:
            self.cancelled.set()
            raise
        return await super().query_database_select_async(
            authorization=authorization,
            database_name=database_name,
            body=body,
        )


class FakeSubscription:
    def __init__(
        self,
        name: str,
        events: Any,
        *,
        join_leave: bool,
        recoverable: bool,
    ) -> None:
        self.name = name
        self.events = events
        self.join_leave = join_leave
        self.recoverable = recoverable
        self.calls: list[tuple[str, Any]] = []
        self.presence_clients: dict[str, Any] = {}
        self.presence_error: Exception | None = None
        self.presence_entered: asyncio.Event | None = None
        self.presence_release: asyncio.Event | None = None
        self.inside_subscribed_handler = False
        self.subscribed = asyncio.Event()
        self.unsubscribe_error: Exception | None = None
        self.unsubscribe_entered: asyncio.Event | None = None
        self.unsubscribe_release: asyncio.Event | None = None

    async def subscribe(self) -> None:
        self.calls.append(("subscribe", None))
        await self.emit_subscribed()

    async def ready(self) -> None:
        await self.subscribed.wait()

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
        await self.events.on_unsubscribed(
            SimpleNamespace(code=0, reason="unsubscribe called")
        )

    async def presence(self) -> Any:
        if self.inside_subscribed_handler:
            message = "presence must run outside the subscription callback"
            raise AssertionError(message)
        self.calls.append(("presence", None))
        if self.presence_error is not None:
            raise self.presence_error
        clients = self.presence_clients.copy()
        if self.presence_entered is not None:
            self.presence_entered.set()
        if self.presence_release is not None:
            await self.presence_release.wait()
        return SimpleNamespace(clients=clients)

    async def emit_subscribed(self) -> None:
        self.subscribed.set()
        self.inside_subscribed_handler = True
        try:
            await self.events.on_subscribed(
                SimpleNamespace(
                    channel=self.name,
                    recoverable=self.recoverable,
                    positioned=False,
                    stream_position=None,
                    was_recovering=False,
                    recovered=False,
                    data=None,
                )
            )
        finally:
            self.inside_subscribed_handler = False

    async def emit_subscribing(self) -> None:
        self.subscribed.clear()
        await self.events.on_subscribing(SimpleNamespace(code=0, reason="reconnecting"))

    async def emit(self, data: Any) -> None:
        await self.events.on_publication(
            SimpleNamespace(pub=SimpleNamespace(data=data))
        )

    async def emit_join(self, info: Any) -> None:
        self.presence_clients[str(info.client)] = info
        await self.events.on_join(SimpleNamespace(info=info))

    async def emit_leave(self, info: Any) -> None:
        self.presence_clients.pop(str(info.client), None)
        await self.events.on_leave(SimpleNamespace(info=info))


class FakeCentrifugeClient:
    def __init__(self, events: Any = None) -> None:
        self.calls: list[str] = []
        self.events = events
        self.state = SimpleNamespace(value="disconnected")
        self.presence_clients: dict[str, Any] = {}
        self.presence_error: Exception | None = None
        self.presence_entered: asyncio.Event | None = None
        self.presence_release: asyncio.Event | None = None
        self.disconnect_probe: Callable[[], None] | None = None
        self.disconnect_error: Exception | None = None
        self.subscription: FakeSubscription | None = None
        self._subs: dict[str, FakeSubscription] = {}

    async def connect(self) -> None:
        self.calls.append("connect")
        self.state = SimpleNamespace(value="connected")
        if self.events is not None:
            await self.events.on_connected(SimpleNamespace(client="client-123"))

    async def disconnect(self) -> None:
        self.calls.append("disconnect")
        if self.disconnect_probe is not None:
            self.disconnect_probe()
        if self.disconnect_error is not None:
            raise self.disconnect_error
        self.state = SimpleNamespace(value="disconnected")
        self._subs.clear()
        if self.events is not None:
            await self.events.on_disconnected(
                SimpleNamespace(code=0, reason="disconnect called")
            )

    async def emit_error(self, code: int, error: Exception) -> None:
        if self.events is not None:
            await self.events.on_error(SimpleNamespace(code=code, error=error))

    def new_subscription(
        self,
        name: str,
        *,
        events: Any,
        join_leave: bool = False,
        recoverable: bool = False,
    ) -> FakeSubscription:
        if name in self._subs:
            message = f"duplicate subscription: {name}"
            raise RuntimeError(message)
        self.calls.append(f"channel:{name}")
        self.subscription = FakeSubscription(
            name,
            events,
            join_leave=join_leave,
            recoverable=recoverable,
        )
        self.subscription.presence_clients = self.presence_clients.copy()
        self.subscription.presence_error = self.presence_error
        self.subscription.presence_entered = self.presence_entered
        self.subscription.presence_release = self.presence_release
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


class BlockingConnectCentrifugeClient(FakeCentrifugeClient):
    def __init__(self) -> None:
        super().__init__()
        self.connect_started = asyncio.Event()
        self.connect_release = asyncio.Event()

    async def connect(self) -> None:
        self.calls.append("connect")
        self.connect_started.set()
        await self.connect_release.wait()
        self.state = SimpleNamespace(value="connected")
        if self.events is not None:
            await self.events.on_connected(SimpleNamespace(client="client-123"))


@dataclass(frozen=True)
class FakeCentrifugeFactory:
    client: FakeCentrifugeClient

    def __call__(
        self,
        address: str,
        *,
        events: Any,
        token: str,
        get_token: Callable[[], Awaitable[str]],
    ) -> FakeCentrifugeClient:
        del address, token, get_token
        self.client.events = events
        return self.client


class ControlledCentrifugeFactory:
    """Run native subscription logic with commands acknowledged by the test."""

    def __init__(self, monkeypatch: pytest.MonkeyPatch) -> None:
        centrifuge = importlib.import_module("centrifuge")
        self.client = centrifuge.Client(
            "ws://localhost/realtime/v1/websocket",
            loop=asyncio.get_running_loop(),
        )
        self.commands: asyncio.Queue[dict[str, Any]] = asyncio.Queue()

        def connect() -> None:
            self.client.state = centrifuge.ClientState.CONNECTED
            self.client._connected_future.set_result(True)

        def send_commands(commands: list[dict[str, Any]]) -> None:
            for command in commands:
                self.commands.put_nowait(command)

        monkeypatch.setattr(
            self.client,
            "connect",
            AsyncMock(spec_set=self.client.connect, side_effect=connect),
        )
        monkeypatch.setattr(
            self.client,
            "_send_commands",
            AsyncMock(spec_set=self.client._send_commands, side_effect=send_commands),
        )

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        del args
        self.client.events = kwargs["events"]
        return self.client

    async def command(self) -> dict[str, Any]:
        return await asyncio.wait_for(self.commands.get(), timeout=0.2)

    async def reply(self, command: dict[str, Any], **result: Any) -> None:
        await self.client._process_reply({"id": command["id"], **result})


@pytest.mark.parametrize("channel_type", ["broadcast", "presence"])
def test_realtime_native_dispatch_routes_project_prefixed_publications(
    monkeypatch: pytest.MonkeyPatch, channel_type: realtime_module.ChannelType
) -> None:
    async def scenario() -> None:
        factory = ControlledCentrifugeFactory(monkeypatch)
        client = VolcanoClient(
            anon_key="anon-key",
            _transport=AuthTransport(),
            _realtime_client_factory=factory,
        )
        client.auth.sign_in(email="user@example.com", password="secret")
        received: list[Any] = []
        channel = client.realtime.channel("room", channel_type=channel_type)
        channel.on("message", received.append)
        subscribing = asyncio.create_task(channel.subscribe())
        await factory.reply(await factory.command(), subscribe={})
        if channel_type == "presence":
            await factory.reply(await factory.command(), presence={"presence": {}})
        await subscribing
        payload = {"event": "message", "value": "contract"}
        try:
            # Enter native push dispatch, including its subscription lookup.
            await factory.client._process_reply(
                {
                    "push": {
                        "channel": f"project-id:{channel.name}",
                        "pub": {"data": payload},
                    }
                }
            )
            await channel._callback_queue.join()
            assert received == [payload]
        finally:
            await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_native_dispatch_routes_user_scoped_postgres_publications(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def scenario() -> None:
        factory = ControlledCentrifugeFactory(monkeypatch)
        client = VolcanoClient(
            anon_key="anon-key",
            _transport=AuthTransport(),
            _realtime_client_factory=factory,
        )
        client.auth.sign_in(email="user@example.com", password="secret")
        received: list[Any] = []
        delivered = asyncio.Event()

        def on_insert(change: Any) -> None:
            received.append(change)
            delivered.set()

        channel = client.realtime.channel("public:messages", channel_type="postgres")
        channel.on_postgres_changes(
            "INSERT", schema="public", table="messages", callback=on_insert
        )
        subscribing = asyncio.create_task(channel.subscribe())
        await factory.reply(await factory.command(), subscribe={})
        await subscribing
        payload = {
            "type": "INSERT",
            "schema": "public",
            "table": "messages",
            "record": {"id": 1, "body": "contract"},
            "timestamp": "2026-09-19T22:00:00Z",
        }
        try:
            await factory.client._process_reply(
                {
                    "push": {
                        "channel": "project-id:postgres:public:messages:user-id",
                        "pub": {"data": payload},
                    }
                }
            )
            await asyncio.wait_for(delivered.wait(), timeout=0.2)
            assert len(received) == 1
            assert received[0].record == payload["record"]
            assert received[0].type == "INSERT"
        finally:
            await client.realtime.disconnect()

    asyncio.run(scenario())


async def start_native_presence_refresh(
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[
    VolcanoClient,
    realtime_module.Channel,
    ControlledCentrifugeFactory,
    dict[str, Any],
]:
    factory = ControlledCentrifugeFactory(monkeypatch)
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=factory,
    )
    client.auth.sign_in(email="user@example.com", password="secret")
    channel = client.realtime.channel("lobby", channel_type="presence")
    subscribing = asyncio.create_task(channel.subscribe())
    command = await factory.command()
    await factory.reply(command, subscribe={})
    command = await factory.command()
    await factory.reply(command, presence={"presence": {}})
    await subscribing
    await channel._wait_presence_sync()
    subscription = factory.client.get_subscription(channel.name)
    await subscription._move_subscribing(1, "transport closed")
    command = await factory.command()
    await factory.reply(command, subscribe={})
    command = await factory.command()
    assert "presence" in command
    return client, channel, factory, command


@pytest.mark.parametrize("remove", [False, True])
@pytest.mark.parametrize("failed_reply", [False, True])
def test_realtime_stopped_presence_query_accepts_late_native_reply(
    monkeypatch: pytest.MonkeyPatch, *, remove: bool, failed_reply: bool
) -> None:
    async def scenario() -> None:
        client, channel, factory, presence = await start_native_presence_refresh(
            monkeypatch
        )
        healthy = client.realtime.channel("healthy")
        received = asyncio.Event()
        healthy.on("message", lambda _message: received.set())
        subscribing = asyncio.create_task(healthy.subscribe())
        command = await factory.command()
        await factory.reply(command, subscribe={})
        await subscribing
        stopping = asyncio.create_task(
            client.realtime.remove_channel("lobby", channel_type="presence")
            if remove
            else channel.unsubscribe()
        )
        command = await factory.command()
        assert "unsubscribe" in command
        try:
            if failed_reply:
                await factory.reply(
                    presence, error={"code": 100, "message": "presence unavailable"}
                )
            else:
                await factory.reply(
                    presence,
                    presence={
                        "presence": {"stale": {"client": "stale", "user": "peer"}}
                    },
                )
            await factory.reply(command, unsubscribe={})
            await stopping
            assert channel.get_presence_state() == {}
            await factory.client._process_reply(
                {"push": {"channel": healthy.name, "pub": {"data": "healthy"}}}
            )
            await asyncio.wait_for(received.wait(), timeout=0.2)
        finally:
            # Let a failed assertion finish the unsubscribe before closing the client.
            if not stopping.done():
                await factory.reply(command, unsubscribe={})
            await asyncio.gather(stopping, return_exceptions=True)
            await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_disconnect_settles_pending_native_presence_query(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def scenario() -> None:
        client, channel, factory, _presence = await start_native_presence_refresh(
            monkeypatch
        )
        await client.realtime.disconnect()
        assert channel.get_presence_state() == {}
        assert not factory.client._inflight_commands

    asyncio.run(scenario())


def test_realtime_cancelled_pause_keeps_native_subscription_resumable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def scenario() -> None:
        client, channel, factory, presence = await start_native_presence_refresh(
            monkeypatch
        )
        subscription = factory.client.get_subscription(channel.name)
        pausing = asyncio.create_task(channel.unsubscribe())
        await asyncio.sleep(0)
        pausing.cancel()
        await factory.reply(await factory.command(), unsubscribe={})
        with pytest.raises(asyncio.CancelledError):
            await pausing
        await factory.reply(presence, presence={"presence": {}})
        assert subscription.state.value == "unsubscribed"
        assert_same(channel._subscribed, expected=False)

        resuming = asyncio.create_task(channel.subscribe())
        try:
            command = await factory.command()
            assert "subscribe" in command
            await factory.reply(command, subscribe={})
            command = await factory.command()
            await factory.reply(command, presence={"presence": {}})
            await resuming
            await channel._wait_presence_sync()
            assert_same(channel._subscribed, expected=True)
            assert factory.client.get_subscription(channel.name) is subscription
        finally:
            await client.realtime.disconnect()
            await asyncio.gather(resuming, return_exceptions=True)

    asyncio.run(scenario())


def test_realtime_repeated_pause_retains_presence_clear_notification(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def scenario() -> None:
        client, channel, factory, presence = await start_native_presence_refresh(
            monkeypatch
        )
        entered, release = asyncio.Event(), asyncio.Event()
        snapshots: list[Any] = []

        async def receive(state: Any) -> None:
            snapshots.append(state)
            if state:
                entered.set()
                await release.wait()

        channel.on_presence_sync(receive)
        await factory.reply(
            presence,
            presence={"presence": {"peer": {"client": "peer", "user": "peer"}}},
        )
        await asyncio.wait_for(entered.wait(), timeout=0.2)
        try:
            pausing = asyncio.create_task(channel.unsubscribe())
            command = await factory.command()
            await factory.reply(command, unsubscribe={})
            await pausing
            await channel.unsubscribe()
            release.set()
            await asyncio.wait_for(channel._callback_queue.join(), timeout=0.2)
            assert snapshots[-1] == {}
            assert channel.get_presence_state() == {}
        finally:
            release.set()
            await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_channel_exposes_its_canonical_name() -> None:
    client = VolcanoClient(anon_key="anon-key", _transport=AuthTransport())

    assert client.realtime.channel("contract").name == "broadcast:contract"
    assert (
        client.realtime.channel("contract", channel_type="presence").name
        == "presence:contract"
    )
    assert (
        client.realtime.channel(
            "public:messages",
            channel_type="postgres",
        ).name
        == "postgres:public:messages"
    )


def test_realtime_reuses_channels_with_the_same_auto_fetch_setting() -> None:
    client = VolcanoClient(anon_key="anon-key", _transport=AuthTransport())

    enabled = client.realtime.channel(
        "public:messages",
        channel_type="postgres",
    )
    disabled = client.realtime.channel(
        "public:archive",
        channel_type="postgres",
        auto_fetch=False,
    )

    assert (
        client.realtime.channel(
            "public:messages",
            channel_type="postgres",
            auto_fetch=True,
        )
        is enabled
    )
    assert (
        client.realtime.channel(
            "public:archive",
            channel_type="postgres",
            auto_fetch=False,
        )
        is disabled
    )


def test_realtime_reuses_channels_with_the_same_fetch_configuration() -> None:
    client = VolcanoClient(anon_key="anon-key", _transport=AuthTransport())
    channel = client.realtime.channel(
        "public:messages",
        channel_type="postgres",
        fetch_batch_window_ms=10,
        fetch_max_batch_size=25,
    )

    assert (
        client.realtime.channel(
            "public:messages",
            channel_type="postgres",
            fetch_batch_window_ms=10,
            fetch_max_batch_size=25,
        )
        is channel
    )


def test_realtime_rejects_conflicting_channel_fetch_configuration() -> None:
    client = VolcanoClient(anon_key="anon-key", _transport=AuthTransport())
    client.realtime.channel(
        "public:messages",
        channel_type="postgres",
        auto_fetch=False,
    )

    with pytest.raises(ValueError, match="fetch configuration"):
        client.realtime.channel(
            "public:messages",
            channel_type="postgres",
            auto_fetch=True,
        )


@pytest.mark.parametrize(
    ("options", "message"),
    [
        ({"fetch_batch_window_ms": True}, "fetch_batch_window_ms"),
        ({"fetch_batch_window_ms": 0}, "fetch_batch_window_ms"),
        ({"fetch_batch_window_ms": 1.5}, "fetch_batch_window_ms"),
        ({"fetch_max_batch_size": True}, "fetch_max_batch_size"),
        ({"fetch_max_batch_size": 0}, "fetch_max_batch_size"),
        ({"fetch_max_batch_size": 129}, "fetch_max_batch_size"),
    ],
)
def test_realtime_rejects_invalid_channel_fetch_configuration(
    options: dict[str, Any],
    message: str,
) -> None:
    client = VolcanoClient(anon_key="anon-key", _transport=AuthTransport())

    with pytest.raises(ValueError, match=message):
        client.realtime.channel(
            "public:messages",
            channel_type="postgres",
            **options,
        )


def test_realtime_postgres_delivery_identity_changes_on_reauthentication() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        channel = client.realtime.channel(
            "public:messages",
            channel_type="postgres",
        )
        await channel.subscribe()
        identity = channel._capture_postgres_delivery_identity()

        assert channel._postgres_delivery_is_current(identity)

        client.auth.sign_in(email="user@example.com", password="secret")

        identity_after_reauthentication = channel._capture_postgres_delivery_identity()
        assert not channel._postgres_delivery_is_current(identity)
        assert not channel._postgres_delivery_is_current(
            identity_after_reauthentication
        )
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_postgres_delivery_identity_changes_on_resubscription() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        channel = client.realtime.channel(
            "public:messages",
            channel_type="postgres",
        )
        await channel.subscribe()
        identity = channel._capture_postgres_delivery_identity()
        subscription = official.subscription
        assert subscription is not None

        await subscription.emit_subscribing()
        assert not channel._postgres_delivery_is_current(identity)

        await subscription.emit_subscribed()
        next_identity = channel._capture_postgres_delivery_identity()

        assert not channel._postgres_delivery_is_current(identity)
        assert channel._postgres_delivery_is_current(next_identity)
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_rejects_new_subscriptions_after_session_changes() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        broadcast = client.realtime.channel("updates")
        await broadcast.subscribe()

        client.auth.sign_in(email="user@example.com", password="secret")
        postgres = client.realtime.channel(
            "public:messages",
            channel_type="postgres",
        )

        with pytest.raises(RuntimeError, match="session changed"):
            await postgres.subscribe()
        assert postgres._subscription is None
        await client.realtime.disconnect()

    asyncio.run(scenario())


async def test_realtime_drops_queued_postgres_callbacks_from_an_old_epoch() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    def insert(record_id: int) -> dict[str, Any]:
        return {
            "type": "INSERT",
            "schema": "public",
            "table": "messages",
            "record": {"id": record_id},
            "timestamp": "2026-09-03T12:00:00Z",
        }

    received: list[int] = []
    first_started = asyncio.Event()
    release_first = asyncio.Event()
    third_received = asyncio.Event()
    channel = client.realtime.channel(
        "public:messages",
        channel_type="postgres",
    )

    async def on_insert(change: Any) -> None:
        record_id = change.record["id"]
        if record_id == 1:
            first_started.set()
            await release_first.wait()
        received.append(record_id)
        if record_id == 3:
            third_received.set()

    channel.on_postgres_changes(
        "INSERT",
        schema="public",
        table="messages",
        callback=on_insert,
    )
    await channel.subscribe()
    subscription = official.subscription
    assert subscription is not None

    await subscription.emit(insert(1))
    await first_started.wait()
    first_worker = channel._postgres_worker
    assert first_worker is not None
    await subscription.emit(insert(2))

    await subscription.emit_subscribing()
    assert_same(channel._postgres_worker, expected=None)
    release_first.set()
    await subscription.emit_subscribed()
    await subscription.emit(insert(3))
    await asyncio.wait_for(third_received.wait(), timeout=0.2)

    assert received == [1, 3]
    assert channel._postgres_worker is not first_worker
    await client.realtime.disconnect()


def test_realtime_only_queues_changes_with_an_interested_listener() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        @dataclass
        class UnhashableListener:
            changes: list[Any]
            received: asyncio.Event

            def __call__(self, change: Any) -> None:
                self.changes.append(change)
                self.received.set()

        def publication(event: str, table: str) -> dict[str, Any]:
            return {
                "type": event,
                "schema": "public",
                "table": table,
                "record": {"id": 1},
                "timestamp": "2026-09-03T12:00:00Z",
            }

        filtered: list[Any] = []
        unfiltered: list[Any] = []
        unfiltered_received = asyncio.Event()
        channel = client.realtime.channel(
            "public:messages",
            channel_type="postgres",
        )
        stop = channel.on_postgres_changes(
            "INSERT",
            schema="public",
            table="messages",
            callback=filtered.append,
        )
        await channel.subscribe()
        subscription = official.subscription
        assert subscription is not None

        await subscription.emit(publication("UPDATE", "messages"))
        await subscription.emit(publication("INSERT", "other"))

        assert_same(channel._postgres_worker, expected=None)

        stop()
        await subscription.emit(publication("INSERT", "messages"))

        assert_same(channel._postgres_worker, expected=None)

        channel.on("*", UnhashableListener(unfiltered, unfiltered_received))
        await subscription.emit(publication("UPDATE", "other"))
        await asyncio.wait_for(unfiltered_received.wait(), timeout=0.2)

        assert filtered == []
        assert len(unfiltered) == 1
        assert channel._postgres_worker is not None
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_captures_supported_postgres_fetch_request() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")
    client.realtime.set_database_name("app")

    async def scenario() -> None:
        channel = client.realtime.channel(
            "public:messages",
            channel_type="postgres",
        )
        await channel.subscribe()
        change = realtime_module.PostgresChange(
            type="INSERT",
            schema="public",
            table="messages",
            id=42,
            mode="lightweight",
        )

        request = channel._postgres_fetch_request(change)
        client.realtime.set_database_name("next")

        assert request == realtime_module._PostgresFetchRequest(
            database_name="app",
            access_token="access-1",
            table="messages",
            row_id=42,
        )
        assert channel._postgres_fetch_request(
            realtime_module.PostgresChange(
                type="INSERT",
                schema="private",
                table="messages",
                id=42,
                mode="lightweight",
            )
        ) == realtime_module._PostgresFetchRequest(
            database_name="next",
            access_token="access-1",
            table="private.messages",
            row_id=42,
        )
        assert (
            channel._postgres_fetch_request(
                realtime_module.PostgresChange(
                    type="DELETE",
                    schema="public",
                    table="messages",
                    id=42,
                    mode="lightweight",
                )
            )
            is None
        )
        assert (
            channel._postgres_fetch_request(
                realtime_module.PostgresChange(
                    type="UPDATE",
                    schema="public",
                    table="messages",
                    record={"id": 42},
                )
            )
            is None
        )
        client.realtime.set_database_name(None)
        assert channel._postgres_fetch_request(change) is None
        await client.realtime.disconnect()

    asyncio.run(scenario())


@pytest.mark.parametrize("schema", ["public", "private"])
def test_realtime_fetches_lightweight_postgres_rows(schema: str) -> None:
    official = FakeCentrifugeClient()
    transport = RealtimeDatabaseTransport([{"id": 42, "body": "fetched"}])
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=transport,
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")
    client.realtime.set_database_name("app")

    async def scenario() -> None:
        changes: list[Any] = []
        received = asyncio.Event()
        channel = client.realtime.channel(
            f"{schema}:messages",
            channel_type="postgres",
        )

        def on_insert(change: Any) -> None:
            changes.append(change)
            received.set()

        channel.on_postgres_changes(
            "INSERT",
            schema=schema,
            table="messages",
            callback=on_insert,
        )
        await channel.subscribe()
        subscription = official.subscription
        assert subscription is not None

        await subscription.emit(
            {
                "type": "INSERT",
                "schema": schema,
                "table": "messages",
                "id": 42,
                "mode": "lightweight",
                "timestamp": "2026-09-03T12:00:00Z",
            }
        )
        await asyncio.wait_for(received.wait(), timeout=0.2)

        assert changes[0].record == {"id": 42, "body": "fetched"}
        assert changes[0].id is None
        assert changes[0].mode is None
        assert transport.queries == [
            {
                "authorization": "access-1",
                "database_name": "app",
                "body": {
                    "table": "messages" if schema == "public" else f"{schema}.messages",
                    "filters": [{"column": "id", "operator": "in", "value": [42]}],
                    "limit": 1,
                },
            }
        ]
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_batches_compatible_lightweight_postgres_rows() -> None:
    official = FakeCentrifugeClient()
    transport = RealtimeDatabaseTransport(
        [
            {"id": 42, "body": "first"},
            {"id": 43, "body": "second"},
        ]
    )
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=transport,
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")
    client.realtime.set_database_name("app")

    async def scenario() -> None:
        changes: list[Any] = []
        received = asyncio.Event()
        channel = client.realtime.channel(
            "public:messages",
            channel_type="postgres",
        )

        def on_insert(change: Any) -> None:
            changes.append(change)
            if len(changes) == 2:
                received.set()

        channel.on_postgres_changes(
            "INSERT",
            schema="public",
            table="messages",
            callback=on_insert,
        )
        await channel.subscribe()
        subscription = official.subscription
        assert subscription is not None
        assert subscription.recoverable is False

        for row_id in (42, 43):
            await subscription.emit(
                {
                    "type": "INSERT",
                    "schema": "public",
                    "table": "messages",
                    "id": row_id,
                    "mode": "lightweight",
                    "timestamp": "2026-09-03T12:00:00Z",
                }
            )
        await asyncio.wait_for(received.wait(), timeout=0.2)

        assert [change.record for change in changes] == [
            {"id": 42, "body": "first"},
            {"id": 43, "body": "second"},
        ]
        assert transport.queries == [
            {
                "authorization": "access-1",
                "database_name": "app",
                "body": {
                    "table": "messages",
                    "filters": [
                        {
                            "column": "id",
                            "operator": "in",
                            "value": [42, 43],
                        }
                    ],
                    "limit": 2,
                },
            }
        ]
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_honors_channel_fetch_max_batch_size() -> None:
    official = FakeCentrifugeClient()
    transport = RealtimeDatabaseTransport(
        [
            {"id": 42, "body": "first"},
            {"id": 43, "body": "second"},
        ]
    )
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=transport,
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")
    client.realtime.set_database_name("app")

    async def scenario() -> None:
        changes: list[Any] = []
        received = asyncio.Event()
        channel = client.realtime.channel(
            "public:messages",
            channel_type="postgres",
            fetch_max_batch_size=1,
        )

        def on_insert(change: Any) -> None:
            changes.append(change)
            if len(changes) == 2:
                received.set()

        channel.on_postgres_changes(
            "INSERT",
            schema="public",
            table="messages",
            callback=on_insert,
        )
        await channel.subscribe()
        subscription = official.subscription
        assert subscription is not None

        for row_id in (42, 43):
            await subscription.emit(
                {
                    "type": "INSERT",
                    "schema": "public",
                    "table": "messages",
                    "id": row_id,
                    "mode": "lightweight",
                    "timestamp": "2026-09-03T12:00:00Z",
                }
            )
        await asyncio.wait_for(received.wait(), timeout=0.2)

        query_ids = [
            query["body"]["filters"][0]["value"] for query in transport.queries
        ]
        assert query_ids == [[42], [43]]
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_can_disable_lightweight_postgres_row_fetching() -> None:
    official = FakeCentrifugeClient()
    transport = RealtimeDatabaseTransport([{"id": 42, "body": "fetched"}])
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=transport,
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")
    client.realtime.set_database_name("app")

    async def scenario() -> None:
        changes: list[Any] = []
        received = asyncio.Event()
        channel = client.realtime.channel(
            "public:messages",
            channel_type="postgres",
            auto_fetch=False,
        )

        def on_insert(change: Any) -> None:
            changes.append(change)
            received.set()

        channel.on_postgres_changes(
            "INSERT",
            schema="public",
            table="messages",
            callback=on_insert,
        )
        await channel.subscribe()
        subscription = official.subscription
        assert subscription is not None

        await subscription.emit(
            {
                "type": "INSERT",
                "schema": "public",
                "table": "messages",
                "id": 42,
                "mode": "lightweight",
                "timestamp": "2026-09-03T12:00:00Z",
            }
        )
        await asyncio.wait_for(received.wait(), timeout=0.2)

        assert changes[0].record is None
        assert changes[0].id == 42
        assert changes[0].mode == "lightweight"
        assert transport.queries == []
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_delivers_lightweight_fallback_when_row_is_absent() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=RealtimeDatabaseTransport([]),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")
    client.realtime.set_database_name("app")

    async def scenario() -> None:
        changes: list[Any] = []
        errors: list[dict[str, Any]] = []
        received = asyncio.Event()
        asyncio.get_running_loop().set_exception_handler(
            lambda _loop, context: errors.append(context)
        )
        channel = client.realtime.channel(
            "public:messages",
            channel_type="postgres",
        )

        def on_update(change: Any) -> None:
            changes.append(change)
            received.set()

        channel.on_postgres_changes(
            "UPDATE",
            schema="public",
            table="messages",
            callback=on_update,
        )
        await channel.subscribe()
        subscription = official.subscription
        assert subscription is not None

        await subscription.emit(
            {
                "type": "UPDATE",
                "schema": "public",
                "table": "messages",
                "id": 404,
                "mode": "lightweight",
                "timestamp": "2026-09-03T12:00:00Z",
            }
        )
        await asyncio.wait_for(received.wait(), timeout=0.2)

        assert changes[0].record is None
        assert changes[0].id == 404
        assert changes[0].mode == "lightweight"
        assert errors[0]["message"] == "Volcano realtime Postgres row fetch failed"
        assert isinstance(errors[0]["exception"], LookupError)
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_unsubscribe_does_not_wait_for_obsolete_row_fetches() -> None:
    official = FakeCentrifugeClient()
    transport = BlockingRealtimeDatabaseTransport()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=transport,
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")
    client.realtime.set_database_name("app")

    async def scenario() -> None:
        channel = client.realtime.channel(
            "public:messages",
            channel_type="postgres",
        )
        channel.on_postgres_changes(
            "INSERT",
            schema="public",
            table="messages",
            callback=lambda _change: None,
        )
        await channel.subscribe()
        subscription = official.subscription
        assert subscription is not None

        await subscription.emit(
            {
                "type": "INSERT",
                "schema": "public",
                "table": "messages",
                "id": 42,
                "mode": "lightweight",
                "timestamp": "2026-09-03T12:00:00Z",
            }
        )
        await asyncio.wait_for(transport.started.wait(), timeout=0.2)

        await asyncio.wait_for(channel.unsubscribe(), timeout=0.2)
        assert transport.cancelled.is_set()
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_disconnect_invalidates_channels_before_clearing_auth() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        channel = client.realtime.channel(
            "public:messages",
            channel_type="postgres",
        )
        await channel.subscribe()
        observed = False

        def observe_disconnect_boundary() -> None:
            nonlocal observed
            assert_same(channel._subscribed, expected=False)
            assert client.realtime._connection_token() == "access-1"
            observed = True

        official.disconnect_probe = observe_disconnect_boundary
        await client.realtime.disconnect()

        assert observed
        with pytest.raises(RuntimeError, match="no session binding"):
            client.realtime._connection_token()

    asyncio.run(scenario())


def test_realtime_routes_immutable_rls_scoped_postgres_changes() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        updates: list[Any] = []
        inserts: list[Any] = []
        received = asyncio.Event()

        def on_update(change: Any) -> None:
            updates.append(change)
            received.set()

        channel = client.realtime.channel(
            "public:messages",
            channel_type="postgres",
        )
        channel.on_postgres_changes(
            "UPDATE",
            schema="public",
            table="messages",
            callback=on_update,
        )
        channel.on_postgres_changes(
            "INSERT",
            schema="public",
            table="messages",
            callback=inserts.append,
        )
        await channel.subscribe()
        await official.emit_wire_publication(
            "project-id:postgres:public:messages:user-id",
            {
                "type": "UPDATE",
                "schema": "public",
                "table": "messages",
                "record": {"id": 1, "body": "updated"},
                "old_record": {"id": 1, "body": "old"},
                "columns": ["body"],
                "timestamp": "2026-09-02T12:00:00Z",
            },
        )
        await asyncio.wait_for(received.wait(), timeout=0.1)

        change = updates[0]
        assert change.type == "UPDATE"
        assert change.schema == "public"
        assert change.table == "messages"
        assert change.record == {"id": 1, "body": "updated"}
        assert change.old_record == {"id": 1, "body": "old"}
        assert change.columns == ("body",)
        assert change.timestamp == "2026-09-02T12:00:00Z"
        assert inserts == []
        with pytest.raises(TypeError):
            cast("dict[str, Any]", change.record)["body"] = "mutated"

        await official.emit_wire_publication(
            "project-id:postgres:public:messages:extra:user-id",
            {
                "type": "UPDATE",
                "schema": "public",
                "table": "messages",
                "timestamp": "2026-09-02T12:01:00Z",
            },
        )
        await asyncio.sleep(0)
        assert len(updates) == 1
        await client.realtime.disconnect()

    asyncio.run(scenario())


@pytest.mark.parametrize("field", ["record", "old_record"])
@pytest.mark.parametrize("invalid", ["invalid", 0, False, []])
async def test_realtime_drops_malformed_records_before_delivering_valid_changes(
    field: str,
    invalid: object,
) -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")
    changes: list[PostgresChange] = []
    received = asyncio.Event()

    def on_change(change: PostgresChange) -> None:
        changes.append(change)
        if change.record == {"id": "valid"}:
            received.set()

    channel = client.realtime.channel("public:messages", channel_type="postgres")
    channel.on_postgres_changes(
        "*", schema="public", table="messages", callback=on_change
    )
    payload: dict[str, object] = {
        "type": "UPDATE",
        "schema": "public",
        "table": "messages",
        "record": {"id": "valid"},
        "timestamp": "2026-09-02T12:00:00Z",
    }
    wire_channel = "project-id:postgres:public:messages:user-id"
    invalid_payload = {**payload, "record": {"id": "invalid"}, field: invalid}
    try:
        await channel.subscribe()
        await official.emit_wire_publication(wire_channel, invalid_payload)
        await official.emit_wire_publication(wire_channel, payload)
        await asyncio.wait_for(received.wait(), timeout=1)
        assert len(changes) == 1
        assert changes[0].record == {"id": "valid"}
    finally:
        await client.realtime.disconnect()


def test_realtime_preserves_lightweight_postgres_metadata() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        changes: list[Any] = []
        received = asyncio.Event()

        def on_insert(change: Any) -> None:
            changes.append(change)
            received.set()

        channel = client.realtime.channel(
            "public:messages",
            channel_type="postgres",
        )
        channel.on_postgres_changes(
            "INSERT",
            schema="public",
            table="messages",
            callback=on_insert,
        )
        await channel.subscribe()
        await official.emit_wire_publication(
            "project-id:postgres:public:messages:user-id",
            {
                "type": "INSERT",
                "schema": "public",
                "table": "messages",
                "id": 42,
                "mode": "lightweight",
                "timestamp": "2026-09-02T12:00:00Z",
            },
        )
        await asyncio.wait_for(received.wait(), timeout=0.1)

        assert changes[0].id == 42
        assert changes[0].mode == "lightweight"
        assert changes[0].record is None
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_normalizes_lightweight_postgres_deletes() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        changes: list[Any] = []
        received = asyncio.Event()
        channel = client.realtime.channel(
            "public:messages",
            channel_type="postgres",
        )

        def on_delete(change: Any) -> None:
            changes.append(change)
            if len(changes) == 2:
                received.set()

        channel.on_postgres_changes(
            "DELETE",
            schema="public",
            table="messages",
            callback=on_delete,
        )
        await channel.subscribe()
        common = {
            "type": "DELETE",
            "schema": "public",
            "table": "messages",
            "mode": "lightweight",
            "timestamp": "2026-09-03T12:00:00Z",
        }
        await official.emit_wire_publication(
            "project-id:postgres:public:messages:user-id",
            {**common, "id": 42},
        )
        await official.emit_wire_publication(
            "project-id:postgres:public:messages:user-id",
            {**common, "id": 43, "old_record": {"id": 43, "body": "old"}},
        )
        await asyncio.wait_for(received.wait(), timeout=0.1)

        assert changes[0].old_record == {"id": 42}
        assert changes[1].old_record == {"id": 43, "body": "old"}
        assert all(change.id is None for change in changes)
        assert all(change.mode is None for change in changes)
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_validates_postgres_change_operations() -> None:
    client = VolcanoClient(anon_key="anon-key", _transport=AuthTransport())
    broadcast = client.realtime.channel("contract")
    postgres = client.realtime.channel(
        "public:messages",
        channel_type="postgres",
    )

    with pytest.raises(ValueError, match="only available for postgres"):
        broadcast.on_postgres_changes(
            "*",
            schema="public",
            table="messages",
            callback=lambda _change: None,
        )
    with pytest.raises(ValueError, match="unsupported Postgres change event"):
        postgres.on_postgres_changes(
            "UPSERT",  # type: ignore[arg-type]
            schema="public",
            table="messages",
            callback=lambda _change: None,
        )

    async def send() -> None:
        with pytest.raises(ValueError, match="only available for broadcast"):
            await postgres.send({"body": "not allowed"})

    asyncio.run(send())


def test_realtime_presence_sync_tracks_initial_join_and_leave_state() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        channel = client.realtime.channel("lobby", channel_type="presence")
        sync_states: list[Any] = []
        joins: list[RealtimePresenceInfo] = []
        leaves: list[RealtimePresenceInfo] = []
        synced = asyncio.Event()

        def on_sync(state: Any) -> None:
            sync_states.append(state)
            synced.set()

        stop_sync = channel.on_presence_sync(on_sync)
        channel.on("join", joins.append)
        channel.on("leave", leaves.append)

        official.presence_clients = {
            "alice-client": SimpleNamespace(
                client="alice-client",
                user="alice",
                conn_info={"display_name": "Alice"},
            )
        }
        await channel.subscribe()
        assert official.subscription is not None
        await asyncio.wait_for(synced.wait(), timeout=0.1)
        assert channel.get_presence_state() == {
            "alice-client": RealtimePresenceInfo(
                client="alice-client",
                user="alice",
                data={"display_name": "Alice"},
            )
        }
        assert official.subscription.join_leave is True
        assert official.subscription.recoverable is True

        synced.clear()
        bob = SimpleNamespace(
            client="bob-client",
            user="bob",
            conn_info={"display_name": "Bob"},
        )
        await official.subscription.emit_join(bob)
        await asyncio.wait_for(synced.wait(), timeout=0.1)
        assert joins == [
            RealtimePresenceInfo(
                client="bob-client",
                user="bob",
                data={"display_name": "Bob"},
            )
        ]
        assert set(channel.get_presence_state()) == {
            "alice-client",
            "bob-client",
        }

        synced.clear()
        await official.subscription.emit_leave(bob)
        await asyncio.wait_for(synced.wait(), timeout=0.1)
        assert leaves == joins
        assert set(channel.get_presence_state()) == {"alice-client"}

        stop_sync()
        stop_sync()
        await client.realtime.remove_channel("lobby", channel_type="presence")
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_presence_subscribe_waits_for_initial_roster() -> None:
    official = FakeCentrifugeClient()
    presence_entered = asyncio.Event()
    presence_release = asyncio.Event()
    official.presence_entered = presence_entered
    official.presence_release = presence_release
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        channel = client.realtime.channel("lobby", channel_type="presence")
        subscribing = asyncio.create_task(channel.subscribe())
        await presence_entered.wait()
        assert not subscribing.done()

        presence_release.set()
        await subscribing
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_presence_resyncs_after_resubscription() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        channel = client.realtime.channel("lobby", channel_type="presence")
        await channel.subscribe()
        assert official.subscription is not None
        official.subscription.presence_clients = {
            "carol-client": SimpleNamespace(
                client="carol-client",
                user="carol",
                conn_info={"display_name": "Carol"},
            )
        }
        official.subscription.presence_entered = asyncio.Event()

        await official.subscription.emit_subscribed()
        await official.subscription.presence_entered.wait()
        await asyncio.wait_for(channel._wait_presence_sync(), timeout=0.2)

        assert set(channel.get_presence_state()) == {"carol-client"}
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_presence_clears_while_resubscribing() -> None:
    official = FakeCentrifugeClient()
    official.presence_clients = {
        "alice-client": SimpleNamespace(
            client="alice-client", user="alice", conn_info={}
        )
    }
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        channel = client.realtime.channel("lobby", channel_type="presence")
        await channel.subscribe()
        assert channel.get_presence_state()
        assert official.subscription is not None

        await official.subscription.emit_subscribing()

        assert channel.get_presence_state() == {}
        with pytest.raises(RuntimeError, match="subscribed"):
            await channel.track({"status": "away"})
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_presence_replays_a_resync_requested_during_a_query() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        channel = client.realtime.channel("lobby", channel_type="presence")
        await channel.subscribe()
        assert official.subscription is not None
        official.subscription.presence_entered = asyncio.Event()
        official.subscription.presence_release = asyncio.Event()

        await official.subscription.emit_subscribed()
        await official.subscription.presence_entered.wait()
        await official.subscription.emit_subscribed()
        official.subscription.presence_clients = {
            "carol-client": SimpleNamespace(
                client="carol-client", user="carol", conn_info={}
            )
        }
        official.subscription.presence_release.set()
        await asyncio.wait_for(channel._wait_presence_sync(), timeout=0.2)

        assert official.subscription.calls.count(("presence", None)) == 3
        assert set(channel.get_presence_state()) == {"carol-client"}
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_presence_resync_replays_concurrent_join_and_leave() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        channel = client.realtime.channel("lobby", channel_type="presence")
        await channel.subscribe()
        assert official.subscription is not None
        carol = SimpleNamespace(client="carol-client", user="carol", conn_info={})
        official.subscription.presence_clients = {"carol-client": carol}
        official.subscription.presence_entered = asyncio.Event()
        official.subscription.presence_release = asyncio.Event()

        resync = asyncio.create_task(official.subscription.emit_subscribed())
        await official.subscription.presence_entered.wait()
        bob = SimpleNamespace(client="bob-client", user="bob", conn_info={})
        join = asyncio.create_task(official.subscription.emit_join(bob))
        leave = asyncio.create_task(official.subscription.emit_leave(carol))
        await asyncio.wait_for(asyncio.shield(join), timeout=0.1)
        await asyncio.wait_for(asyncio.shield(leave), timeout=0.1)
        official.subscription.presence_release.set()
        await asyncio.gather(resync, join, leave)

        assert set(channel.get_presence_state()) == {"bob-client"}
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_track_exposes_immutable_local_state() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        channel = client.realtime.channel("lobby", channel_type="presence")
        await channel.subscribe()
        tracked = {"status": "online"}

        await channel.track(tracked)
        tracked["status"] = "away"

        assert channel.tracked_state == {"status": "online"}
        await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_unsubscribe_clears_presence_state() -> None:
    official = FakeCentrifugeClient()
    official.presence_clients = {
        "alice-client": SimpleNamespace(
            client="alice-client",
            user="alice",
            conn_info={},
        )
    }
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        channel = client.realtime.channel("lobby", channel_type="presence")
        states: list[Any] = []
        cleared = asyncio.Event()

        def on_sync(state: Any) -> None:
            states.append(state)
            if not state:
                cleared.set()

        channel.on_presence_sync(on_sync)
        await channel.subscribe()
        assert official.subscription is not None
        await channel.track({"status": "online"})

        await channel.unsubscribe()
        await asyncio.wait_for(cleared.wait(), timeout=0.1)

        assert channel.get_presence_state() == {}
        assert channel.tracked_state == {}
        assert states[-1] == {}
        with pytest.raises(RuntimeError, match="must be subscribed"):
            await channel.track({"status": "online"})
        await official.subscription.emit_join(
            SimpleNamespace(client="late-client", user="late", conn_info={})
        )
        assert channel.get_presence_state() == {}
        await client.realtime.disconnect()

    asyncio.run(scenario())


async def test_realtime_presence_sync_coalesces_latest_backpressured_state() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    channel = client.realtime.channel("lobby", channel_type="presence")
    blocked = asyncio.Event()
    release = asyncio.Event()
    observed_sizes: list[int] = []
    completed = asyncio.Event()

    async def on_sync(state: Any) -> None:
        observed_sizes.append(len(state))
        if len(state) == 140:
            completed.set()
        if len(state) == 1:
            blocked.set()
            await release.wait()

    channel.on_presence_sync(on_sync)
    await channel.subscribe()
    assert official.subscription is not None
    await official.subscription.emit_join(
        SimpleNamespace(client="client-0", user="user-0", conn_info={})
    )
    await blocked.wait()
    for index in range(1, 140):
        await official.subscription.emit_join(
            SimpleNamespace(
                client=f"client-{index}",
                user=f"user-{index}",
                conn_info={},
            )
        )
    release.set()
    await asyncio.wait_for(completed.wait(), timeout=0.2)

    assert observed_sizes[-1] == 140
    await client.realtime.disconnect()


def test_realtime_newer_queued_snapshot_discards_older_pending_snapshot() -> None:
    client = VolcanoClient(anon_key="anon-key", _transport=AuthTransport())

    async def scenario() -> None:
        channel = client.realtime.channel("lobby", channel_type="presence")
        channel.on_presence_sync(lambda _state: None)

        async def wait_forever() -> None:
            await asyncio.Event().wait()

        blocker = asyncio.create_task(wait_forever())
        channel._callback_task = blocker
        for _ in range(channel._callback_queue.maxsize):
            channel._callback_queue.put_nowait(
                realtime_module._CallbackDelivery(
                    "presence_sync",
                    {"version": 0},
                )
            )

        await channel._emit("presence_sync", {"version": 1})
        channel._callback_queue.get_nowait()
        channel._callback_queue.task_done()
        await channel._emit("presence_sync", {"version": 2})
        queued: list[Any] = []
        while not channel._callback_queue.empty():
            queued.append(channel._callback_queue.get_nowait().data)
            channel._callback_queue.task_done()
        channel._enqueue_pending_presence_sync()
        blocker.cancel()
        await asyncio.gather(blocker, return_exceptions=True)

        assert queued[-1] == {"version": 2}
        assert channel._callback_queue.empty()

    asyncio.run(scenario())


def test_realtime_presence_operations_reject_broadcast_channels() -> None:
    client = VolcanoClient(anon_key="anon-key", _transport=AuthTransport())
    channel = client.realtime.channel("contract")

    with pytest.raises(ValueError, match="presence channels"):
        channel.on_presence_sync(lambda _state: None)

    async def scenario() -> None:
        with pytest.raises(ValueError, match="presence channels"):
            await channel.track()

    asyncio.run(scenario())


def test_realtime_rejects_unsupported_channel_types() -> None:
    client = VolcanoClient(anon_key="anon-key", _transport=AuthTransport())
    unsupported = cast("Any", "presense")

    with pytest.raises(ValueError, match="channel type"):
        client.realtime.channel("contract", channel_type=unsupported)

    async def scenario() -> None:
        with pytest.raises(ValueError, match="channel type"):
            await client.realtime.remove_channel(
                "contract",
                channel_type=unsupported,
            )

    asyncio.run(scenario())


def test_realtime_presence_values_are_hashable_without_metadata() -> None:
    first = RealtimePresenceInfo(
        client="client-1",
        user="user-1",
        data={"status": "online"},
    )
    second = RealtimePresenceInfo(
        client="client-1",
        user="user-1",
        data={"status": "away"},
    )

    assert hash(first) == hash(second)


def test_realtime_reports_presence_query_failures() -> None:
    official = FakeCentrifugeClient()
    official.presence_clients = {
        "alice-client": SimpleNamespace(
            client="alice-client", user="alice", conn_info={}
        )
    }
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")
    errors: list[RealtimeErrorContext] = []
    presence_error = centrifuge_error("presence unavailable")

    async def scenario() -> None:
        reported = asyncio.Event()

        def on_error(context: RealtimeErrorContext) -> None:
            errors.append(context)
            reported.set()

        client.realtime.on_error(on_error)
        channel = client.realtime.channel(
            "lobby",
            channel_type="presence",
        )
        await channel.subscribe()
        assert channel.get_presence_state()
        assert official.subscription is not None
        official.subscription.presence_error = presence_error
        await official.subscription.emit_subscribed()
        await asyncio.wait_for(reported.wait(), timeout=0.1)
        assert channel.get_presence_state() == {}
        await client.realtime.disconnect()

    asyncio.run(scenario())

    assert len(errors) == 1
    assert errors[0].message == "presence unavailable"
    assert errors[0].error is presence_error


def test_realtime_wraps_official_client_without_exposing_it() -> None:
    transport = AuthTransport()
    official = FakeCentrifugeClient()
    factory_arguments: dict[str, Any] = {}

    def factory(
        address: str,
        *,
        events: Any,
        token: str,
        get_token: Callable[[], Awaitable[str]],
    ) -> FakeCentrifugeClient:
        factory_arguments.update(
            address=address,
            events=events,
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
        assert official.subscription.recoverable is True
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
        with pytest.raises(RuntimeError, match="must be subscribed"):
            await channel.send({"event": "message", "value": "late"})

        generation, _lineage, _session = client._capture_session_binding()
        refreshed = Session(
            access_token="access-2",
            refresh_token="refresh-token-2",
            user_id="user-123",
        )
        assert client._set_session_if_current(
            refreshed,
            generation,
            event="TOKEN_REFRESHED",
        )
        assert await factory_arguments["get_token"]() == "access-2"
        transport.access_token = "access-3"
        client.auth.sign_in(email="user@example.com", password="secret")
        with pytest.raises(RuntimeError, match="session changed"):
            await factory_arguments["get_token"]()
        assert client.realtime._connection_token() == "access-2"
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


def test_realtime_broadcast_resubscribe_retains_recoverable_subscription() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        channel = client.realtime.channel("room")
        await channel.subscribe()
        subscription = official.subscription
        assert subscription is not None
        assert subscription.recoverable is True

        await channel.unsubscribe()
        await channel.subscribe()

        assert official.subscription is subscription
        assert subscription.calls == [
            ("subscribe", None),
            ("unsubscribe", None),
            ("subscribe", None),
        ]
        await client.realtime.disconnect()

    asyncio.run(scenario())


@pytest.mark.parametrize("channel_type", ["broadcast", "presence"])
def test_realtime_paused_channel_ignores_wire_publications(
    channel_type: realtime_module.ChannelType,
) -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        received: list[Any] = []
        channel = client.realtime.channel("room", channel_type=channel_type)
        channel.on("message", received.append)
        await channel.subscribe()
        await channel.unsubscribe()
        try:
            await official.emit_wire_publication(
                f"project-id:{channel.name}", {"value": "paused"}
            )
            await asyncio.wait_for(channel._callback_queue.join(), timeout=0.2)
            assert received == []
            await channel.subscribe()
            await official.emit_wire_publication(
                f"project-id:{channel.name}", {"value": "resumed"}
            )
            await asyncio.wait_for(channel._callback_queue.join(), timeout=0.2)
            assert received == [{"value": "resumed"}]
        finally:
            await client.realtime.disconnect()

    asyncio.run(scenario())


@pytest.mark.parametrize("resume", [False, True])
def test_realtime_discards_queued_messages_when_delivery_is_paused(
    *, resume: bool
) -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        received: list[Any] = []
        entered, release = asyncio.Event(), asyncio.Event()

        async def receive(message: Any) -> None:
            received.append(message)
            entered.set()
            await release.wait()

        channel = client.realtime.channel("room")
        channel.on("message", receive)
        await channel.subscribe()
        try:
            await official.emit_wire_publication(channel.name, "active")
            await asyncio.wait_for(entered.wait(), timeout=0.2)
            await official.emit_wire_publication(channel.name, "queued")
            await channel.unsubscribe()
            if resume:
                await channel.subscribe()
            release.set()
            await asyncio.wait_for(channel._callback_queue.join(), timeout=0.2)
            assert received == ["active"]
        finally:
            release.set()
            await client.realtime.disconnect()

    asyncio.run(scenario())


@pytest.mark.parametrize("resume", [False, True])
def test_realtime_discards_queued_presence_events_on_pause(*, resume: bool) -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        entered, release = asyncio.Event(), asyncio.Event()
        received: list[Any] = []
        snapshots: list[Any] = []

        async def block(_message: Any) -> None:
            entered.set()
            await release.wait()

        channel = client.realtime.channel("lobby", channel_type="presence")
        channel.on("message", block)
        channel.on("join", received.append).on("leave", received.append)
        channel.on_presence_sync(snapshots.append)
        await channel.subscribe()
        await asyncio.wait_for(channel._callback_queue.join(), timeout=0.2)
        snapshots.clear()
        assert official.subscription is not None
        try:
            await official.subscription.emit("active")
            await asyncio.wait_for(entered.wait(), timeout=0.2)
            info = SimpleNamespace(client="peer", user="user", conn_info={})
            await official.subscription.emit_join(info)
            await official.subscription.emit_leave(info)
            await channel.unsubscribe()
            if resume:
                await channel.subscribe()
            release.set()
            await asyncio.wait_for(channel._callback_queue.join(), timeout=0.2)
            assert received == []
            assert snapshots
            assert all(state == {} for state in snapshots)
        finally:
            release.set()
            await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_explicit_pause_frees_queue_capacity_for_recovered_messages() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        entered, release = asyncio.Event(), asyncio.Event()
        received: list[Any] = []

        async def receive(message: Any) -> None:
            received.append(message)
            entered.set()
            await release.wait()

        channel = client.realtime.channel("room").on("message", receive)
        await channel.subscribe()
        assert official.subscription is not None
        try:
            await official.subscription.emit("active")
            await asyncio.wait_for(entered.wait(), timeout=0.2)
            for _ in range(channel._callback_queue.maxsize):
                await official.subscription.emit("obsolete")
            await channel.unsubscribe()
            await channel.subscribe()
            await official.subscription.emit("recovered")
            release.set()
            await asyncio.wait_for(channel._callback_queue.join(), timeout=0.2)
            assert received == ["active", "recovered"]
        finally:
            release.set()
            await client.realtime.disconnect()

    asyncio.run(scenario())


@pytest.mark.parametrize("channel_type", ["broadcast", "presence"])
def test_realtime_reconnect_preserves_messages_already_accepted_by_centrifuge(
    monkeypatch: pytest.MonkeyPatch,
    channel_type: realtime_module.ChannelType,
) -> None:
    async def scenario() -> None:
        factory = ControlledCentrifugeFactory(monkeypatch)
        official = factory.client
        client = VolcanoClient(
            anon_key="anon-key",
            _transport=AuthTransport(),
            _realtime_client_factory=factory,
        )
        client.auth.sign_in(email="user@example.com", password="secret")
        entered, release = asyncio.Event(), asyncio.Event()
        received: list[Any] = []

        async def receive(message: Any) -> None:
            received.append(message)
            entered.set()
            await release.wait()

        channel = client.realtime.channel("room", channel_type=channel_type).on(
            "message", receive
        )
        subscribing = asyncio.create_task(channel.subscribe())
        command = await factory.command()
        await factory.reply(
            command, subscribe={"recoverable": True, "offset": 0, "epoch": "stream"}
        )
        if channel_type == "presence":
            presence = await factory.command()
            await factory.reply(presence, presence={"presence": {}})
        await asyncio.wait_for(subscribing, timeout=0.2)
        subscription = official.get_subscription(channel.name)
        try:
            await subscription._process_publication({"offset": 1, "data": 1})
            await asyncio.wait_for(entered.wait(), timeout=0.2)
            await subscription._process_publication({"offset": 2, "data": 2})
            await subscription._move_subscribing(1, "transport closed")
            command = await factory.command()
            assert command["subscribe"]["offset"] == 2
            await factory.reply(
                command,
                subscribe={
                    "recoverable": True,
                    "epoch": "stream",
                    "offset": 3,
                    "was_recovering": True,
                    "recovered": True,
                    "publications": [{"offset": 3, "data": 3}],
                },
            )
            if channel_type == "presence":
                presence = await factory.command()
                await factory.reply(presence, presence={"presence": {}})
            release.set()
            await asyncio.wait_for(channel._callback_queue.join(), timeout=0.2)
            assert received == [1, 2, 3]
        finally:
            release.set()
            await client.realtime.disconnect()

    asyncio.run(scenario())


def test_centrifuge_preserves_recovery_position_across_unsubscribe() -> None:
    async def scenario() -> None:
        centrifuge = importlib.import_module("centrifuge")
        client = centrifuge.Client(
            "ws://localhost/realtime/v1/websocket",
            loop=asyncio.get_running_loop(),
        )
        subscription = client.new_subscription("broadcast:room", recoverable=True)
        subscription._recover = True
        subscription._epoch = "stream-epoch"
        subscription._offset = 41
        subscription.state = centrifuge.SubscriptionState.SUBSCRIBED

        unsubscribe = AsyncMock(spec_set=client._unsubscribe, return_value=None)
        client._unsubscribe = unsubscribe

        await subscription.unsubscribe()
        unsubscribe.assert_awaited_once_with("broadcast:room")
        command = client._construct_subscribe_command(subscription, 1)

        subscribe = command["subscribe"]
        assert subscribe["channel"] == "broadcast:room"
        assert subscribe["recoverable"] is True
        assert subscribe["recover"] is True
        assert subscribe["epoch"] == "stream-epoch"
        assert subscribe["offset"] == 41

    asyncio.run(scenario())


def test_realtime_rejects_a_session_change_during_connect() -> None:
    transport = AuthTransport()
    official = BlockingConnectCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=transport,
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        subscribing = asyncio.create_task(client.realtime.channel("room").subscribe())
        await official.connect_started.wait()
        transport.access_token = "access-2"
        client.auth.sign_in(email="user@example.com", password="secret")
        official.connect_release.set()

        with pytest.raises(RuntimeError, match="session changed"):
            await subscribing

    asyncio.run(scenario())

    assert official.calls == ["connect", "disconnect"]
    assert client.realtime._connection is None


def test_realtime_retains_a_provisional_connection_when_cleanup_fails() -> None:
    transport = AuthTransport()
    official = BlockingConnectCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=transport,
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        subscribing = asyncio.create_task(client.realtime.channel("room").subscribe())
        await official.connect_started.wait()
        transport.access_token = "access-2"
        client.auth.sign_in(email="user@example.com", password="secret")
        cleanup_error = centrifuge_error("disconnect failed")
        official.disconnect_error = cleanup_error
        official.connect_release.set()

        with pytest.raises(type(cleanup_error), match="disconnect failed"):
            await subscribing
        assert client.realtime._connection is not None

        official.disconnect_error = None
        with pytest.raises(RuntimeError, match="session changed"):
            await client.realtime.channel("room").subscribe()
        await client.realtime.disconnect()

    asyncio.run(scenario())

    assert official.calls == ["connect", "disconnect", "disconnect"]
    assert client.realtime._connection is None


def test_realtime_connection_callbacks_receive_immutable_contexts() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        connected: list[RealtimeConnectContext] = []
        disconnected: list[RealtimeDisconnectContext] = []
        errors: list[RealtimeErrorContext] = []
        connected_event = asyncio.Event()
        disconnected_event = asyncio.Event()
        error_event = asyncio.Event()

        def on_connected(context: RealtimeConnectContext) -> None:
            connected.append(context)
            connected_event.set()

        def on_disconnected(context: RealtimeDisconnectContext) -> None:
            disconnected.append(context)
            disconnected_event.set()

        def on_error(context: RealtimeErrorContext) -> None:
            errors.append(context)
            error_event.set()

        stop_connect = client.realtime.on_connect(on_connected)
        disconnect_callback = AsyncMock(
            spec_set=on_disconnected, side_effect=on_disconnected
        )
        client.realtime.on_disconnect(disconnect_callback)
        stop_error = client.realtime.on_error(on_error)

        await client.realtime.channel("contract").subscribe()
        await asyncio.wait_for(connected_event.wait(), timeout=0.1)
        assert connected == [RealtimeConnectContext(client="client-123")]

        error = RuntimeError("socket failed")
        await official.emit_error(7, error)
        await asyncio.wait_for(error_event.wait(), timeout=0.1)
        assert errors == [
            RealtimeErrorContext(code=7, message="socket failed", error=error)
        ]

        stop_connect()
        stop_connect()
        stop_error()
        await client.realtime.disconnect()
        await asyncio.wait_for(disconnected_event.wait(), timeout=0.1)
        assert disconnected == [
            RealtimeDisconnectContext(code=0, reason="disconnect called")
        ]
        disconnect_callback.assert_awaited_once_with(disconnected[0])

    asyncio.run(scenario())


def test_realtime_connection_callbacks_do_not_block_transport_events() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        callback_started = asyncio.Event()
        callback_release = asyncio.Event()

        async def on_connect(_context: RealtimeConnectContext) -> None:
            callback_started.set()
            await callback_release.wait()

        client.realtime.on_connect(on_connect)
        await asyncio.wait_for(
            client.realtime.channel("contract").subscribe(),
            timeout=0.1,
        )
        await asyncio.wait_for(callback_started.wait(), timeout=0.1)
        callback_release.set()
        await client.realtime.disconnect()

    asyncio.run(scenario())


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
        assert_same(client.realtime.is_connected, expected=False)
        await channel.subscribe()
        assert_same(client.realtime.is_connected, expected=True)

        await client.realtime.remove_channel("contract")

        assert official.subscription is not None
        assert official.subscription.calls[-1] == ("unsubscribe", None)
        replacement = client.realtime.channel("contract")
        assert replacement is not channel
        await replacement.subscribe()
        assert_same(client.realtime.is_connected, expected=True)
        await client.realtime.remove_channel("missing")
        await client.realtime.disconnect()
        assert_same(client.realtime.is_connected, expected=False)

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
        assert_same(client.realtime.is_connected, expected=True)

        official.state = SimpleNamespace(value="connecting")

        assert_same(client.realtime.is_connected, expected=False)
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
        assert_same(client.realtime.is_connected, expected=True)
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


async def test_realtime_callback_failure_does_not_stop_later_callbacks() -> None:
    transport = AuthTransport()
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=transport,
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

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
        with pytest.raises(asyncio.CancelledError):
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

    def failing_disconnect() -> None:
        first.calls.append("disconnect")
        message = "disconnect failed"
        raise RuntimeError(message)

    disconnect = AsyncMock(spec_set=first.disconnect, side_effect=failing_disconnect)
    monkeypatch.setattr(first, "disconnect", disconnect)

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
    disconnect.assert_awaited_once_with()


def test_realtime_disconnect_closes_transport_when_channel_reset_is_cancelled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
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
        reset_started = asyncio.Event()
        second_reset = False
        original_second_reset = second._reset

        async def blocking_reset() -> None:
            reset_started.set()
            await asyncio.Event().wait()

        async def observe_second_reset() -> None:
            nonlocal second_reset
            await original_second_reset()
            second_reset = True

        monkeypatch.setattr(first, "_reset", blocking_reset)
        monkeypatch.setattr(second, "_reset", observe_second_reset)
        disconnecting = asyncio.create_task(client.realtime.disconnect())
        await reset_started.wait()
        disconnecting.cancel()

        with pytest.raises(asyncio.CancelledError):
            await disconnecting

        assert official.state.value == "disconnected"
        assert official.calls[-1] == "disconnect"
        assert first._subscription is None
        assert not first._subscribed
        assert second_reset
        assert second._subscription is None
        assert not second._subscribed
        assert client.realtime._connection is None
        assert client.realtime._connection_access_token is None
        assert client.realtime._connection_session_lineage is None

    asyncio.run(scenario())


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

    def new_subscription(
        name: str,
        *,
        events: Any,
        join_leave: bool = False,
        recoverable: bool = False,
    ) -> FakeSubscription:
        official.calls.append(f"channel:{name}")
        official.subscription = BlockingSubscription(
            name,
            events,
            join_leave=join_leave,
            recoverable=recoverable,
        )
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
        with pytest.raises(asyncio.CancelledError):
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


@pytest.mark.parametrize("operation", ["remove", "remove_all", "disconnect"])
def test_realtime_shutdown_does_not_cancel_or_wait_for_application_work(
    operation: str,
) -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        started, release, completed = (asyncio.Event() for _ in range(3))
        received: list[str] = []

        async def receive(message: str) -> None:
            received.append(message)
            started.set()
            await release.wait()
            await asyncio.gather(client.realtime.disconnect())
            completed.set()

        channel = client.realtime.channel("room").on("message", receive)
        await channel.subscribe()
        await official.emit_wire_publication(channel.name, "running")
        await started.wait()
        await official.emit_wire_publication(channel.name, "queued")
        operations = {
            "remove": lambda: client.realtime.remove_channel("room"),
            "remove_all": client.realtime.remove_all_channels,
            "disconnect": client.realtime.disconnect,
        }
        try:
            await asyncio.wait_for(operations[operation](), timeout=0.2)
            await asyncio.wait_for(operations[operation](), timeout=0.2)
            assert not completed.is_set()
            release.set()
            await asyncio.wait_for(completed.wait(), timeout=0.2)
            await channel._callback_queue.join()
            assert received == ["running"]
            await asyncio.sleep(0)
            assert not client.realtime._callback_tasks
        finally:
            release.set()
            await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_reconnect_serializes_delivery_after_running_callback() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        started, release = asyncio.Event(), asyncio.Event()
        received: list[str] = []

        async def receive(message: str) -> None:
            received.append(message)
            if message == "first":
                started.set()
                await release.wait()
                received.append("finished")

        channel = client.realtime.channel("room").on("message", receive)
        await channel.subscribe()
        await official.emit_wire_publication(channel.name, "first")
        await started.wait()
        try:
            for _ in range(2):
                await client.realtime.disconnect()
                await channel.subscribe()
                await official.emit_wire_publication(channel.name, "discarded")
            await channel.unsubscribe()
            await channel.subscribe()
            await official.emit_wire_publication(channel.name, "resumed")
            await asyncio.sleep(0)
            assert received == ["first"]
            release.set()
            await asyncio.wait_for(channel._callback_queue.join(), timeout=0.2)
            assert received == ["first", "finished", "resumed"]
        finally:
            release.set()
            await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_callback_child_tasks_can_stop_delivery() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        completed = asyncio.Event()

        async def receive(_message: Any) -> None:
            await asyncio.gather(client.realtime.remove_channel("room"))
            await asyncio.wait_for(client.realtime.disconnect(), timeout=0.2)
            completed.set()

        channel = client.realtime.channel("room").on("message", receive)
        await channel.subscribe()
        await official.emit_wire_publication(channel.name, "message")
        await asyncio.wait_for(completed.wait(), timeout=0.2)

    asyncio.run(scenario())


def test_realtime_event_loop_shutdown_does_not_start_queued_callbacks() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")
    received: list[str] = []
    channel = client.realtime.channel("room")

    async def scenario() -> None:
        started = asyncio.Event()

        async def receive(message: str) -> None:
            received.append(message)
            started.set()
            await asyncio.Event().wait()

        channel.on("message", receive)
        await channel.subscribe()
        await official.emit_wire_publication(channel.name, "running")
        await started.wait()
        await official.emit_wire_publication(channel.name, "queued")

    asyncio.run(scenario())
    assert received == ["running"]
    assert channel._callback_task is None or channel._callback_task.done()


def test_realtime_callback_workers_finish_when_idle() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        received: list[str] = []
        channel = client.realtime.channel("room").on("message", received.append)
        await channel.subscribe()
        try:
            for message in ("first", "second"):
                await official.emit_wire_publication(channel.name, message)
                await channel._callback_queue.join()
                await asyncio.sleep(0)
                assert channel._callback_task is None or channel._callback_task.done()
            assert received == ["first", "second"]
        finally:
            await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_callback_cancellation_does_not_cancel_later_delivery() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        received: list[str] = []
        errors: list[dict[str, Any]] = []
        loop = asyncio.get_running_loop()
        previous_handler = loop.get_exception_handler()
        loop.set_exception_handler(lambda _loop, context: errors.append(context))

        async def receive(message: str) -> None:
            if message == "cancel":
                task = asyncio.current_task()
                assert task is not None
                task.cancel()
                await asyncio.sleep(0)
            received.append(message)

        channel = client.realtime.channel("room").on("message", receive)
        await channel.subscribe()
        try:
            await official.emit_wire_publication(channel.name, "cancel")
            await official.emit_wire_publication(channel.name, "next")
            await asyncio.wait_for(channel._callback_queue.join(), timeout=0.2)
            assert received == ["next"]
            assert len(errors) == 1
            assert isinstance(errors[0]["exception"], asyncio.CancelledError)
        finally:
            loop.set_exception_handler(previous_handler)
            await client.realtime.disconnect()

    asyncio.run(scenario())


def test_realtime_worker_registration_precedes_callback_execution(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def scenario() -> None:
        factory = ControlledCentrifugeFactory(monkeypatch)
        client = VolcanoClient(
            anon_key="anon-key",
            _transport=AuthTransport(),
            _realtime_client_factory=factory,
        )
        client.auth.sign_in(email="user@example.com", password="secret")
        received: list[str] = []
        release = asyncio.Event()
        channel = client.realtime.channel("room", channel_type="presence")

        async def receive(_message: Any) -> None:
            received.append("message started")
            await channel.unsubscribe()
            await release.wait()
            received.append("message finished")

        channel.on("message", receive)
        channel.on_presence_sync(lambda _state: received.append("presence"))
        subscribing = asyncio.create_task(channel.subscribe())
        await factory.reply(await factory.command(), subscribe={})
        await factory.reply(await factory.command(), presence={"presence": {}})
        await subscribing
        await channel._wait_presence_sync()
        await channel._callback_queue.join()
        await asyncio.sleep(0)
        received.clear()
        loop = asyncio.get_running_loop()
        previous_factory = loop.get_task_factory()
        # Python 3.11 uses deferred tasks; later runtimes also support eager tasks.
        loop.set_task_factory(getattr(asyncio, "eager_task_factory", None))
        try:
            subscription = factory.client.get_subscription(channel.name)
            await subscription._process_publication({"data": "message"})
            command = await factory.command()
            assert "unsubscribe" in command
            await factory.reply(command, unsubscribe={})
            assert received == ["message started"]
            release.set()
            await asyncio.wait_for(channel._callback_queue.join(), timeout=0.2)
            assert received == ["message started", "message finished", "presence"]
        finally:
            release.set()
            loop.set_task_factory(previous_factory)
            await client.realtime.disconnect()

    asyncio.run(scenario())


@pytest.mark.parametrize("channel_type", ["broadcast", "presence", "postgres"])
def test_realtime_subscribe_waits_for_server_acknowledgement(
    monkeypatch: pytest.MonkeyPatch,
    channel_type: realtime_module.ChannelType,
) -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        requested = asyncio.Event()

        async def subscribe(subscription: FakeSubscription) -> None:
            subscription.subscribed.clear()
            await subscription.emit_subscribing()
            requested.set()

        monkeypatch.setattr(FakeSubscription, "subscribe", subscribe)
        channel = client.realtime.channel("contract", channel_type=channel_type)
        try:
            for _ in range(2):
                requested.clear()
                subscribing = asyncio.create_task(channel.subscribe())
                await asyncio.wait_for(requested.wait(), timeout=0.2)
                assert not subscribing.done()
                assert official.subscription is not None
                await official.subscription.emit_subscribed()
                await asyncio.wait_for(subscribing, timeout=0.2)
                assert_same(channel._subscribed, expected=True)
                if channel_type == "broadcast":
                    await channel.send({"value": "ready"})
                    assert official.subscription.calls[-1] == (
                        "publish",
                        {"value": "ready"},
                    )
                await channel.unsubscribe()
        finally:
            await client.realtime.disconnect()

    asyncio.run(scenario())


@pytest.mark.parametrize("cancelled", [False, True])
def test_realtime_subscribe_releases_connection_lock_after_readiness_failure(
    monkeypatch: pytest.MonkeyPatch, *, cancelled: bool
) -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")
    error = (
        asyncio.CancelledError() if cancelled else centrifuge_error("ready timed out")
    )

    ready = create_autospec(FakeSubscription.ready, spec_set=True, side_effect=error)
    monkeypatch.setattr(FakeSubscription, "ready", ready)

    async def scenario() -> None:
        channel = client.realtime.channel("contract")
        with pytest.raises(type(error)) as failure:
            await channel.subscribe()
        assert failure.value is error
        await asyncio.wait_for(client.realtime.disconnect(), timeout=0.2)
        assert not client.realtime.is_connected

    asyncio.run(scenario())

    ready.assert_awaited_once_with(official.subscription)


@pytest.mark.parametrize("cancelled", [False, True])
@pytest.mark.parametrize("cleanup_fails", [False, True])
async def test_realtime_failed_readiness_cannot_activate_later(
    monkeypatch: pytest.MonkeyPatch, *, cancelled: bool, cleanup_fails: bool
) -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    requested = asyncio.Event()
    fail = asyncio.Event()
    received: list[Any] = []

    async def subscribe(subscription: FakeSubscription) -> None:
        await subscription.emit_subscribing()
        requested.set()

    async def ready(_subscription: FakeSubscription) -> None:
        await fail.wait()
        message = "ready timed out"
        raise centrifuge_error(message)

    channel = client.realtime.channel("contract").on("message", received.append)
    with monkeypatch.context() as patch:
        patch.setattr(FakeSubscription, "subscribe", subscribe)
        patch.setattr(FakeSubscription, "ready", ready)
        subscribing = asyncio.create_task(channel.subscribe())
        await asyncio.wait_for(requested.wait(), timeout=0.2)
        stale = official.subscription
        assert stale is not None
        if cleanup_fails:
            stale.unsubscribe_error = centrifuge_error("cleanup failed")
        if cancelled:
            subscribing.cancel()
        else:
            fail.set()
        error = asyncio.CancelledError if cancelled else type(centrifuge_error(""))
        with pytest.raises(error):
            await subscribing
    try:
        await stale.emit_subscribed()
        await stale.emit("late acknowledgement")
        await asyncio.wait_for(channel._callback_queue.join(), timeout=0.2)
        assert_same(channel._subscribed, expected=False)
        assert received == []
        assert ("unsubscribe", None) in stale.calls
        stale.unsubscribe_error = None
        await channel.subscribe()
        await stale.emit_subscribing()
        await stale.emit("obsolete subscription")
        await channel.send("retry")
        await official.emit_wire_publication(channel.name, "retry")
        await asyncio.wait_for(channel._callback_queue.join(), timeout=0.2)
        assert received == ["retry"]
    finally:
        await client.realtime.disconnect()


async def test_realtime_removal_can_overlap_readiness_rollback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    requested, unsubscribed, release = (
        asyncio.Event(),
        asyncio.Event(),
        asyncio.Event(),
    )

    async def subscribe(subscription: FakeSubscription) -> None:
        await subscription.emit_subscribing()
        requested.set()

    async def ready(_subscription: FakeSubscription) -> None:
        await unsubscribed.wait()
        message = "subscription unsubscribed"
        raise centrifuge_error(message)

    async def unsubscribe(_subscription: FakeSubscription) -> None:
        if unsubscribed.is_set():
            return
        # Centrifuge marks the subscription unsubscribed before awaiting its reply.
        unsubscribed.set()
        await release.wait()

    monkeypatch.setattr(FakeSubscription, "subscribe", subscribe)
    monkeypatch.setattr(FakeSubscription, "ready", ready)
    monkeypatch.setattr(FakeSubscription, "unsubscribe", unsubscribe)
    channel = client.realtime.channel("pending")
    subscribing = asyncio.create_task(channel.subscribe())
    await asyncio.wait_for(requested.wait(), timeout=0.2)
    removing = asyncio.create_task(client.realtime.remove_channel("pending"))
    try:
        await asyncio.wait_for(unsubscribed.wait(), timeout=0.2)
        release.set()
        with pytest.raises(type(centrifuge_error("")), match="unsubscribed"):
            await asyncio.wait_for(subscribing, timeout=0.2)
        await asyncio.wait_for(removing, timeout=0.2)
        assert client.realtime.channel("pending") is not channel
    finally:
        release.set()
        await asyncio.gather(subscribing, removing, return_exceptions=True)
        await client.realtime.disconnect()


@pytest.mark.parametrize("operation", ["send", "unsubscribe", "remove", "disconnect"])
def test_realtime_pending_readiness_does_not_block_other_operations(
    monkeypatch: pytest.MonkeyPatch, operation: str
) -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        requested = asyncio.Event()
        healthy = client.realtime.channel("healthy")
        await healthy.subscribe()

        async def subscribe(subscription: FakeSubscription) -> None:
            await subscription.emit_subscribing()
            requested.set()

        monkeypatch.setattr(FakeSubscription, "subscribe", subscribe)
        pending = client.realtime.channel("pending")
        subscribing = asyncio.create_task(pending.subscribe())
        await asyncio.wait_for(requested.wait(), timeout=0.2)
        try:
            operations = {
                "send": lambda: healthy.send("healthy"),
                "unsubscribe": healthy.unsubscribe,
                "remove": lambda: client.realtime.remove_channel("pending"),
                "disconnect": client.realtime.disconnect,
            }
            await asyncio.wait_for(operations[operation](), timeout=0.2)
            if operation in {"remove", "disconnect"}:
                assert official.subscription is not None
                await official.subscription.emit_subscribed()
                assert not pending._subscribed
                with pytest.raises(asyncio.CancelledError):
                    await asyncio.wait_for(subscribing, timeout=0.2)
            else:
                assert official.subscription is not None
                await official.subscription.emit_subscribed()
                await asyncio.wait_for(subscribing, timeout=0.2)
                await pending.send("ready")
        finally:
            subscribing.cancel()
            await asyncio.gather(subscribing, return_exceptions=True)
            await client.realtime.disconnect()

    asyncio.run(scenario())


@pytest.mark.parametrize("channel_type", ["broadcast", "presence", "postgres"])
def test_realtime_native_subscription_waits_for_acknowledgement(
    monkeypatch: pytest.MonkeyPatch,
    channel_type: realtime_module.ChannelType,
) -> None:
    async def scenario() -> None:
        factory = ControlledCentrifugeFactory(monkeypatch)
        client = VolcanoClient(
            anon_key="anon-key",
            _transport=AuthTransport(),
            _realtime_client_factory=factory,
        )
        client.auth.sign_in(email="user@example.com", password="secret")
        channel = client.realtime.channel("room", channel_type=channel_type)
        subscribing = asyncio.create_task(channel.subscribe())
        try:
            command = await factory.command()
            assert not subscribing.done()
            await factory.reply(command, subscribe={})
            if channel_type == "presence":
                command = await factory.command()
                assert "presence" in command
                assert not subscribing.done()
                await factory.reply(command, presence={"presence": {}})
            await asyncio.wait_for(subscribing, timeout=0.2)
            assert_same(channel._subscribed, expected=True)
            if channel_type == "broadcast":
                sending = asyncio.create_task(channel.send("ready"))
                command = await factory.command()
                assert command["publish"]["data"] == "ready"
                await factory.reply(command, publish={})
                await asyncio.wait_for(sending, timeout=0.2)
        finally:
            await client.realtime.disconnect()
            await asyncio.gather(subscribing, return_exceptions=True)

    asyncio.run(scenario())


@pytest.mark.parametrize("cancelled", [False, True])
def test_realtime_native_failed_readiness_stops_late_acknowledgement_and_allows_retry(
    monkeypatch: pytest.MonkeyPatch, *, cancelled: bool
) -> None:
    async def scenario() -> None:
        factory = ControlledCentrifugeFactory(monkeypatch)
        if not cancelled:
            factory.client._timeout = 0.01
        client = VolcanoClient(
            anon_key="anon-key",
            _transport=AuthTransport(),
            _realtime_client_factory=factory,
        )
        client.auth.sign_in(email="user@example.com", password="secret")
        received: list[Any] = []
        channel = client.realtime.channel("room").on("message", received.append)
        subscribing = asyncio.create_task(channel.subscribe())
        try:
            original_command = await factory.command()
            original_subscription = factory.client.get_subscription(channel.name)
            if cancelled:
                subscribing.cancel()
            stopping = await factory.command()
            assert "unsubscribe" in stopping
            await factory.reply(original_command, subscribe={})
            await original_subscription._process_publication({"data": "obsolete"})
            await factory.reply(stopping, unsubscribe={})
            error = (
                asyncio.CancelledError
                if cancelled
                else realtime_module.CENTRIFUGE_ERROR
            )
            with pytest.raises(error):
                await asyncio.wait_for(subscribing, timeout=0.2)
            assert_same(channel._subscribed, expected=False)
            assert channel._subscription is None
            assert received == []

            subscribing = asyncio.create_task(channel.subscribe())
            command = await factory.command()
            await factory.reply(command, subscribe={})
            await asyncio.wait_for(subscribing, timeout=0.2)
            subscription = factory.client.get_subscription(channel.name)
            assert subscription is not original_subscription
            await subscription._process_publication({"data": "retry"})
            await asyncio.wait_for(channel._callback_queue.join(), timeout=0.2)
            assert received == ["retry"]
        finally:
            await client.realtime.disconnect()
            await asyncio.gather(subscribing, return_exceptions=True)

    asyncio.run(scenario())


@pytest.mark.parametrize("failed_reply", [False, True])
def test_realtime_cancelled_subscribe_settles_late_presence_reply(
    monkeypatch: pytest.MonkeyPatch, *, failed_reply: bool
) -> None:
    async def scenario() -> None:
        factory = ControlledCentrifugeFactory(monkeypatch)
        client = VolcanoClient(
            anon_key="anon-key",
            _transport=AuthTransport(),
            _realtime_client_factory=factory,
        )
        client.auth.sign_in(email="user@example.com", password="secret")
        channel = client.realtime.channel("room", channel_type="presence")
        subscribing = asyncio.create_task(channel.subscribe())
        await factory.reply(await factory.command(), subscribe={})
        presence = await factory.command()
        subscribing.cancel()
        stopping = await factory.command()
        assert "unsubscribe" in stopping
        try:
            if failed_reply:
                await factory.reply(
                    presence, error={"code": 100, "message": "presence unavailable"}
                )
            else:
                await factory.reply(
                    presence,
                    presence={
                        "presence": {"stale": {"client": "stale", "user": "peer"}}
                    },
                )
            await factory.reply(stopping, unsubscribe={})
            with pytest.raises(asyncio.CancelledError):
                await subscribing
            assert channel._subscription is None
            assert channel.get_presence_state() == {}
            subscribing = asyncio.create_task(channel.subscribe())
            await factory.reply(await factory.command(), subscribe={})
            await factory.reply(await factory.command(), presence={"presence": {}})
            await asyncio.wait_for(subscribing, timeout=0.2)
            assert_same(channel._subscribed, expected=True)
        finally:
            await client.realtime.disconnect()
            await asyncio.gather(subscribing, return_exceptions=True)

    asyncio.run(scenario())


def test_realtime_removed_channel_does_not_cancel_callback_subscription(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def scenario() -> None:
        factory = ControlledCentrifugeFactory(monkeypatch)
        client = VolcanoClient(
            anon_key="anon-key",
            _transport=AuthTransport(),
            _realtime_client_factory=factory,
        )
        client.auth.sign_in(email="user@example.com", password="secret")
        active = client.realtime.channel("active")
        pending = client.realtime.channel("pending")
        completed = asyncio.Event()

        async def receive(_message: Any) -> None:
            await pending.subscribe()
            completed.set()

        active.on("message", receive)
        subscribing = asyncio.create_task(active.subscribe())
        await factory.reply(await factory.command(), subscribe={})
        await subscribing
        subscription = factory.client.get_subscription(active.name)
        await subscription._process_publication({"data": "subscribe"})
        pending_command = await factory.command()
        removing = asyncio.create_task(client.realtime.remove_channel("active"))
        try:
            command = await factory.command()
            assert command["unsubscribe"]["channel"] == active.name
            await factory.reply(command, unsubscribe={})
            await asyncio.wait_for(removing, timeout=0.2)
            assert not completed.is_set()
            await factory.reply(pending_command, subscribe={})
            await asyncio.wait_for(completed.wait(), timeout=0.2)
            assert pending._subscribed
            assert client.realtime.channel("active") is not active
        finally:
            await client.realtime.disconnect()
            await asyncio.gather(removing, return_exceptions=True)

    asyncio.run(scenario())


def test_realtime_pause_during_readiness_retains_native_recovery(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def scenario() -> None:
        factory = ControlledCentrifugeFactory(monkeypatch)
        client = VolcanoClient(
            anon_key="anon-key",
            _transport=AuthTransport(),
            _realtime_client_factory=factory,
        )
        client.auth.sign_in(email="user@example.com", password="secret")
        channel = client.realtime.channel("room")
        subscribing = asyncio.create_task(channel.subscribe())
        await factory.reply(
            await factory.command(),
            subscribe={"recoverable": True, "offset": 10, "epoch": "stream"},
        )
        await subscribing
        subscription = factory.client.get_subscription(channel.name)
        pausing = asyncio.create_task(channel.unsubscribe())
        await factory.reply(await factory.command(), unsubscribe={})
        await pausing
        subscribing = asyncio.create_task(channel.subscribe())
        pending_command = await factory.command()
        assert pending_command["subscribe"]["offset"] == 10
        pausing = asyncio.create_task(channel.unsubscribe())
        command = await factory.command()
        try:
            await factory.reply(pending_command, subscribe={})
            await factory.reply(command, unsubscribe={})
            await pausing
            with pytest.raises(RuntimeError, match="subscription was interrupted"):
                await subscribing
            assert channel._subscription is subscription
            subscribing = asyncio.create_task(channel.subscribe())
            command = await factory.command()
            assert command["subscribe"]["offset"] == 10
            await factory.reply(command, subscribe={})
            await asyncio.wait_for(subscribing, timeout=0.2)
        finally:
            await client.realtime.disconnect()
            await asyncio.gather(subscribing, pausing, return_exceptions=True)

    asyncio.run(scenario())


@pytest.mark.parametrize("remove_all", [False, True])
def test_realtime_failed_removal_clears_presence(
    monkeypatch: pytest.MonkeyPatch, *, remove_all: bool
) -> None:
    async def scenario() -> None:
        factory = ControlledCentrifugeFactory(monkeypatch)
        client = VolcanoClient(
            anon_key="anon-key",
            _transport=AuthTransport(),
            _realtime_client_factory=factory,
        )
        client.auth.sign_in(email="user@example.com", password="secret")
        channel = client.realtime.channel("room", channel_type="presence")
        subscribing = asyncio.create_task(channel.subscribe())
        await factory.reply(await factory.command(), subscribe={})
        await factory.reply(
            await factory.command(),
            presence={"presence": {"peer": {"client": "peer", "user": "user"}}},
        )
        await subscribing
        await channel.track({"status": "online"})
        removing = asyncio.create_task(
            client.realtime.remove_all_channels()
            if remove_all
            else client.realtime.remove_channel("room", channel_type="presence")
        )
        await factory.command()
        try:
            await factory.client.disconnect()
            with pytest.raises(realtime_module.CENTRIFUGE_ERROR):
                await removing
            assert channel.get_presence_state() == {}
            assert channel.tracked_state == {}
            assert_same(channel._subscribed, expected=False)
        finally:
            await client.realtime.disconnect()
            await asyncio.gather(removing, return_exceptions=True)

    asyncio.run(scenario())


@pytest.mark.parametrize("channel_type", ["broadcast", "presence", "postgres"])
def test_realtime_disconnect_cancels_readiness_and_allows_immediate_retry(
    monkeypatch: pytest.MonkeyPatch, channel_type: Any
) -> None:
    async def scenario() -> None:
        first = ControlledCentrifugeFactory(monkeypatch)
        second = ControlledCentrifugeFactory(monkeypatch)
        factories = iter((first, second))

        def factory(*args: Any, **kwargs: Any) -> Any:
            return next(factories)(*args, **kwargs)

        client = VolcanoClient(
            anon_key="anon-key",
            _transport=AuthTransport(),
            _realtime_client_factory=factory,
        )
        client.auth.sign_in(email="user@example.com", password="secret")
        channel = client.realtime.channel("room", channel_type=channel_type)
        subscribing = asyncio.create_task(channel.subscribe())
        await first.command()
        retrying: asyncio.Task[None] | None = None
        try:
            await client.realtime.disconnect()
            done, _ = await asyncio.wait({subscribing}, timeout=0.2)
            assert subscribing in done
            with pytest.raises(asyncio.CancelledError):
                await subscribing
            retrying = asyncio.create_task(channel.subscribe())
            await second.reply(await second.command(), subscribe={})
            if channel_type == "presence":
                await second.reply(await second.command(), presence={"presence": {}})
            await asyncio.wait_for(retrying, timeout=0.2)
            assert_same(channel._subscribed, expected=True)
        finally:
            subscribing.cancel()
            if retrying is not None:
                retrying.cancel()
                await asyncio.gather(retrying, return_exceptions=True)
            await asyncio.gather(subscribing, return_exceptions=True)
            await client.realtime.disconnect()

    asyncio.run(scenario())


@pytest.mark.parametrize("remove_all", [False, True])
def test_realtime_cancelled_local_removal_clears_presence(*, remove_all: bool) -> None:
    async def scenario() -> None:
        official = FakeCentrifugeClient()
        official.presence_clients = {
            "peer": SimpleNamespace(client="peer", user="user")
        }
        client = VolcanoClient(
            anon_key="anon-key",
            _transport=AuthTransport(),
            _realtime_client_factory=FakeCentrifugeFactory(official),
        )
        client.auth.sign_in(email="user@example.com", password="secret")
        channel = client.realtime.channel("room", channel_type="presence")
        await channel.subscribe()
        await channel.track({"status": "online"})
        subscription = official.subscription
        assert subscription is not None
        subscription.unsubscribe_entered = asyncio.Event()
        subscription.unsubscribe_release = asyncio.Event()
        removing = asyncio.create_task(
            client.realtime.remove_all_channels()
            if remove_all
            else client.realtime.remove_channel("room", channel_type="presence")
        )
        try:
            await subscription.unsubscribe_entered.wait()
            removing.cancel()
            subscription.unsubscribe_release.set()
            with pytest.raises(asyncio.CancelledError):
                await removing
            assert channel.get_presence_state() == {}
            assert channel.tracked_state == {}
            assert_same(channel._subscribed, expected=False)
        finally:
            await client.realtime.disconnect()
            await asyncio.gather(removing, return_exceptions=True)

    asyncio.run(scenario())


@pytest.mark.parametrize("channel_type", ["broadcast", "presence", "postgres"])
def test_realtime_repeated_subscribe_does_not_stop_active_delivery(
    monkeypatch: pytest.MonkeyPatch, channel_type: realtime_module.ChannelType
) -> None:
    async def scenario() -> None:
        factory = ControlledCentrifugeFactory(monkeypatch)
        client = VolcanoClient(
            anon_key="anon-key",
            _transport=AuthTransport(),
            _realtime_client_factory=factory,
        )
        client.auth.sign_in(email="user@example.com", password="secret")
        channel = client.realtime.channel("room", channel_type=channel_type)
        subscribing = asyncio.create_task(channel.subscribe())
        await factory.reply(await factory.command(), subscribe={})
        if channel_type == "presence":
            await factory.reply(await factory.command(), presence={"presence": {}})
        await subscribing
        subscribing = asyncio.create_task(channel.subscribe())
        try:
            await asyncio.sleep(0)
            assert subscribing.done()
            assert not subscribing.cancel()
            await subscribing
            assert factory.commands.empty()
            assert_same(channel._subscribed, expected=True)
        finally:
            await client.realtime.disconnect()
            await asyncio.gather(subscribing, return_exceptions=True)

    asyncio.run(scenario())


@pytest.mark.parametrize("disconnect", [False, True])
async def test_realtime_stop_invalidates_queued_subscribe_calls(
    monkeypatch: pytest.MonkeyPatch, *, disconnect: bool
) -> None:
    first = ControlledCentrifugeFactory(monkeypatch)
    second = ControlledCentrifugeFactory(monkeypatch)
    factories = iter((first, second))

    def factory(*args: Any, **kwargs: Any) -> Any:
        return next(factories)(*args, **kwargs)

    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=factory,
    )
    client.auth.sign_in(email="user@example.com", password="secret")
    channel = client.realtime.channel("room")
    subscribing = asyncio.create_task(channel.subscribe())
    await first.command()
    queued = asyncio.create_task(channel.subscribe())
    await asyncio.sleep(0)
    assert not queued.done()
    stopping = asyncio.create_task(
        client.realtime.disconnect() if disconnect else channel.unsubscribe()
    )
    retrying: asyncio.Task[None] | None = None
    try:
        if not disconnect:
            await first.reply(await first.command(), unsubscribe={})
        await stopping
        done, _ = await asyncio.wait({subscribing, queued}, timeout=0.2)
        assert done == {subscribing, queued}
        with pytest.raises(asyncio.CancelledError):
            await queued
        assert_same(channel._subscribed, expected=False)
        assert first.commands.empty()
        assert second.commands.empty()
        retrying = asyncio.create_task(channel.subscribe())
        current = second if disconnect else first
        await current.reply(await current.command(), subscribe={})
        await asyncio.wait_for(retrying, timeout=0.2)
        assert_same(channel._subscribed, expected=True)
    finally:
        for task in (subscribing, queued, stopping, retrying):
            if task is not None:
                task.cancel()
                await asyncio.gather(task, return_exceptions=True)
        await client.realtime.disconnect()


def test_realtime_repeated_pause_invalidates_intervening_subscribe(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def scenario() -> None:
        factory = ControlledCentrifugeFactory(monkeypatch)
        client = VolcanoClient(
            anon_key="anon-key",
            _transport=AuthTransport(),
            _realtime_client_factory=factory,
        )
        client.auth.sign_in(email="user@example.com", password="secret")
        channel = client.realtime.channel("room")
        first = asyncio.create_task(channel.subscribe())
        await factory.command()
        pause = asyncio.create_task(channel.unsubscribe())
        await asyncio.sleep(0)
        queued = asyncio.create_task(channel.subscribe())
        last_pause = asyncio.create_task(channel.unsubscribe())
        try:
            await factory.reply(await factory.command(), unsubscribe={})
            await pause
            await last_pause
            done, _ = await asyncio.wait({first, queued}, timeout=0.2)
            assert done == {first, queued}
            with pytest.raises(asyncio.CancelledError):
                await queued
            assert_same(channel._subscribed, expected=False)
            assert factory.commands.empty()
        finally:
            await client.realtime.disconnect()
            for task in (first, queued, pause, last_pause):
                task.cancel()
                await asyncio.gather(task, return_exceptions=True)

    asyncio.run(scenario())


@pytest.mark.parametrize("operation", ["unsubscribe", "remove", "remove_all"])
@pytest.mark.parametrize("outcome", ["reply", "error", "disconnect"])
async def test_realtime_cancelled_unsubscribe_keeps_native_replies_valid(
    monkeypatch: pytest.MonkeyPatch, operation: str, outcome: str
) -> None:
    factory = ControlledCentrifugeFactory(monkeypatch)
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=factory,
    )
    client.auth.sign_in(email="user@example.com", password="secret")
    channel = client.realtime.channel("room")
    subscribing = asyncio.create_task(channel.subscribe())
    await factory.reply(await factory.command(), subscribe={})
    await subscribing
    operations = {
        "unsubscribe": channel.unsubscribe,
        "remove": lambda: client.realtime.remove_channel("room"),
        "remove_all": client.realtime.remove_all_channels,
    }
    stopping = asyncio.create_task(operations[operation]())
    command = await factory.command()
    stopping.cancel()
    await asyncio.sleep(0)
    stopping.cancel()
    await asyncio.sleep(0)
    retrying: asyncio.Task[None] | None = None
    try:
        if outcome != "disconnect":
            retrying = asyncio.create_task(channel.subscribe())
            await asyncio.sleep(0)
            assert factory.commands.empty()
            assert not retrying.done()
        if outcome == "disconnect":
            await factory.client.disconnect()
        elif outcome == "error":
            await factory.reply(command, error={"code": 100, "message": "failed"})
        else:
            await factory.reply(command, unsubscribe={})
        with pytest.raises(asyncio.CancelledError):
            await asyncio.wait_for(stopping, timeout=0.2)
        assert_same(channel._subscribed, expected=False)
        if retrying is not None:
            await factory.reply(await factory.command(), subscribe={})
            await asyncio.wait_for(retrying, timeout=0.2)
            publishing = asyncio.create_task(channel.send("still reading replies"))
            await factory.reply(await factory.command(), publish={})
            await asyncio.wait_for(publishing, timeout=0.2)
    finally:
        await asyncio.gather(stopping, return_exceptions=True)
        await client.realtime.disconnect()


def test_realtime_cancelled_unsubscribe_settles_on_native_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def scenario() -> None:
        factory = ControlledCentrifugeFactory(monkeypatch)
        client = VolcanoClient(
            anon_key="anon-key",
            _transport=AuthTransport(),
            _realtime_client_factory=factory,
        )
        client.auth.sign_in(email="user@example.com", password="secret")
        channel = client.realtime.channel("room")
        subscribing = asyncio.create_task(channel.subscribe())
        await factory.reply(await factory.command(), subscribe={})
        await subscribing
        factory.client._timeout = 0.01
        stopping = asyncio.create_task(channel.unsubscribe())
        await factory.command()
        stopping.cancel()
        try:
            with pytest.raises(asyncio.CancelledError):
                await asyncio.wait_for(stopping, timeout=0.2)
            assert_same(channel._subscribed, expected=False)
            assert not factory.client._inflight_commands
        finally:
            await client.realtime.disconnect()

    asyncio.run(scenario())


@pytest.mark.parametrize("same_session", [False, True])
def test_realtime_binds_bootstrap_refresh_without_profile(
    *, same_session: bool
) -> None:
    def token(session_id: str) -> str:
        payload = base64.urlsafe_b64encode(
            json.dumps({"session_id": session_id}).encode()
        ).decode()
        return f"header.{payload}.signature"

    class BootstrapTransport(AuthTransport):
        def auth_refresh(self, **_arguments: Any) -> Response:
            return Response(
                200,
                {
                    "access_token": token(
                        "00000000-0000-4000-8000-000000000001"
                        if same_session
                        else "00000000-0000-4000-8000-000000000002"
                    ),
                    "refresh_token": "other-refresh",
                    "user": {"id": "00000000-0000-4000-8000-000000000002"},
                },
            )

    async def scenario() -> None:
        official = FakeCentrifugeClient()
        client = VolcanoClient(
            anon_key="anon",
            access_token=token("00000000-0000-4000-8000-000000000001"),
            refresh_token="other-refresh",
            _transport=BootstrapTransport(),
            _realtime_client_factory=FakeCentrifugeFactory(official),
        )
        try:
            await client.realtime.channel("contract").subscribe()
            assert client.current_session is not None
            assert client.current_session.user_id is None
            if same_session:
                client.auth.refresh_session()
                await client.realtime.channel("another").subscribe()
            else:
                with pytest.raises(
                    AuthenticationError, match="different server session"
                ):
                    client.auth.refresh_session()
            assert client.current_session.access_token == token(
                "00000000-0000-4000-8000-000000000001"
            )
        finally:
            await client.realtime.disconnect()

    asyncio.run(scenario())
