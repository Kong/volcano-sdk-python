from __future__ import annotations

import asyncio
import gc
import weakref
from typing import TYPE_CHECKING

import pytest
from test_realtime_fetch_worker import (
    BlockingRowFetch,
    OutcomeRecorder,
    RecordingBatchFetch,
    fetch_job,
    passthrough_job,
)
from typing_extensions import override

from volcano_sdk._realtime_fetch_worker import (
    PostgresFetchJob,
    PostgresFetchOutcome,
    PostgresFetchWorker,
    _StopWorker,
    _wait_for_close,
)

if TYPE_CHECKING:
    from volcano_sdk.realtime import _PostgresFetchRequest


async def cancel_operation(task: asyncio.Task[None] | None) -> None:
    if task is not None:
        _ = task.cancel()
        _ = await asyncio.gather(task, return_exceptions=True)


class CancellationAwareQueue(asyncio.Queue[PostgresFetchJob[str] | _StopWorker]):
    def __init__(self) -> None:
        super().__init__(maxsize=1)
        self.cancelled = asyncio.Event()
        self.release = asyncio.Event()
        self.pending_put: asyncio.Task[None] | None = None

    @override
    async def put(self, item: PostgresFetchJob[str] | _StopWorker) -> None:
        self.pending_put = asyncio.current_task()
        try:
            await super().put(item)
        except asyncio.CancelledError:
            self.cancelled.set()
            _ = await self.release.wait()
            raise


@pytest.mark.order(0)
async def test_successful_batch_delivers_each_result() -> None:
    fetch = RecordingBatchFetch()
    deliver = OutcomeRecorder()
    worker = PostgresFetchWorker(fetch, deliver, queue_limit=2)
    jobs = [fetch_job(1), fetch_job(2)]

    await asyncio.wait_for(worker._fetch_and_deliver(jobs), timeout=1)

    assert fetch.calls == [(1, 2)]
    assert deliver.items == [
        PostgresFetchOutcome(job=jobs[0], record={"id": 1}),
        PostgresFetchOutcome(job=jobs[1], record={"id": 2}),
    ]


async def test_failed_close_waits_for_stop_task_cleanup() -> None:
    failure = RuntimeError("worker failed")
    cancellation_seen = asyncio.Event()
    cleanup_release = asyncio.Event()

    async def fail() -> None:
        raise failure

    async def stop() -> None:
        try:
            _ = await asyncio.Event().wait()
        except asyncio.CancelledError:
            cancellation_seen.set()
            _ = await cleanup_release.wait()
            raise

    worker_task = asyncio.create_task(fail())
    stop_task = asyncio.create_task(stop())
    waiter = asyncio.create_task(_wait_for_close(worker_task, stop_task))
    try:
        _ = await asyncio.wait_for(cancellation_seen.wait(), timeout=1)
        assert not waiter.done()
        cleanup_release.set()
        with pytest.raises(RuntimeError, match="worker failed") as caught:
            await asyncio.wait_for(waiter, timeout=1)
        assert caught.value is failure
        assert stop_task.done()
    finally:
        cleanup_release.set()
        await cancel_operation(waiter)
        await cancel_operation(stop_task)


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
    assert worker._stop_task is None
    assert worker._queue.empty()
    await worker.close()
    await asyncio.wait_for(worker.abort(), timeout=1)
    await asyncio.wait_for(worker.abort(), timeout=1)

    with pytest.raises(RuntimeError, match="fetch worker is closed"):
        await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=1)
    assert fetch.calls == []
    assert deliver.items == []


async def test_closed_worker_rejects_new_jobs_before_abort() -> None:
    worker = PostgresFetchWorker(
        RecordingBatchFetch(), OutcomeRecorder(), queue_limit=1
    )
    await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=1)
    await asyncio.wait_for(worker.close(), timeout=1)

    with pytest.raises(RuntimeError, match="fetch worker is closed"):
        await asyncio.wait_for(worker.enqueue(fetch_job(2)), timeout=1)


async def test_abort_cancels_an_active_fetch() -> None:
    fetch = BlockingRowFetch()
    worker = PostgresFetchWorker(fetch, OutcomeRecorder(), queue_limit=1)
    aborting: asyncio.Task[None] | None = None
    try:
        await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=1)
        _ = await asyncio.wait_for(fetch.started.wait(), timeout=1)
        aborting = asyncio.create_task(worker.abort())
        _ = await asyncio.wait_for(fetch.cancelled.wait(), timeout=0.5)
        await asyncio.wait_for(aborting, timeout=1)
    finally:
        fetch.release.set()
        await cancel_operation(aborting)
        await asyncio.wait_for(worker.abort(), timeout=1)


async def test_cancelled_enqueue_waits_for_its_queue_put_to_finish() -> None:
    fetch = BlockingRowFetch()
    worker = PostgresFetchWorker(fetch, OutcomeRecorder(), queue_limit=1)
    queue = CancellationAwareQueue()
    worker._queue = queue
    enqueueing: asyncio.Task[None] | None = None
    try:
        await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=1)
        _ = await asyncio.wait_for(fetch.started.wait(), timeout=1)
        await asyncio.wait_for(worker.enqueue(fetch_job(2)), timeout=1)
        enqueueing = asyncio.create_task(worker.enqueue(fetch_job(3)))
        await asyncio.sleep(0)
        assert not enqueueing.done()

        _ = enqueueing.cancel()
        _ = await asyncio.wait_for(queue.cancelled.wait(), timeout=0.5)
        assert not enqueueing.done()
        queue.release.set()
        with pytest.raises(asyncio.CancelledError):
            await asyncio.wait_for(enqueueing, timeout=1)
    finally:
        queue.release.set()
        await cancel_operation(queue.pending_put)
        await cancel_operation(enqueueing)
        await asyncio.wait_for(worker.abort(), timeout=1)


async def test_enqueue_rejects_cancellation_after_queue_put_completes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worker = PostgresFetchWorker(
        RecordingBatchFetch(), OutcomeRecorder(), queue_limit=1
    )

    async def wait_forever() -> None:
        _ = await asyncio.Event().wait()

    task = asyncio.create_task(wait_forever())

    async def cancel_after_put(
        worker_task: asyncio.Task[None], put_task: asyncio.Task[None]
    ) -> None:
        await put_task
        _ = worker_task.cancel()
        _ = await asyncio.gather(worker_task, return_exceptions=True)

    monkeypatch.setattr(worker, "_await_put_or_worker", cancel_after_put)
    try:
        with pytest.raises(RuntimeError, match="fetch worker is closed"):
            await worker._put_while_running(fetch_job(1), task)
    finally:
        await cancel_operation(task)


async def test_enqueues_release_completion_callbacks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fetch = BlockingRowFetch()
    worker = PostgresFetchWorker(fetch, OutcomeRecorder(), queue_limit=1)
    loop = asyncio.get_running_loop()
    create_future = loop.create_future
    created: list[weakref.ReferenceType[asyncio.Future[None]]] = []

    def track_future() -> asyncio.Future[None]:
        future: asyncio.Future[None] = create_future()
        created.append(weakref.ref(future))
        return future

    try:
        await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=1)
        _ = await asyncio.wait_for(fetch.started.wait(), timeout=1)
        with monkeypatch.context() as patch:
            patch.setattr(loop, "create_future", track_future)
            async with asyncio.timeout(1):
                await worker.enqueue(fetch_job(2))

        await asyncio.sleep(0)
        _ = gc.collect()
        assert len(created) == 1
        assert created[0]() is None
    finally:
        await asyncio.wait_for(worker.abort(), timeout=1)


@pytest.mark.order(0)
async def test_race_helper_handles_two_already_completed_tasks() -> None:
    async def complete() -> None:
        return

    task = asyncio.create_task(complete())
    put_task = asyncio.create_task(complete())
    _ = await asyncio.gather(task, put_task)

    await asyncio.wait_for(
        PostgresFetchWorker._await_put_or_worker(task, put_task), timeout=1
    )


async def test_first_enqueue_finishes_before_worker_shutdown() -> None:
    worker = PostgresFetchWorker(
        RecordingBatchFetch(), OutcomeRecorder(), queue_limit=1
    )
    try:
        await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=0.5)
        assert worker._task is not None
        assert not worker._task.done()
    finally:
        await asyncio.wait_for(worker.abort(), timeout=1)


async def test_known_worker_failure_does_not_schedule_a_stop_request() -> None:
    failure = RuntimeError("delivery failed")
    delivery_started = asyncio.Event()
    release_delivery = asyncio.Event()

    async def fail_delivery(_outcome: PostgresFetchOutcome[str]) -> None:
        delivery_started.set()
        _ = await release_delivery.wait()
        raise failure

    worker = PostgresFetchWorker(RecordingBatchFetch(), fail_delivery, queue_limit=1)
    try:
        await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=1)
        _ = await asyncio.wait_for(delivery_started.wait(), timeout=1)
        release_delivery.set()
        assert worker._task is not None
        _ = await asyncio.gather(worker._task, return_exceptions=True)

        with pytest.raises(RuntimeError, match="delivery failed") as caught:
            await asyncio.wait_for(worker.close(), timeout=1)
        assert caught.value is failure
        assert worker._stop_task is None
    finally:
        release_delivery.set()
        await asyncio.wait_for(worker.abort(), timeout=1)


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


async def test_wrong_batch_result_count_fails_before_delivery() -> None:
    release = asyncio.Event()

    async def no_results(
        _requests: tuple[_PostgresFetchRequest, ...],
    ) -> tuple[dict[str, int], ...]:
        _ = await release.wait()
        return ()

    deliver = OutcomeRecorder()
    worker = PostgresFetchWorker(no_results, deliver, queue_limit=1)
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


async def test_default_batch_window_flushes_before_another_row_arrives() -> None:
    fetch = RecordingBatchFetch()
    delivered = asyncio.Event()

    async def deliver(_outcome: PostgresFetchOutcome[str]) -> None:
        delivered.set()

    worker = PostgresFetchWorker(fetch, deliver, queue_limit=2, max_batch_size=2)
    try:
        await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=1)
        _ = await asyncio.wait_for(delivered.wait(), timeout=0.5)
        await asyncio.wait_for(worker.enqueue(fetch_job(2)), timeout=1)
        await asyncio.wait_for(worker.close(), timeout=1)

        assert fetch.calls == [(1,), (2,)]
    finally:
        await asyncio.wait_for(worker.abort(), timeout=1)


async def test_full_batch_flushes_before_close() -> None:
    fetch = RecordingBatchFetch()
    delivered = asyncio.Event()
    outcomes: list[PostgresFetchOutcome[str]] = []

    async def deliver(outcome: PostgresFetchOutcome[str]) -> None:
        outcomes.append(outcome)
        if len(outcomes) == 2:
            delivered.set()

    worker = PostgresFetchWorker(
        fetch, deliver, queue_limit=2, max_batch_size=2, batch_window_seconds=60
    )
    try:
        await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=1)
        await asyncio.wait_for(worker.enqueue(fetch_job(2)), timeout=1)
        _ = await asyncio.wait_for(delivered.wait(), timeout=1)
        await asyncio.wait_for(worker.close(), timeout=1)
        await asyncio.wait_for(worker._queue.join(), timeout=1)

        assert fetch.calls == [(1, 2)]
        assert outcomes == [
            PostgresFetchOutcome(job=fetch_job(1), record={"id": 1}),
            PostgresFetchOutcome(job=fetch_job(2), record={"id": 2}),
        ]
    finally:
        await asyncio.wait_for(worker.abort(), timeout=1)


async def test_passthrough_does_not_enter_a_fetch_batch() -> None:
    fetch = RecordingBatchFetch()
    deliver = OutcomeRecorder()
    worker = PostgresFetchWorker(
        fetch, deliver, queue_limit=2, max_batch_size=2, batch_window_seconds=0.01
    )
    try:
        await asyncio.wait_for(
            worker.enqueue(passthrough_job("full-payload")), timeout=1
        )
        await asyncio.wait_for(worker.enqueue(fetch_job(1)), timeout=1)
        await asyncio.wait_for(worker.close(), timeout=1)

        assert fetch.calls == [(1,)]
        assert deliver.items == [
            PostgresFetchOutcome(job=passthrough_job("full-payload")),
            PostgresFetchOutcome(job=fetch_job(1), record={"id": 1}),
        ]
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
