from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from volcano_sdk import PostgresChange, Session, VolcanoClient
from volcano_sdk._realtime_fetch_worker import (
    PostgresFetchJob,
    PostgresFetchOutcome,
    PostgresFetchRequest,
)
from volcano_sdk._realtime_messages import (
    CallbackDelivery,
    PostgresDelivery,
)
from volcano_sdk._realtime_transport import (
    consume_presence_result,
    finish_unsubscribe,
)

from .realtime_probes import channel_state, failed_operation, realtime_state
from .state_assertions import assert_same
from .test_realtime import FakeCentrifugeClient, FakeCentrifugeFactory


def make_client() -> VolcanoClient:
    return VolcanoClient(
        anon_key="anon",
        access_token="access",
        _realtime_client_factory=FakeCentrifugeFactory(FakeCentrifugeClient()),
    )


async def test_cancelled_native_work_preserves_the_callers_cancellation() -> None:
    task = asyncio.create_task(asyncio.sleep(0))
    _ = task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    cancellation = asyncio.CancelledError("caller cancelled")

    consume_presence_result(task)
    with pytest.raises(asyncio.CancelledError) as caught:
        finish_unsubscribe(task, cancellation)

    assert caught.value is cancellation
    assert task.cancelled()


async def test_stale_presence_callbacks_cannot_change_a_resubscribed_channel() -> None:
    native = FakeCentrifugeClient()
    current = SimpleNamespace(client="current", user="user")
    native.presence_clients = {"current": current}
    client = VolcanoClient(
        anon_key="anon",
        access_token="access",
        _realtime_client_factory=FakeCentrifugeFactory(native),
    )
    channel = client.realtime.channel("lobby", channel_type="presence")
    synced = asyncio.Event()

    def observe_sync(_state: object) -> None:
        synced.set()

    _ = channel.on("presence_sync", observe_sync)
    try:
        await channel.subscribe()
        _ = await asyncio.wait_for(synced.wait(), timeout=2)
        events = channel_state(channel).subscription_events
        assert events is not None
        await client.realtime.disconnect()
        synced.clear()
        await channel.subscribe()
        _ = await asyncio.wait_for(synced.wait(), timeout=2)
        roster = channel.get_presence_state()
        assert tuple(roster) == ("current",)
        assert channel_state(channel).subscription_events is not events

        await events.on_join(
            SimpleNamespace(info=SimpleNamespace(client="stale", user="other"))
        )
        assert channel.get_presence_state() == roster

        await events.on_leave(SimpleNamespace(info=current))
        assert channel.get_presence_state() == roster
    finally:
        await client.realtime.disconnect()


def test_postgres_listener_removal_is_idempotent() -> None:
    channel = make_client().realtime.channel("public:messages", channel_type="postgres")
    unsubscribe = channel.on_postgres_changes(
        "*", schema="public", table="messages", callback=lambda _change: None
    )

    unsubscribe()
    unsubscribe()

    assert channel_state(channel).postgres_filters == {}
    assert not channel_state(channel).has_postgres_listener(
        PostgresChange(type="INSERT", schema="public", table="messages")
    )


def test_postgres_channel_without_listeners_ignores_changes() -> None:
    channel = make_client().realtime.channel("public:messages", channel_type="postgres")

    assert not channel_state(channel).has_postgres_listener(
        PostgresChange(type="INSERT", schema="public", table="messages")
    )


async def test_postgres_failure_cannot_deliver_into_a_replacement_session() -> None:
    client = make_client()
    channel = client.realtime.channel("public:messages", channel_type="postgres")
    received: list[object] = []
    _ = channel.on("*", received.append)
    replacement = Session("other-access", "other-refresh", "other-user")
    errors: list[dict[str, object]] = []
    loop = asyncio.get_running_loop()
    previous = loop.get_exception_handler()

    def replace_session(
        _loop: asyncio.AbstractEventLoop, context: dict[str, object]
    ) -> None:
        errors.append(context)
        _ = client.auth.set_session(replacement)

    loop.set_exception_handler(replace_session)
    try:
        await channel.subscribe()
        change = PostgresChange(
            type="UPDATE", schema="public", table="messages", id=42, mode="lightweight"
        )
        delivery = PostgresDelivery(
            change, channel_state(channel).capture_postgres_delivery_identity()
        )
        request = PostgresFetchRequest("main", "access", "messages", 42)
        failure = RuntimeError("fetch rejected")
        await channel_state(channel).deliver_postgres(
            PostgresFetchOutcome(job=PostgresFetchJob(request, delivery), error=failure)
        )

        assert client.current_session == replacement
        assert received == []
        assert channel_state(channel).callback_queue.empty()
        assert errors == [
            {
                "message": "Volcano realtime Postgres row fetch failed",
                "exception": failure,
                "channel": channel.name,
            }
        ]
    finally:
        loop.set_exception_handler(previous)
        await client.realtime.disconnect()


async def test_presence_sync_stopped_before_start_releases_its_task() -> None:
    client = make_client()
    channel = client.realtime.channel("lobby", channel_type="presence")
    channel_state(channel).presence.schedule_presence_sync()
    task = channel_state(channel).presence_sync_task
    assert task is not None

    await channel.unsubscribe()
    await task

    assert channel_state(channel).presence_sync_task is None
    assert channel.get_presence_state() == {}
    assert realtime_state(client.realtime).connection is None


async def test_cancelling_presence_sync_drains_the_running_task() -> None:
    channel = make_client().realtime.channel("lobby", channel_type="presence")
    entered = asyncio.Event()
    release = asyncio.Event()
    stopped = asyncio.Event()

    async def blocked_sync() -> None:
        entered.set()
        try:
            _ = await release.wait()
        finally:
            stopped.set()

    task = asyncio.create_task(blocked_sync())
    channel_state(channel).presence_sync_task = task
    try:
        _ = await asyncio.wait_for(entered.wait(), timeout=0.2)
        await asyncio.wait_for(
            channel_state(channel).presence.cancel_presence_sync(), timeout=0.2
        )

        assert task.done()
        assert stopped.is_set()
        assert_same(channel_state(channel).presence_sync_task, expected=None)
    finally:
        release.set()
        _ = task.cancel()
        _ = await asyncio.wait_for(
            asyncio.gather(task, return_exceptions=True), timeout=0.2
        )


async def test_presence_failure_cleanup_aborts_if_error_reporting_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    realtime = make_client().realtime
    channel = realtime.channel("lobby", channel_type="presence")
    await channel_state(channel).presence.begin_presence_sync()

    async def fail_reporting() -> None:
        await failed_operation(RuntimeError())

    monkeypatch.setattr(
        channel_state(channel).presence, "fail_presence_sync", fail_reporting
    )
    with pytest.raises(RuntimeError):
        await realtime_state(realtime).report_presence_sync_failure(
            channel_state(channel), RuntimeError()
        )

    assert not channel_state(channel).presence_syncing
    assert channel_state(channel).presence_events == []


async def test_running_presence_sync_coalesces_a_second_request() -> None:
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
        channel_state(channel).presence.schedule_presence_sync()
        first = channel_state(channel).presence_sync_task
        assert first is not None
        _ = await asyncio.wait_for(subscription.presence_entered.wait(), timeout=0.2)

        channel_state(channel).presence.schedule_presence_sync()
        assert channel_state(channel).presence_sync_task is first
        assert channel_state(channel).presence_sync_pending
        subscription.presence_release.set()
        await asyncio.wait_for(
            channel_state(channel).presence.wait_presence_sync(), timeout=0.2
        )
    finally:
        await client.realtime.disconnect()


async def test_removing_an_unsubscribed_channel_preserves_a_new_registration() -> None:
    realtime = make_client().realtime
    original = realtime.channel("messages")
    await realtime.remove_channel("messages")
    replacement = realtime.channel("messages")

    assert (
        await realtime_state(realtime).remove_registered_channel(
            original.name, channel_state(original)
        )
        is None
    )

    assert realtime.channel("messages") is replacement
    assert replacement is not original
    assert realtime_state(realtime).removing_channels == set()
    assert realtime_state(realtime).connection is None


async def test_removing_a_never_subscribed_channel_leaves_other_native_channels() -> (
    None
):
    client = make_client()
    active = client.realtime.channel("active")
    _ = client.realtime.channel("inactive")
    try:
        await active.subscribe()
        await client.realtime.remove_channel("inactive")

        assert channel_state(active).subscribed
        assert client.realtime.channel("active") is active
    finally:
        await client.realtime.disconnect()


async def test_recovering_presence_channel_drops_queued_join_callback() -> None:
    native = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon",
        access_token="access",
        _realtime_client_factory=FakeCentrifugeFactory(native),
    )
    channel = client.realtime.channel("lobby", channel_type="presence")
    received: list[object] = []
    _ = channel.on("join", received.append)
    try:
        await channel.subscribe()
        subscription = native.subscription
        assert subscription is not None
        queued = CallbackDelivery(
            "join",
            SimpleNamespace(client="stale"),
            delivery_epoch=channel_state(channel).presence_epoch,
        )
        await subscription.emit_subscribing()
        await channel_state(channel).dispatch_delivery(queued)

        assert received == []
    finally:
        await client.realtime.disconnect()


async def test_failed_subscription_cleanup_rechecks_ownership_after_lock_wait(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = make_client()
    channel = client.realtime.channel("messages")
    paused = asyncio.Event()
    pause = channel_state(channel).pause_delivery

    def pause_and_notify() -> None:
        pause()
        paused.set()

    monkeypatch.setattr(channel_state(channel), "pause_delivery", pause_and_notify)
    try:
        await channel.subscribe()
        subscription = channel_state(channel).subscription
        assert subscription is not None
        async with realtime_state(client.realtime).connection_lock:
            cleanup = asyncio.create_task(
                realtime_state(client.realtime).cleanup_failed_subscription(
                    channel_state(channel), subscription, RuntimeError("ready failed")
                )
            )
            _ = await asyncio.wait_for(paused.wait(), timeout=2)
            await realtime_state(client.realtime).discard_subscription(
                channel_state(channel)
            )
            replacement = await realtime_state(client.realtime).prepare_subscription(
                channel_state(channel), channel_state(channel).subscribe_generation
            )
        await asyncio.wait_for(cleanup, timeout=2)

        assert replacement is not subscription
        assert channel_state(channel).subscription is replacement
        assert channel_state(channel).subscription_events is not None
        await channel.subscribe()
        assert channel_state(channel).subscription is replacement
        assert channel_state(channel).subscribed
    finally:
        await client.realtime.disconnect()


async def test_failed_subscription_cleanup_preserves_an_existing_replacement() -> None:
    client = make_client()
    channel = client.realtime.channel("messages")
    try:
        await channel.subscribe()
        stale = channel_state(channel).subscription
        await client.realtime.disconnect()
        await channel.subscribe()
        replacement = channel_state(channel).subscription
        assert stale is not None
        assert replacement is not stale

        await realtime_state(client.realtime).cleanup_failed_subscription(
            channel_state(channel), stale, RuntimeError("stale readiness failed")
        )

        assert channel_state(channel).subscription is replacement
        assert channel_state(channel).subscribed
    finally:
        await client.realtime.disconnect()
