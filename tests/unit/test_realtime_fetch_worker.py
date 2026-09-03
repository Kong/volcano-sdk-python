from __future__ import annotations

import asyncio
import threading
from contextlib import suppress
from typing import Any

import pytest

from volcano_sdk import realtime as realtime_module
from volcano_sdk._realtime_fetch_worker import (
    PostgresFetchJob,
    PostgresFetchOutcome,
    PostgresFetchWorker,
)


class BlockingRowFetch:
    def __init__(self) -> None:
        self.started = threading.Event()
        self.release = threading.Event()
        self.row_ids: list[int] = []

    def __call__(
        self,
        request: realtime_module._PostgresFetchRequest,
    ) -> dict[str, Any]:
        row_id = request.row_id
        assert isinstance(row_id, int)
        self.row_ids.append(row_id)
        if row_id == 1:
            self.started.set()
            if not self.release.wait(timeout=1):
                message = "blocked row fetch was not released"
                raise TimeoutError(message)
        return {"id": row_id}


class FailingThenSuccessfulFetch:
    def __init__(self, failure: Exception) -> None:
        self.failure = failure

    def __call__(
        self,
        request: realtime_module._PostgresFetchRequest,
    ) -> dict[str, Any]:
        row_id = request.row_id
        assert isinstance(row_id, int)
        if row_id == 1:
            raise self.failure
        return {"id": row_id}


def fetch_job(row_id: int) -> PostgresFetchJob[str]:
    return PostgresFetchJob(
        request=realtime_module._PostgresFetchRequest(
            database_name="app",
            access_token="captured-token",
            table="messages",
            row_id=row_id,
        ),
        fallback=f"lightweight-{row_id}",
    )


async def wait_for_thread(event: threading.Event) -> None:
    assert await asyncio.to_thread(event.wait, 0.2)


def test_postgres_fetch_worker_bounds_and_orders_fetches() -> None:
    async def scenario() -> None:
        fetch = BlockingRowFetch()
        outcomes: list[PostgresFetchOutcome[str]] = []

        async def deliver(outcome: PostgresFetchOutcome[str]) -> None:
            outcomes.append(outcome)

        worker = PostgresFetchWorker(fetch, deliver, queue_limit=1)
        await worker.enqueue(fetch_job(1))
        await wait_for_thread(fetch.started)
        await worker.enqueue(fetch_job(2))
        third_enqueue = asyncio.create_task(worker.enqueue(fetch_job(3)))
        await asyncio.sleep(0)

        assert not third_enqueue.done()

        fetch.release.set()
        await asyncio.wait_for(third_enqueue, timeout=0.2)
        await asyncio.wait_for(worker.close(), timeout=0.2)

        assert fetch.row_ids == [1, 2, 3]
        assert [outcome.record for outcome in outcomes] == [
            {"id": 1},
            {"id": 2},
            {"id": 3},
        ]
        assert [outcome.job.fallback for outcome in outcomes] == [
            "lightweight-1",
            "lightweight-2",
            "lightweight-3",
        ]

    asyncio.run(scenario())


def test_postgres_fetch_worker_rejects_an_unbounded_queue() -> None:
    async def deliver(_outcome: PostgresFetchOutcome[str]) -> None:
        return None

    with pytest.raises(ValueError, match="queue_limit must be positive"):
        PostgresFetchWorker(BlockingRowFetch(), deliver, queue_limit=0)


def test_postgres_fetch_worker_delivers_fallback_and_continues_after_failure() -> None:
    async def scenario() -> None:
        failure = RuntimeError("database unavailable")
        outcomes: list[PostgresFetchOutcome[str]] = []

        async def deliver(outcome: PostgresFetchOutcome[str]) -> None:
            outcomes.append(outcome)

        worker = PostgresFetchWorker(
            FailingThenSuccessfulFetch(failure),
            deliver,
            queue_limit=2,
        )
        await worker.enqueue(fetch_job(1))
        await worker.enqueue(fetch_job(2))
        await asyncio.wait_for(worker.close(), timeout=0.2)

        assert outcomes == [
            PostgresFetchOutcome(job=fetch_job(1), error=failure),
            PostgresFetchOutcome(job=fetch_job(2), record={"id": 2}),
        ]

    asyncio.run(scenario())


def test_postgres_fetch_worker_rejects_work_after_delivery_failure() -> None:
    async def scenario() -> None:
        failure = RuntimeError("delivery failed")
        delivery_started = asyncio.Event()

        async def fail_delivery(_outcome: PostgresFetchOutcome[str]) -> None:
            delivery_started.set()
            raise failure

        worker = PostgresFetchWorker(
            BlockingRowFetch(),
            fail_delivery,
            queue_limit=1,
        )
        await worker.enqueue(fetch_job(2))
        await delivery_started.wait()
        await asyncio.sleep(0)

        with pytest.raises(RuntimeError) as raised:
            await worker.enqueue(fetch_job(3))

        assert raised.value is failure

    asyncio.run(scenario())


def test_postgres_fetch_worker_recovers_from_cancelled_close() -> None:
    async def scenario() -> None:
        fetch = BlockingRowFetch()
        outcomes: list[PostgresFetchOutcome[str]] = []

        async def deliver(outcome: PostgresFetchOutcome[str]) -> None:
            outcomes.append(outcome)

        worker = PostgresFetchWorker(fetch, deliver, queue_limit=1)
        await worker.enqueue(fetch_job(1))
        await wait_for_thread(fetch.started)
        await worker.enqueue(fetch_job(2))

        interrupted_close = asyncio.create_task(worker.close())
        await asyncio.sleep(0)
        interrupted_close.cancel()
        with suppress(asyncio.CancelledError):
            await interrupted_close

        fetch.release.set()
        try:
            await asyncio.wait_for(worker.close(), timeout=0.2)
        finally:
            task = worker._task
            if task is not None and not task.done():
                task.cancel()
                await asyncio.gather(task, return_exceptions=True)

        assert [outcome.record for outcome in outcomes] == [{"id": 1}, {"id": 2}]

    asyncio.run(scenario())
