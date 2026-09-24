from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest
from test_realtime_fetch_worker import (
    BlockingRowFetch,
    OutcomeRecorder,
    RecordingBatchFetch,
    fetch_job,
)

from volcano_sdk._realtime_fetch_worker import PostgresFetchOutcome, PostgresFetchWorker

if TYPE_CHECKING:
    from volcano_sdk.realtime import _PostgresFetchRequest


async def cancel_operation(task: asyncio.Task[None] | None) -> None:
    if task is not None:
        _ = task.cancel()
        _ = await asyncio.gather(task, return_exceptions=True)


@pytest.mark.parametrize(
    ("window", "size", "message"),
    [
        (-1, 1, "batch_window_seconds cannot be negative"),
        (0, 0, "max_batch_size must be between 1 and queue_limit"),
        (0, 3, "max_batch_size must be between 1 and queue_limit"),
    ],
)
def test_worker_rejects_invalid_batch_configuration(
    window: float, size: int, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        _ = PostgresFetchWorker(
            RecordingBatchFetch(),
            OutcomeRecorder(),
            queue_limit=2,
            batch_window_seconds=window,
            max_batch_size=size,
        )


async def test_unused_worker_can_close_and_abort_repeatedly() -> None:
    fetch = RecordingBatchFetch()
    deliver = OutcomeRecorder()
    worker = PostgresFetchWorker(fetch, deliver, queue_limit=1)

    await worker.close()
    await worker.close()
    await asyncio.wait_for(worker.abort(), timeout=1)
    await asyncio.wait_for(worker.abort(), timeout=1)

    with pytest.raises(RuntimeError, match="fetch worker is closed"):
        await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=1)
    assert fetch.calls == []
    assert deliver.items == []


async def test_close_failure_cancels_a_blocked_stop_request() -> None:
    fetch = BlockingRowFetch()
    failure = RuntimeError("delivery failed")

    async def fail_delivery(_outcome: PostgresFetchOutcome[str]) -> None:
        raise failure

    worker = PostgresFetchWorker(fetch, fail_delivery, queue_limit=1)
    closing = None
    try:
        await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=1)
        _ = await asyncio.wait_for(fetch.started.wait(), timeout=1)
        await asyncio.wait_for(worker.enqueue(fetch_job(2)), timeout=1)
        closing = asyncio.create_task(worker.close())
        await asyncio.sleep(0)
        stop_task = worker._stop_task
        assert stop_task is not None
        assert not stop_task.done()
        fetch.release.set()

        with pytest.raises(RuntimeError, match="delivery failed") as caught:
            await asyncio.wait_for(closing, timeout=1)

        assert caught.value is failure
        assert stop_task.cancelled()
        assert fetch.row_ids == [1]
    finally:
        await asyncio.wait_for(worker.abort(), timeout=1)
        await cancel_operation(closing)


async def test_abort_unblocks_close_with_a_full_queue() -> None:
    fetch = BlockingRowFetch()
    deliver = OutcomeRecorder()
    worker = PostgresFetchWorker(fetch, deliver, queue_limit=1)
    closing = None
    try:
        await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=1)
        _ = await asyncio.wait_for(fetch.started.wait(), timeout=1)
        await asyncio.wait_for(worker.enqueue(fetch_job(2)), timeout=1)
        closing = asyncio.create_task(worker.close())
        await asyncio.sleep(0)
        stop_task = worker._stop_task
        assert stop_task is not None
        assert not stop_task.done()

        await asyncio.wait_for(worker.abort(), timeout=1)
        with pytest.raises(asyncio.CancelledError):
            await asyncio.wait_for(closing, timeout=1)
        await worker.close()

        assert stop_task.cancelled()
        assert fetch.cancelled.is_set()
        assert deliver.items == []
    finally:
        await asyncio.wait_for(worker.abort(), timeout=1)
        await cancel_operation(closing)


async def test_abort_rejects_an_enqueue_waiting_for_capacity() -> None:
    fetch = BlockingRowFetch()
    deliver = OutcomeRecorder()
    worker = PostgresFetchWorker(fetch, deliver, queue_limit=1)
    enqueueing = None
    try:
        await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=1)
        _ = await asyncio.wait_for(fetch.started.wait(), timeout=1)
        await asyncio.wait_for(worker.enqueue(fetch_job(2)), timeout=1)
        enqueueing = asyncio.create_task(worker.enqueue(fetch_job(3)))
        await asyncio.sleep(0)
        assert not enqueueing.done()

        await asyncio.wait_for(worker.abort(), timeout=1)
        with pytest.raises(RuntimeError, match="fetch worker is closed"):
            await asyncio.wait_for(enqueueing, timeout=1)

        assert fetch.cancelled.is_set()
        assert deliver.items == []
    finally:
        await asyncio.wait_for(worker.abort(), timeout=1)
        await cancel_operation(enqueueing)


@pytest.mark.parametrize("records", [(), ({"id": 1}, {"id": 2})])
async def test_wrong_batch_result_count_fails_before_delivery(
    records: tuple[dict[str, int], ...],
) -> None:
    release = asyncio.Event()

    async def malformed_results(
        _requests: tuple[_PostgresFetchRequest, ...],
    ) -> tuple[dict[str, int], ...]:
        _ = await release.wait()
        return records

    deliver = OutcomeRecorder()
    worker = PostgresFetchWorker(malformed_results, deliver, queue_limit=1)
    try:
        await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=1)
        release.set()
        with pytest.raises(RuntimeError, match="unexpected result count"):
            await asyncio.wait_for(worker.close(), timeout=1)
        assert deliver.items == []
    finally:
        await asyncio.wait_for(worker.abort(), timeout=1)


async def test_fetch_cancellation_propagates_without_delivering_a_fallback() -> None:
    started = asyncio.Event()
    release = asyncio.Event()

    async def cancelled_fetch(
        _requests: tuple[_PostgresFetchRequest, ...],
    ) -> tuple[dict[str, int], ...]:
        started.set()
        _ = await release.wait()
        raise asyncio.CancelledError

    deliver = OutcomeRecorder()
    worker = PostgresFetchWorker(cancelled_fetch, deliver, queue_limit=1)
    try:
        await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=1)
        _ = await asyncio.wait_for(started.wait(), timeout=1)
        release.set()

        with pytest.raises(asyncio.CancelledError):
            await asyncio.wait_for(worker.close(), timeout=1)

        assert deliver.items == []
    finally:
        await asyncio.wait_for(worker.abort(), timeout=1)


async def test_batch_window_flushes_without_waiting_for_another_row_or_close() -> None:
    fetch = RecordingBatchFetch()
    delivered = asyncio.Event()

    async def deliver(outcome: PostgresFetchOutcome[str]) -> None:
        assert outcome.record == {"id": 1}
        delivered.set()

    worker = PostgresFetchWorker(
        fetch, deliver, queue_limit=2, max_batch_size=2, batch_window_seconds=0.1
    )
    try:
        await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=1)
        _ = await asyncio.wait_for(delivered.wait(), timeout=1)
        await asyncio.wait_for(worker.close(), timeout=1)

        assert fetch.calls == [(1,)]
    finally:
        await asyncio.wait_for(worker.abort(), timeout=1)


@pytest.mark.parametrize(("window", "expected"), [(0, [(1,), (2,)]), (60, [(1, 2)])])
async def test_batch_capacity_and_zero_window_preserve_delivery_order(
    window: float, expected: list[tuple[int, ...]]
) -> None:
    fetch = RecordingBatchFetch()
    deliver = OutcomeRecorder()
    worker = PostgresFetchWorker(
        fetch, deliver, queue_limit=2, max_batch_size=2, batch_window_seconds=window
    )
    try:
        await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=1)
        await asyncio.wait_for(worker.enqueue(fetch_job(2)), timeout=1)
        await asyncio.wait_for(worker.close(), timeout=1)
        await asyncio.wait_for(worker.abort(), timeout=1)

        assert fetch.calls == expected
        assert [item.record for item in deliver.items] == [{"id": 1}, {"id": 2}]
    finally:
        await asyncio.wait_for(worker.abort(), timeout=1)


async def test_zero_batch_window_keeps_queued_followup_fetches_separate() -> None:
    first_fetch_started = asyncio.Event()
    release_first_fetch = asyncio.Event()
    recording_fetch = RecordingBatchFetch()

    async def fetch(
        requests: tuple[_PostgresFetchRequest, ...],
    ) -> tuple[dict[str, int], ...]:
        if requests[0].row_id == 1:
            first_fetch_started.set()
            _ = await release_first_fetch.wait()
        return await recording_fetch(requests)

    worker = PostgresFetchWorker(
        fetch,
        OutcomeRecorder(),
        queue_limit=3,
        max_batch_size=3,
    )
    try:
        await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=1)
        _ = await asyncio.wait_for(first_fetch_started.wait(), timeout=0.2)
        await asyncio.wait_for(worker.enqueue(fetch_job(2)), timeout=1)
        await asyncio.wait_for(worker.enqueue(fetch_job(3)), timeout=1)
        release_first_fetch.set()
        await asyncio.wait_for(worker.close(), timeout=1)

        assert recording_fetch.calls == [(1,), (2,), (3,)]
    finally:
        await asyncio.wait_for(worker.abort(), timeout=1)
