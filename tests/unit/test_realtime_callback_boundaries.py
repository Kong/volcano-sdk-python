from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest
from fixtures.invalid_realtime_callback import register_non_callable
from test_realtime import FakeCentrifugeClient, FakeCentrifugeFactory

from volcano_sdk import RealtimeConnectContext, VolcanoClient
from volcano_sdk.realtime import _CallbackDelivery

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


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
    channel = realtime.channel("messages").on("message", lambda _value: None)
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
