from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest
from test_realtime import FakeCentrifugeClient, FakeCentrifugeFactory

from volcano_sdk import PostgresChange, Session, VolcanoClient
from volcano_sdk._realtime_fetch_worker import (
    PostgresFetchJob,
    PostgresFetchOutcome,
    PostgresFetchRequest,
)
from volcano_sdk.realtime import (
    _consume_presence_result,
    _finish_unsubscribe,
    _PostgresDelivery,
)


def make_client() -> VolcanoClient:
    return VolcanoClient(
        anon_key="anon",
        access_token="access",
        _realtime_client_factory=FakeCentrifugeFactory(FakeCentrifugeClient()),
    )


async def test_cancelled_native_work_preserves_the_callers_cancellation() -> None:
    task = asyncio.create_task(asyncio.sleep(0))
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    cancellation = asyncio.CancelledError("caller cancelled")

    _consume_presence_result(task)
    with pytest.raises(asyncio.CancelledError) as caught:
        _finish_unsubscribe(task, cancellation)

    assert caught.value is cancellation
    assert task.cancelled()


async def test_stale_native_presence_callbacks_cannot_repopulate_removed_channels() -> (
    None
):
    client = make_client()
    channel = client.realtime.channel("lobby", channel_type="presence")
    try:
        await channel.subscribe()
        events = channel._subscription_events
        assert events is not None
        await client.realtime.remove_channel("lobby", channel_type="presence")
        replacement = client.realtime.channel("lobby", channel_type="presence")
        await replacement.subscribe()
        context = SimpleNamespace(info=SimpleNamespace(client="stale", user="user"))

        await events.on_join(context)
        await events.on_leave(context)

        assert channel.get_presence_state() == {}
        assert replacement.get_presence_state() == {}
    finally:
        await client.realtime.disconnect()


def test_postgres_listener_removal_is_idempotent() -> None:
    channel = make_client().realtime.channel("public:messages", channel_type="postgres")
    unsubscribe = channel.on_postgres_changes(
        "*", schema="public", table="messages", callback=lambda _change: None
    )

    unsubscribe()
    unsubscribe()

    assert channel._postgres_filters == {}
    assert not channel._has_postgres_listener(
        PostgresChange(type="INSERT", schema="public", table="messages")
    )


async def test_postgres_failure_cannot_deliver_into_a_replacement_session() -> None:
    client = make_client()
    channel = client.realtime.channel("public:messages", channel_type="postgres")
    received: list[object] = []
    channel.on("*", received.append)
    replacement = Session("other-access", "other-refresh", "other-user")
    errors: list[dict[str, object]] = []
    loop = asyncio.get_running_loop()
    previous = loop.get_exception_handler()

    def replace_session(
        _loop: asyncio.AbstractEventLoop, context: dict[str, object]
    ) -> None:
        errors.append(context)
        client.auth.set_session(replacement)

    loop.set_exception_handler(replace_session)
    try:
        await channel.subscribe()
        change = PostgresChange(
            type="UPDATE", schema="public", table="messages", id=42, mode="lightweight"
        )
        delivery = _PostgresDelivery(
            change, channel._capture_postgres_delivery_identity()
        )
        request = PostgresFetchRequest("main", "access", "messages", 42)
        failure = RuntimeError("fetch rejected")
        await channel._deliver_postgres(
            PostgresFetchOutcome(job=PostgresFetchJob(request, delivery), error=failure)
        )

        assert client.current_session == replacement
        assert received == []
        assert channel._callback_queue.empty()
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
    channel._schedule_presence_sync()
    task = channel._presence_sync_task
    assert task is not None

    await channel.unsubscribe()
    await task

    assert channel._presence_sync_task is None
    assert channel.get_presence_state() == {}
    assert client.realtime._connection is None


async def test_removing_an_unsubscribed_channel_preserves_a_new_registration() -> None:
    realtime = make_client().realtime
    original = realtime.channel("messages")
    await realtime.remove_channel("messages")
    replacement = realtime.channel("messages")

    assert await realtime._remove_registered_channel(original.name, original) is None

    assert realtime.channel("messages") is replacement
    assert replacement is not original
    assert realtime._removing_channels == set()
    assert realtime._connection is None


async def test_failed_subscription_cleanup_rechecks_ownership_after_lock_wait(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = make_client()
    channel = client.realtime.channel("messages")
    paused = asyncio.Event()
    pause = channel._pause_delivery

    def pause_and_notify() -> None:
        pause()
        paused.set()

    monkeypatch.setattr(channel, "_pause_delivery", pause_and_notify)
    try:
        await channel.subscribe()
        subscription = channel._subscription
        assert subscription is not None
        async with client.realtime._connection_lock:
            cleanup = asyncio.create_task(
                client.realtime._cleanup_failed_subscription(
                    channel, subscription, RuntimeError("ready failed")
                )
            )
            await asyncio.wait_for(paused.wait(), timeout=2)
            await client.realtime._discard_subscription(channel)
            replacement = await client.realtime._prepare_subscription(
                channel, channel._subscribe_generation
            )
        await asyncio.wait_for(cleanup, timeout=2)

        assert replacement is not subscription
        assert channel._subscription is replacement
        assert channel._subscription_events is not None
        await channel.subscribe()
        assert channel._subscription is replacement
        assert channel._subscribed
    finally:
        await client.realtime.disconnect()
