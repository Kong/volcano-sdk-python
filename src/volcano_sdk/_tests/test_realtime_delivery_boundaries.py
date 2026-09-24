from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from types import SimpleNamespace

import pytest

from volcano_sdk import PostgresChange, VolcanoClient
from volcano_sdk._realtime_fetch_worker import (
    PostgresFetchJob,
    PostgresFetchOutcome,
    PostgresFetchRequest,
)
from volcano_sdk._realtime_messages import (
    PostgresDelivery,
    postgres_change,
    presence_info,
)

from .realtime_probes import channel_state, completed_operation, realtime_state
from .state_assertions import assert_same
from .test_realtime import FakeCentrifugeClient, FakeCentrifugeFactory
from .typing import TYPE_CHECKING

if TYPE_CHECKING:
    from volcano_sdk._realtime_messages import PostgresDeliveryIdentity
    from volcano_sdk.models import JSONValue
    from volcano_sdk.realtime import ChannelType


def empty_metadata() -> dict[str, JSONValue]:
    return {}


@dataclass(frozen=True)
class Peer:
    client: str
    user: str = "user"
    conn_info: dict[str, JSONValue] = field(default_factory=empty_metadata)


def make_client() -> VolcanoClient:
    return VolcanoClient(
        anon_key="anon",
        access_token="access",
        _realtime_client_factory=FakeCentrifugeFactory(FakeCentrifugeClient()),
    )


def publication() -> dict[str, object]:
    return {
        "type": "INSERT",
        "schema": "public",
        "table": "messages",
        "record": {"id": "record"},
        "timestamp": "2026-09-22T12:00:00Z",
    }


def test_postgres_wire_event_rejects_non_json_identifier() -> None:
    malformed = {**publication(), "id": object()}

    assert postgres_change(malformed) is None


@pytest.mark.parametrize("channel_type", ["broadcast", "presence"])
@pytest.mark.parametrize("peer", [None, Peer("absent")])
async def test_presence_events_do_not_populate_inactive_or_non_presence_channels(
    channel_type: ChannelType, peer: Peer | None
) -> None:
    channel = make_client().realtime.channel("lobby", channel_type=channel_type)

    await channel_state(channel).presence.presence_join(peer)
    await channel_state(channel).presence.presence_leave(peer)

    assert channel_state(channel).presence_state == {}
    assert channel_state(channel).presence_events == []
    assert channel_state(channel).callback_queue.empty()


async def test_active_broadcast_channel_ignores_misrouted_presence_events() -> None:
    client = make_client()
    channel = client.realtime.channel("messages")
    peer = Peer("alice")
    try:
        await channel.subscribe()
        await channel_state(channel).presence.presence_join(peer)
        assert channel_state(channel).presence_state == {}

        channel_state(channel).presence_state[peer.client] = presence_info(peer)
        await channel_state(channel).presence.presence_leave(peer)
        assert tuple(channel_state(channel).presence_state) == (peer.client,)
    finally:
        await client.realtime.disconnect()


async def test_presence_leave_notifies_with_the_current_roster() -> None:
    client = make_client()
    channel = client.realtime.channel("lobby", channel_type="presence")
    snapshots: list[object] = []
    _ = channel.on_presence_sync(snapshots.append)
    try:
        await channel.subscribe()
        await channel_state(channel).presence.presence_join(Peer("alice"))
        await channel_state(channel).presence.presence_leave(Peer("alice"))
        await asyncio.wait_for(
            channel_state(channel).callback_queue.join(), timeout=0.2
        )

        assert snapshots[-1] == {}
    finally:
        await client.realtime.disconnect()


async def test_presence_sync_without_a_subscription_has_no_work() -> None:
    realtime = make_client().realtime
    channel = realtime.channel("lobby", channel_type="presence")

    await realtime_state(realtime).sync_presence(channel_state(channel))

    assert channel.get_presence_state() == {}
    assert not channel_state(channel).presence_syncing


async def test_queued_callbacks_keep_their_delivery_identity() -> None:
    client = make_client()
    presence = client.realtime.channel("lobby", channel_type="presence")
    postgres = client.realtime.channel("public:messages", channel_type="postgres")

    def ignore_delivery(_value: object) -> None:
        pass

    _ = presence.on("join", ignore_delivery)
    _ = postgres.on("*", ignore_delivery)

    async def hold() -> None:
        _ = await asyncio.Event().wait()

    blocker = asyncio.create_task(hold())
    channel_state(presence).callback_task = blocker
    channel_state(postgres).callback_task = blocker
    try:
        await channel_state(presence).emit("join", Peer("alice"))
        presence_delivery = channel_state(presence).callback_queue.get_nowait()
        channel_state(presence).callback_queue.task_done()
        assert (
            presence_delivery.delivery_epoch is channel_state(presence).presence_epoch
        )
        assert presence_delivery.postgres_identity is None

        identity = channel_state(postgres).capture_postgres_delivery_identity()
        await channel_state(postgres).emit(
            "*",
            PostgresChange(type="INSERT", schema="public", table="messages"),
            postgres_identity=identity,
        )
        postgres_delivery = channel_state(postgres).callback_queue.get_nowait()
        channel_state(postgres).callback_queue.task_done()
        assert postgres_delivery.postgres_identity is identity
        assert postgres_delivery.delivery_epoch is None
    finally:
        channel_state(presence).callback_task = None
        channel_state(postgres).callback_task = None
        _ = blocker.cancel()
        _ = await asyncio.gather(blocker, return_exceptions=True)


async def test_postgres_delivery_queued_before_unsubscribe_is_not_dispatched() -> None:
    client = make_client()
    channel = client.realtime.channel("public:messages", channel_type="postgres")
    received: list[PostgresChange] = []
    _ = channel.on("*", received.append)

    async def hold() -> None:
        _ = await asyncio.Event().wait()

    blocker = asyncio.create_task(hold())
    try:
        await channel.subscribe()
        channel_state(channel).callback_task = blocker
        change = PostgresChange(type="INSERT", schema="public", table="messages")
        identity = channel_state(channel).capture_postgres_delivery_identity()
        await channel_state(channel).deliver_postgres(
            PostgresFetchOutcome(
                job=PostgresFetchJob(
                    request=None,
                    fallback=PostgresDelivery(change=change, identity=identity),
                )
            )
        )
        queued = channel_state(channel).callback_queue.get_nowait()
        channel_state(channel).callback_queue.task_done()
        await channel_state(channel).end_postgres_epoch()
        await channel_state(channel).dispatch_delivery(queued)

        assert received == []
    finally:
        channel_state(channel).callback_task = None
        _ = blocker.cancel()
        _ = await asyncio.gather(blocker, return_exceptions=True)
        await client.realtime.disconnect()


async def test_missing_postgres_row_reports_its_identity() -> None:
    client = make_client()
    channel = client.realtime.channel("public:messages", channel_type="postgres")
    loop = asyncio.get_running_loop()
    previous_handler = loop.get_exception_handler()
    errors: list[dict[str, object]] = []

    def record(_loop: asyncio.AbstractEventLoop, context: dict[str, object]) -> None:
        errors.append(context)

    loop.set_exception_handler(record)
    try:
        channel_state(channel).report_postgres_fetch_failure(
            PostgresChange(type="INSERT", schema="public", table="messages"),
            PostgresFetchRequest("main", "access", "messages", 42),
            None,
        )
    finally:
        loop.set_exception_handler(previous_handler)
        await client.realtime.disconnect()

    assert len(errors) == 1
    assert errors[0]["message"] == "Volcano realtime Postgres row fetch failed"
    assert errors[0]["channel"] == channel.name
    failure = errors[0]["exception"]
    assert isinstance(failure, LookupError)
    assert str(failure) == "Postgres row not found: public.messages:42"


async def test_presence_snapshot_replays_join_and_leave_received_during_sync() -> None:
    client = make_client()
    channel = client.realtime.channel("lobby", channel_type="presence")
    alice, bob = Peer("alice"), Peer("bob")
    try:
        await channel.subscribe()
        await channel_state(channel).presence.begin_presence_sync()
        await channel_state(channel).presence.presence_join(bob)
        await channel_state(channel).presence.presence_leave(alice)
        await channel_state(channel).presence.complete_presence_sync({"alice": alice})

        assert set(channel.get_presence_state()) == {"bob"}
        assert channel.get_presence_state()["bob"].user == "user"
        assert channel_state(channel).presence_events == []
        assert not channel_state(channel).presence_syncing
    finally:
        await client.realtime.disconnect()


async def test_invalid_presence_snapshot_preserves_the_previous_roster(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = make_client()
    channel = client.realtime.channel("lobby", channel_type="presence")

    async def invalid_presence() -> object:
        return await completed_operation(SimpleNamespace(clients=[]))

    try:
        await channel.subscribe()
        await channel_state(channel).presence.presence_join(Peer("alice"))
        original = channel.get_presence_state()
        assert channel_state(channel).subscription is not None
        monkeypatch.setattr(
            channel_state(channel).subscription, "presence", invalid_presence
        )

        await realtime_state(client.realtime).sync_presence(channel_state(channel))

        assert channel.get_presence_state() == original
        assert not channel_state(channel).presence_syncing
        assert channel_state(channel).presence_events == []
    finally:
        await client.realtime.disconnect()


async def test_presence_query_replays_a_join_received_while_loading() -> None:
    native = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon",
        access_token="access",
        _realtime_client_factory=FakeCentrifugeFactory(native),
    )
    channel = client.realtime.channel("lobby", channel_type="presence")
    try:
        await channel.subscribe()
        subscription = native.subscription
        assert subscription is not None
        subscription.presence_clients = {"alice": Peer("alice")}
        subscription.presence_entered = asyncio.Event()
        subscription.presence_release = asyncio.Event()
        sync = asyncio.create_task(
            realtime_state(client.realtime).sync_presence(channel_state(channel))
        )
        try:
            _ = await asyncio.wait_for(
                subscription.presence_entered.wait(), timeout=0.2
            )
            await channel_state(channel).presence.presence_join(Peer("bob"))
            subscription.presence_release.set()
            await asyncio.wait_for(sync, timeout=0.2)
        finally:
            subscription.presence_release.set()
            _ = sync.cancel()
            _ = await asyncio.gather(sync, return_exceptions=True)

        assert set(channel.get_presence_state()) == {"alice", "bob"}
        assert not channel_state(channel).presence_syncing
    finally:
        await client.realtime.disconnect()


async def test_cancelled_presence_query_releases_the_sync_state() -> None:
    native = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon",
        access_token="access",
        _realtime_client_factory=FakeCentrifugeFactory(native),
    )
    channel = client.realtime.channel("lobby", channel_type="presence")
    try:
        await channel.subscribe()
        subscription = native.subscription
        assert subscription is not None
        subscription.presence_entered = asyncio.Event()
        subscription.presence_release = asyncio.Event()
        sync = asyncio.create_task(
            realtime_state(client.realtime).sync_presence(channel_state(channel))
        )
        try:
            _ = await asyncio.wait_for(
                subscription.presence_entered.wait(), timeout=0.2
            )
            assert channel_state(channel).presence_syncing
            _ = sync.cancel()
            with pytest.raises(asyncio.CancelledError):
                await sync

            assert_same(channel_state(channel).presence_syncing, expected=False)
            assert channel_state(channel).presence_events == []
        finally:
            subscription.presence_release.set()
            _ = await asyncio.gather(sync, return_exceptions=True)
    finally:
        await client.realtime.disconnect()


async def test_inactive_postgres_delivery_cannot_start_a_worker_or_dispatch() -> None:
    channel = make_client().realtime.channel("public:messages", channel_type="postgres")
    received: list[PostgresChange] = []
    _ = channel.on("*", received.append)
    identity = channel_state(channel).capture_postgres_delivery_identity()
    delivery = PostgresDelivery(
        change=PostgresChange(type="INSERT", schema="public", table="messages"),
        identity=identity,
    )

    assert channel_state(channel).postgres_delivery(publication()) is None
    assert await channel_state(channel).postgres_delivery_worker(identity) is None
    await channel_state(channel).deliver_postgres(
        PostgresFetchOutcome(job=PostgresFetchJob(request=None, fallback=delivery))
    )

    assert received == []
    assert channel_state(channel).postgres_worker is None
    assert channel_state(channel).callback_queue.empty()


async def test_unsubscribe_between_capture_and_worker_selection_drops_delivery(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = make_client()
    channel = client.realtime.channel("public:messages", channel_type="postgres")
    received: list[PostgresChange] = []
    _ = channel.on("*", received.append)
    select_worker = channel_state(channel).postgres_delivery_worker

    async def stop_before_selection(identity: PostgresDeliveryIdentity) -> None:
        await channel.unsubscribe()
        assert await select_worker(identity) is None

    monkeypatch.setattr(
        channel_state(channel), "postgres_delivery_worker", stop_before_selection
    )
    try:
        await channel.subscribe()
        await channel_state(channel).receive_postgres_change(publication())

        assert received == []
        assert channel_state(channel).postgres_worker is None
        assert not channel_state(channel).subscribed
    finally:
        await client.realtime.disconnect()


@pytest.mark.parametrize("unsubscribe", [False, True])
async def test_closed_postgres_worker_reports_only_current_delivery_failures(
    monkeypatch: pytest.MonkeyPatch, *, unsubscribe: bool
) -> None:
    client = make_client()
    channel = client.realtime.channel("public:messages", channel_type="postgres")
    received: list[PostgresChange] = []
    _ = channel.on("*", received.append)
    try:
        await channel.subscribe()
        identity = channel_state(channel).capture_postgres_delivery_identity()
        worker = await channel_state(channel).postgres_delivery_worker(identity)
        assert worker is not None
        enqueue = worker.enqueue

        async def stop_before_enqueue(job: PostgresFetchJob[PostgresDelivery]) -> None:
            await worker.abort()
            if unsubscribe:
                await channel.unsubscribe()
            await enqueue(job)

        monkeypatch.setattr(worker, "enqueue", stop_before_enqueue)
        if unsubscribe:
            await channel_state(channel).receive_postgres_change(publication())
        else:
            with pytest.raises(RuntimeError, match="Postgres fetch worker is closed"):
                await channel_state(channel).receive_postgres_change(publication())

        assert received == []
    finally:
        await client.realtime.disconnect()
