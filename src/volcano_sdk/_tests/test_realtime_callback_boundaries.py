from __future__ import annotations

import asyncio
import gc
from typing import TYPE_CHECKING

import pytest

from volcano_sdk import PostgresChange, RealtimeConnectContext, Session, VolcanoClient
from volcano_sdk.realtime import (
    _CallbackDelivery,
    _consume_presence_result,
    _finish_unsubscribe,
)

from .fixtures.invalid_realtime_callback import register_non_callable
from .test_realtime import FakeCentrifugeClient, FakeCentrifugeFactory

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from volcano_sdk.realtime import ChannelType


@pytest.fixture
async def loop_errors() -> AsyncIterator[list[dict[str, object]]]:
    loop = asyncio.get_running_loop()
    previous = loop.get_exception_handler()
    errors: list[dict[str, object]] = []

    def handle(_loop: asyncio.AbstractEventLoop, context: dict[str, object]) -> None:
        errors.append(context)

    loop.set_exception_handler(handle)
    try:
        yield errors
    finally:
        loop.set_exception_handler(previous)


async def test_connection_queue_overflow_reports_the_dropped_callback(
    loop_errors: list[dict[str, object]],
) -> None:
    realtime = VolcanoClient(anon_key="anon").realtime
    received: list[object] = []
    _ = realtime.on_connect(received.append)
    limit = realtime._connection_callback_queue.maxsize
    for index in range(limit + 1):
        realtime._enqueue_connection_callbacks(
            "connect", RealtimeConnectContext(client=str(index))
        )

    await asyncio.wait_for(realtime._connection_callback_queue.join(), timeout=2)

    assert received == [RealtimeConnectContext(client=str(i)) for i in range(limit)]
    assert loop_errors == [
        {"message": "Volcano realtime connection callback queue is full"}
    ]


async def test_removed_connection_listener_does_not_block_later_listeners() -> None:
    realtime = VolcanoClient(anon_key="anon").realtime
    received: list[RealtimeConnectContext] = []
    stop_first = realtime.on_connect(received.append)
    _ = realtime.on_connect(received.append)
    context = RealtimeConnectContext(client="connected")

    realtime._enqueue_connection_callbacks("connect", context)
    stop_first()
    await asyncio.wait_for(realtime._connection_callback_queue.join(), timeout=0.2)

    assert received == [context]


async def test_connection_callbacks_keep_order_while_a_listener_is_running() -> None:
    realtime = VolcanoClient(anon_key="anon").realtime
    entered = asyncio.Event()
    release = asyncio.Event()
    received: list[str] = []

    async def observe(context: RealtimeConnectContext) -> None:
        assert context.client is not None
        if context.client == "first":
            entered.set()
            _ = await release.wait()
        received.append(context.client)

    _ = realtime.on_connect(observe)
    realtime._enqueue_connection_callbacks(
        "connect", RealtimeConnectContext(client="first")
    )
    try:
        _ = await asyncio.wait_for(entered.wait(), timeout=0.2)
        realtime._enqueue_connection_callbacks(
            "connect", RealtimeConnectContext(client="second")
        )
        await asyncio.sleep(0)
        assert received == []
    finally:
        release.set()
        await asyncio.wait_for(realtime._connection_callback_queue.join(), timeout=0.2)

    assert received == ["first", "second"]


async def test_detached_presence_query_exception_is_consumed(
    loop_errors: list[dict[str, object]],
) -> None:
    async def fail() -> None:
        raise RuntimeError

    task = asyncio.create_task(fail())
    await asyncio.sleep(0)
    assert task.done()
    _consume_presence_result(task)
    del task
    _ = gc.collect()
    await asyncio.sleep(0)

    assert loop_errors == []


async def test_cancelled_unsubscribe_consumes_a_native_failure(
    loop_errors: list[dict[str, object]],
) -> None:
    async def fail() -> None:
        raise RuntimeError

    task = asyncio.create_task(fail())
    await asyncio.sleep(0)
    assert task.done()
    with pytest.raises(asyncio.CancelledError):
        _finish_unsubscribe(task, asyncio.CancelledError("caller cancelled"))
    del task
    _ = gc.collect()
    await asyncio.sleep(0)

    assert loop_errors == []


async def test_pending_presence_snapshot_is_not_requeued_or_delivered_after_reset() -> (
    None
):
    channel = VolcanoClient(anon_key="anon").realtime.channel(
        "lobby", channel_type="presence"
    )
    received: list[object] = []
    _ = channel.on_presence_sync(received.append)
    channel._pending_presence_sync = {"version": 1}

    channel._enqueue_pending_presence_sync()
    delivery = channel._callback_queue.get_nowait()
    channel._callback_queue.task_done()
    channel._enqueue_pending_presence_sync()
    assert channel._callback_queue.empty()

    channel._discard_callbacks(presence_only=True)
    await channel._dispatch_delivery(delivery)
    assert received == []


def test_full_queue_coalesces_presence_sync_without_dispatcher() -> None:
    channel = VolcanoClient(anon_key="anon").realtime.channel(
        "lobby", channel_type="presence"
    )
    for index in range(channel._callback_queue.maxsize):
        channel._callback_queue.put_nowait(
            _CallbackDelivery("join", index, delivery_epoch=channel._presence_epoch)
        )

    queued = channel._queue_callback(_CallbackDelivery("presence_sync", {"version": 1}))

    assert not queued
    assert channel._callback_task is None
    assert channel._callback_queue.full()
    assert channel._pending_presence_sync == {"version": 1}


def test_new_presence_channel_has_empty_public_state_and_no_pending_snapshot() -> None:
    channel = VolcanoClient(anon_key="anon").realtime.channel(
        "lobby", channel_type="presence"
    )

    assert channel.tracked_state == {}
    channel._enqueue_pending_presence_sync()
    assert channel._callback_queue.empty()


async def test_reset_presence_channel_exposes_empty_local_state() -> None:
    channel = VolcanoClient(anon_key="anon").realtime.channel(
        "lobby", channel_type="presence"
    )

    await channel._reset()

    assert channel.tracked_state == {}


async def test_stale_postgres_callback_cannot_cross_a_session_change() -> None:
    native = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon",
        access_token="access",
        _realtime_client_factory=FakeCentrifugeFactory(native),
    )
    channel = client.realtime.channel("public:messages", channel_type="postgres")
    received: list[object] = []
    _ = channel.on("*", received.append)
    try:
        await channel.subscribe()
        delivery = _CallbackDelivery(
            "*",
            PostgresChange(type="INSERT", schema="public", table="messages"),
            postgres_identity=channel._capture_postgres_delivery_identity(),
        )
        _ = client.auth.set_session(Session("new-access", "new-refresh", "new-user"))
        await channel._dispatch_delivery(delivery)

        assert received == []
    finally:
        await client.realtime.disconnect()


async def test_channel_queue_overflow_preserves_previously_accepted_delivery(
    loop_errors: list[dict[str, object]],
) -> None:
    client = VolcanoClient(
        anon_key="anon",
        access_token="access",
        _realtime_client_factory=FakeCentrifugeFactory(FakeCentrifugeClient()),
    )
    received: list[object] = []
    channel = client.realtime.channel("messages").on("message", received.append)
    limit = channel._callback_queue.maxsize
    try:
        await channel.subscribe()
        for index in range(limit + 1):
            await channel._emit("message", index)
        await asyncio.wait_for(channel._callback_queue.join(), timeout=2)

        assert received == list(range(limit))
        assert loop_errors == [
            {
                "message": (
                    "Volcano realtime callback queue is full; publication dropped"
                ),
                "channel": channel.name,
            }
        ]
    finally:
        await client.realtime.disconnect()


async def test_removed_connection_callback_does_not_run_from_a_queued_event() -> None:
    realtime = VolcanoClient(anon_key="anon").realtime
    received: list[object] = []

    def remove_later_callback(_context: object) -> None:
        unsubscribe()

    _ = realtime.on_connect(remove_later_callback)
    unsubscribe = realtime.on_connect(received.append)
    realtime._enqueue_connection_callbacks("connect", RealtimeConnectContext())

    await asyncio.wait_for(realtime._connection_callback_queue.join(), timeout=2)

    assert received == []


@pytest.mark.parametrize(
    "failure", [RuntimeError("callback failed"), asyncio.CancelledError()]
)
async def test_connection_callback_failure_does_not_interrupt_later_callbacks(
    loop_errors: list[dict[str, object]], failure: BaseException
) -> None:
    realtime = VolcanoClient(anon_key="anon").realtime
    received: list[object] = []

    def fail(_context: object) -> None:
        raise failure

    _ = realtime.on_connect(fail)
    _ = realtime.on_connect(received.append)
    context = RealtimeConnectContext(client="connected")
    realtime._enqueue_connection_callbacks("connect", context)
    await asyncio.wait_for(realtime._connection_callback_queue.join(), timeout=2)

    assert received == [context]
    assert len(loop_errors) == 1
    assert loop_errors[0]["message"] == "Volcano realtime connection callback failed"
    assert loop_errors[0]["event"] == "connect"
    assert isinstance(loop_errors[0]["exception"], type(failure))


@pytest.mark.order(0)
async def test_dispatcher_failure_reports_the_channel_and_releases_the_task(
    monkeypatch: pytest.MonkeyPatch, loop_errors: list[dict[str, object]]
) -> None:
    realtime = VolcanoClient(anon_key="anon").realtime

    def ignore_message(_value: object) -> None:
        pass

    channel = realtime.channel("messages").on("message", ignore_message)
    failure = RuntimeError("dispatcher failed")

    async def fail(_delivery: _CallbackDelivery) -> None:
        raise failure

    monkeypatch.setattr(channel, "_dispatch_delivery", fail)
    await channel._emit("message", "first")
    await channel._emit("message", "second")
    assert channel._callback_queue.qsize() == 2
    task = channel._callback_task
    assert task is not None
    # A broken done callback can strand an awaiter even after this task finishes.
    for _ in range(10):
        if task.done():
            break
        await asyncio.sleep(0)
    assert task.done()
    with pytest.raises(RuntimeError, match="dispatcher failed"):
        task.result()
    await asyncio.sleep(0)
    await asyncio.wait_for(channel._callback_queue.join(), timeout=2)

    assert loop_errors == [
        {
            "message": "Volcano realtime callback dispatcher failed",
            "exception": failure,
            "channel": channel.name,
        }
    ]
    assert channel._callback_task is None
    assert realtime._callback_tasks == set()
    assert channel._callback_queue.empty()


async def test_stale_delivery_is_rejected_before_dispatch_and_callback_execution() -> (
    None
):
    client = VolcanoClient(
        anon_key="anon",
        access_token="access",
        _realtime_client_factory=FakeCentrifugeFactory(FakeCentrifugeClient()),
    )
    channel = client.realtime.channel("messages")
    received: list[object] = []
    _ = channel.on("message", received.append)
    try:
        await channel.subscribe()
        epoch = channel._delivery_epoch
        delivery = _CallbackDelivery("message", "obsolete", delivery_epoch=object())
        await channel._dispatch_delivery(delivery)
        await channel._run_callback(received.append, delivery)

        assert received == []

        await channel._dispatch_delivery(
            _CallbackDelivery("message", "current", delivery_epoch=epoch)
        )
        assert received == ["current"]
    finally:
        await client.realtime.disconnect()


async def test_callback_queued_before_first_unsubscribe_cannot_run_later() -> None:
    client = VolcanoClient(
        anon_key="anon",
        access_token="access",
        _realtime_client_factory=FakeCentrifugeFactory(FakeCentrifugeClient()),
    )
    channel = client.realtime.channel("messages")
    received: list[object] = []
    _ = channel.on("message", received.append)
    try:
        await channel.subscribe()
        queued = _CallbackDelivery(
            "message", "before unsubscribe", delivery_epoch=channel._delivery_epoch
        )
        await channel.unsubscribe()
        await channel._dispatch_delivery(queued)

        assert received == []
    finally:
        await client.realtime.disconnect()


@pytest.mark.parametrize(
    ("channel_type", "event"),
    [("broadcast", "message"), ("presence", "join")],
)
async def test_repeated_callback_invalidation_drops_intermediate_delivery(
    channel_type: ChannelType, event: str
) -> None:
    channel = VolcanoClient(anon_key="anon").realtime.channel(
        "messages", channel_type=channel_type
    )
    received: list[object] = []
    _ = channel.on(event, received.append)
    channel._paused = False
    presence_only = channel_type == "presence"
    channel._discard_callbacks(presence_only=presence_only)
    queued = _CallbackDelivery(
        event, "old connection", delivery_epoch=channel._callback_epoch(event)
    )
    channel._discard_callbacks(presence_only=presence_only)

    await channel._dispatch_delivery(queued)

    assert received == []


async def test_delivery_with_no_remaining_callback_is_safe() -> None:
    channel = VolcanoClient(anon_key="anon").realtime.channel("messages")
    channel._paused = False

    await channel._dispatch_delivery(
        _CallbackDelivery("message", "removed", delivery_epoch=channel._delivery_epoch)
    )


def test_presence_reconnect_invalidates_only_presence_callback_epochs() -> None:
    channel = VolcanoClient(anon_key="anon").realtime.channel(
        "lobby", channel_type="presence"
    )
    channel._paused = False
    pending = {
        event: _CallbackDelivery(
            event, object(), delivery_epoch=channel._callback_epoch(event)
        )
        for event in ("join", "leave", "presence_sync", "message")
    }

    channel._discard_callbacks(presence_only=True)

    for event in ("join", "leave", "presence_sync"):
        assert not channel._callback_delivery_is_current(pending[event])
    assert channel._callback_delivery_is_current(pending["message"])


def test_non_callable_connection_callback_is_rejected_at_runtime() -> None:
    realtime = VolcanoClient(anon_key="anon").realtime
    with pytest.raises(TypeError, match="callback must be callable"):
        register_non_callable(realtime)
