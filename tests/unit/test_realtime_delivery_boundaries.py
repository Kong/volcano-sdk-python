from __future__ import annotations

from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import TYPE_CHECKING

import pytest
from test_realtime import FakeCentrifugeClient, FakeCentrifugeFactory

from volcano_sdk import PostgresChange, VolcanoClient
from volcano_sdk._realtime_fetch_worker import PostgresFetchJob, PostgresFetchOutcome
from volcano_sdk.realtime import _PostgresDelivery

if TYPE_CHECKING:
    from volcano_sdk.models import JSONValue
    from volcano_sdk.realtime import ChannelType, _PostgresDeliveryIdentity


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


@pytest.mark.parametrize("channel_type", ["broadcast", "presence"])
@pytest.mark.parametrize("peer", [None, Peer("absent")])
async def test_presence_events_do_not_populate_inactive_or_non_presence_channels(
    channel_type: ChannelType, peer: Peer | None
) -> None:
    channel = make_client().realtime.channel("lobby", channel_type=channel_type)

    await channel._presence_join(peer)
    await channel._presence_leave(peer)

    assert channel._presence_state == {}
    assert channel._presence_events == []
    assert channel._callback_queue.empty()


async def test_presence_sync_without_a_subscription_has_no_work() -> None:
    realtime = make_client().realtime
    channel = realtime.channel("lobby", channel_type="presence")

    await realtime._sync_presence(channel)

    assert channel.get_presence_state() == {}
    assert not channel._presence_syncing


async def test_presence_snapshot_replays_join_and_leave_received_during_sync() -> None:
    client = make_client()
    channel = client.realtime.channel("lobby", channel_type="presence")
    alice, bob = Peer("alice"), Peer("bob")
    try:
        await channel.subscribe()
        await channel._begin_presence_sync()
        await channel._presence_join(bob)
        await channel._presence_leave(alice)
        await channel._complete_presence_sync({"alice": alice})

        assert set(channel.get_presence_state()) == {"bob"}
        assert channel.get_presence_state()["bob"].user == "user"
        assert channel._presence_events == []
        assert not channel._presence_syncing
    finally:
        await client.realtime.disconnect()


async def test_invalid_presence_snapshot_preserves_the_previous_roster(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = make_client()
    channel = client.realtime.channel("lobby", channel_type="presence")

    async def invalid_presence() -> object:
        return SimpleNamespace(clients=[])

    try:
        await channel.subscribe()
        await channel._presence_join(Peer("alice"))
        original = channel.get_presence_state()
        assert channel._subscription is not None
        monkeypatch.setattr(channel._subscription, "presence", invalid_presence)

        await client.realtime._sync_presence(channel)

        assert channel.get_presence_state() == original
        assert not channel._presence_syncing
        assert channel._presence_events == []
    finally:
        await client.realtime.disconnect()


async def test_inactive_postgres_delivery_cannot_start_a_worker_or_dispatch() -> None:
    channel = make_client().realtime.channel("public:messages", channel_type="postgres")
    received: list[PostgresChange] = []
    _ = channel.on("*", received.append)
    identity = channel._capture_postgres_delivery_identity()
    delivery = _PostgresDelivery(
        change=PostgresChange(type="INSERT", schema="public", table="messages"),
        identity=identity,
    )

    assert channel._postgres_delivery(publication()) is None
    assert await channel._postgres_delivery_worker(identity) is None
    await channel._deliver_postgres(
        PostgresFetchOutcome(job=PostgresFetchJob(request=None, fallback=delivery))
    )

    assert received == []
    assert channel._postgres_worker is None
    assert channel._callback_queue.empty()


async def test_unsubscribe_between_capture_and_worker_selection_drops_delivery(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = make_client()
    channel = client.realtime.channel("public:messages", channel_type="postgres")
    received: list[PostgresChange] = []
    _ = channel.on("*", received.append)
    select_worker = channel._postgres_delivery_worker

    async def stop_before_selection(identity: _PostgresDeliveryIdentity) -> None:
        await channel.unsubscribe()
        assert await select_worker(identity) is None

    monkeypatch.setattr(channel, "_postgres_delivery_worker", stop_before_selection)
    try:
        await channel.subscribe()
        await channel._receive_postgres_change(publication())

        assert received == []
        assert channel._postgres_worker is None
        assert not channel._subscribed
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
        identity = channel._capture_postgres_delivery_identity()
        worker = await channel._postgres_delivery_worker(identity)
        assert worker is not None
        enqueue = worker.enqueue

        async def stop_before_enqueue(job: PostgresFetchJob[_PostgresDelivery]) -> None:
            await worker.abort()
            if unsubscribe:
                await channel.unsubscribe()
            await enqueue(job)

        monkeypatch.setattr(worker, "enqueue", stop_before_enqueue)
        if unsubscribe:
            await channel._receive_postgres_change(publication())
        else:
            with pytest.raises(RuntimeError, match="Postgres fetch worker is closed"):
                await channel._receive_postgres_change(publication())

        assert received == []
    finally:
        await client.realtime.disconnect()
