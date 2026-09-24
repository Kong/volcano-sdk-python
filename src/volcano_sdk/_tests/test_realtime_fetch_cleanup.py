from __future__ import annotations

import asyncio

import pytest
from typing_extensions import override

from volcano_sdk._realtime_fetch_worker import (
    PostgresFetchJob,
    PostgresFetchWorker,
    _StopWorker,
    _wait_for_close,
)

from .test_realtime_fetch_lifecycle import cancel_operation
from .test_realtime_fetch_worker import (
    BlockingRowFetch,
    OutcomeRecorder,
    RecordingBatchFetch,
    fetch_job,
)


class DelayedCancellation:
    def __init__(self) -> None:
        self.started: asyncio.Event = asyncio.Event()
        self.cancelled: asyncio.Event = asyncio.Event()
        self.release_cleanup: asyncio.Event = asyncio.Event()

    async def wait(self) -> None:
        self.started.set()
        try:
            _ = await asyncio.Event().wait()
        except asyncio.CancelledError:
            self.cancelled.set()
            _ = await self.release_cleanup.wait()
            raise


class CleanupQueue(asyncio.Queue[PostgresFetchJob[str] | _StopWorker]):
    def __init__(self) -> None:
        super().__init__(maxsize=1)
        self.started: asyncio.Event = asyncio.Event()
        self.cancelled: asyncio.Event = asyncio.Event()
        self.release_cleanup: asyncio.Event = asyncio.Event()

    @override
    async def put(self, item: PostgresFetchJob[str] | _StopWorker) -> None:
        self.started.set()
        try:
            await super().put(item)
        except asyncio.CancelledError:
            self.cancelled.set()
            _ = await self.release_cleanup.wait()
            raise


async def fail_worker() -> None:
    message = "delivery failed"
    raise RuntimeError(message)


async def test_close_waits_for_cancelled_stop_cleanup() -> None:
    stop = DelayedCancellation()
    stop_task = asyncio.create_task(stop.wait())
    task = asyncio.create_task(fail_worker())
    closing = asyncio.create_task(_wait_for_close(task, stop_task))
    try:
        _ = await asyncio.wait_for(stop.cancelled.wait(), timeout=1)
        await asyncio.sleep(0)
        assert not closing.done()
        stop.release_cleanup.set()
        with pytest.raises(RuntimeError, match="delivery failed"):
            await asyncio.wait_for(closing, timeout=1)
        assert stop_task.cancelled()
    finally:
        stop.release_cleanup.set()
        await cancel_operation(closing)
        await cancel_operation(stop_task)
        await cancel_operation(task)


async def test_cancelled_enqueue_waits_for_its_queue_put_cleanup() -> None:
    queue = CleanupQueue()
    queue.put_nowait(fetch_job(1))
    worker = PostgresFetchWorker(
        RecordingBatchFetch(), OutcomeRecorder(), queue_limit=1
    )
    worker._queue = queue
    waiting = DelayedCancellation()
    task = asyncio.create_task(waiting.wait())
    enqueueing = asyncio.create_task(worker._put_while_running(fetch_job(2), task))
    try:
        _ = await asyncio.wait_for(queue.started.wait(), timeout=1)
        _ = enqueueing.cancel()
        _ = await asyncio.wait_for(queue.cancelled.wait(), timeout=1)
        await asyncio.sleep(0)
        assert not enqueueing.done()
        queue.release_cleanup.set()
        with pytest.raises(asyncio.CancelledError):
            await asyncio.wait_for(enqueueing, timeout=1)
        assert queue.get_nowait() == fetch_job(1)
        assert queue.empty()
    finally:
        queue.release_cleanup.set()
        waiting.release_cleanup.set()
        if not queue.empty():
            _ = queue.get_nowait()
        await cancel_operation(enqueueing)
        await cancel_operation(task)


async def test_abort_cancels_an_outstanding_stop_request() -> None:
    fetch = BlockingRowFetch()
    worker = PostgresFetchWorker(fetch, OutcomeRecorder(), queue_limit=1)
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
        await cancel_operation(closing)
        await asyncio.wait_for(worker.abort(), timeout=1)
        assert stop_task.cancelled()
        assert fetch.cancelled.is_set()
    finally:
        fetch.release.set()
        await cancel_operation(closing)
        await asyncio.wait_for(worker.abort(), timeout=1)


async def test_closed_worker_rejects_jobs_before_abort() -> None:
    worker = PostgresFetchWorker(
        RecordingBatchFetch(), OutcomeRecorder(), queue_limit=1
    )
    try:
        await asyncio.wait_for(worker.close(), timeout=1)
        with pytest.raises(RuntimeError, match="fetch worker is closed"):
            await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=1)
    finally:
        await asyncio.wait_for(worker.abort(), timeout=1)


async def test_repeated_close_completes_all_queued_tasks() -> None:
    worker = PostgresFetchWorker(
        RecordingBatchFetch(),
        OutcomeRecorder(),
        queue_limit=2,
        batch_window_seconds=1,
        max_batch_size=2,
    )
    try:
        await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=1)
        await asyncio.wait_for(worker.enqueue(fetch_job(2)), timeout=1)
        await asyncio.wait_for(worker.close(), timeout=1)
        await asyncio.wait_for(worker.close(), timeout=1)
        await asyncio.wait_for(worker._queue.join(), timeout=1)
    finally:
        await asyncio.wait_for(worker.abort(), timeout=1)


async def test_batch_capacity_flushes_without_an_extra_row() -> None:
    fetch = RecordingBatchFetch()
    delivered = asyncio.Event()

    async def deliver(_outcome: object) -> None:
        delivered.set()

    worker = PostgresFetchWorker[str](
        fetch, deliver, queue_limit=3, max_batch_size=2, batch_window_seconds=60
    )
    try:
        await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=1)
        await asyncio.wait_for(worker.enqueue(fetch_job(2)), timeout=1)
        _ = await asyncio.wait_for(delivered.wait(), timeout=1)
        assert fetch.calls == [(1, 2)]
        await asyncio.wait_for(worker.enqueue(fetch_job(3)), timeout=1)
        await asyncio.wait_for(worker.close(), timeout=1)
        assert fetch.calls == [(1, 2), (3,)]
    finally:
        await asyncio.wait_for(worker.abort(), timeout=1)


async def test_expired_batch_deadline_preserves_queued_row(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worker = PostgresFetchWorker(
        RecordingBatchFetch(), OutcomeRecorder(), queue_limit=1
    )
    worker._queue.put_nowait(fetch_job(1))
    loop = asyncio.get_running_loop()
    with monkeypatch.context() as scoped:
        scoped.setattr(loop, "time", lambda: 42.0)
        assert await worker._next_before(42.0) is None
    assert worker._queue.get_nowait() == fetch_job(1)
