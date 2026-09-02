from __future__ import annotations

import asyncio
import importlib
from dataclasses import dataclass
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, cast

import pytest

from volcano_sdk import (
    RealtimeConnectContext,
    RealtimeDisconnectContext,
    RealtimeErrorContext,
    RealtimePresenceInfo,
    VolcanoClient,
)

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
        self.unsubscribe_error: Exception | None = None
        self.unsubscribe_entered: asyncio.Event | None = None
        self.unsubscribe_release: asyncio.Event | None = None

    async def subscribe(self) -> None:
        self.calls.append(("subscribe", None))
        await self.emit_subscribed()

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
        self.subscription: FakeSubscription | None = None
        self._subs: dict[str, FakeSubscription] = {}

    async def connect(self) -> None:
        self.calls.append("connect")
        self.state = SimpleNamespace(value="connected")
        if self.events is not None:
            await self.events.on_connected(SimpleNamespace(client="client-123"))

    async def disconnect(self) -> None:
        self.calls.append("disconnect")
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
        events: Any,
        token: str,
        get_token: Callable[[], Awaitable[str]],
    ) -> FakeCentrifugeClient:
        del address, token, get_token
        self.client.events = events
        return self.client


def test_realtime_channel_exposes_its_canonical_name() -> None:
    client = VolcanoClient(anon_key="anon-key", _transport=AuthTransport())

    assert client.realtime.channel("contract").name == "broadcast:contract"
    assert (
        client.realtime.channel("contract", channel_type="presence").name
        == "presence:contract"
    )


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
        await asyncio.sleep(0)

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


def test_realtime_presence_sync_coalesces_latest_backpressured_state() -> None:
    official = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")

    async def scenario() -> None:
        channel = client.realtime.channel("lobby", channel_type="presence")
        blocked = asyncio.Event()
        release = asyncio.Event()
        observed_sizes: list[int] = []

        async def on_sync(state: Any) -> None:
            observed_sizes.append(len(state))
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
        for _ in range(500):
            if observed_sizes[-1] == 140:
                break
            await asyncio.sleep(0)

        assert observed_sizes[-1] == 140
        await client.realtime.disconnect()

    asyncio.run(scenario())


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
            channel._callback_queue.put_nowait(("presence_sync", {"version": 0}))

        await channel._emit("presence_sync", {"version": 1})
        channel._callback_queue.get_nowait()
        channel._callback_queue.task_done()
        await channel._emit("presence_sync", {"version": 2})
        queued: list[Any] = []
        while not channel._callback_queue.empty():
            queued.append(channel._callback_queue.get_nowait()[1])
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
    official.presence_error = centrifuge_error("presence unavailable")
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=AuthTransport(),
        _realtime_client_factory=FakeCentrifugeFactory(official),
    )
    client.auth.sign_in(email="user@example.com", password="secret")
    errors: list[RealtimeErrorContext] = []

    async def scenario() -> None:
        reported = asyncio.Event()

        def on_error(context: RealtimeErrorContext) -> None:
            errors.append(context)
            reported.set()

        client.realtime.on_error(on_error)
        await client.realtime.channel(
            "lobby",
            channel_type="presence",
        ).subscribe()
        await asyncio.wait_for(reported.wait(), timeout=0.1)
        await client.realtime.disconnect()

    asyncio.run(scenario())

    assert len(errors) == 1
    assert errors[0].message == "presence unavailable"
    assert errors[0].error is official.presence_error


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
        assert official.subscription.recoverable is False
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

        async def on_disconnected(context: RealtimeDisconnectContext) -> None:
            disconnected.append(context)
            disconnected_event.set()

        def on_error(context: RealtimeErrorContext) -> None:
            errors.append(context)
            error_event.set()

        stop_connect = client.realtime.on_connect(on_connected)
        client.realtime.on_disconnect(on_disconnected)
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
