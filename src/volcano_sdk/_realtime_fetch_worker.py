"""Bounded, ordered row fetching for realtime Postgres changes."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic, TypeVar

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from .realtime import _PostgresFetchRequest

FallbackT = TypeVar("FallbackT")
PostgresRecord = dict[str, Any]
_WORKER_CLOSED = "Postgres fetch worker is closed"
_INVALID_QUEUE_LIMIT = "queue_limit must be positive"
_INVALID_BATCH_WINDOW = "batch_window_seconds cannot be negative"
_INVALID_BATCH_SIZE = "max_batch_size must be between 1 and queue_limit"
_INVALID_RESULT_COUNT = "Postgres fetch returned an unexpected result count"


@dataclass(frozen=True, slots=True)
class PostgresFetchJob(Generic[FallbackT]):
    """Pair a captured row request with its lightweight fallback."""

    request: _PostgresFetchRequest | None
    fallback: FallbackT


@dataclass(frozen=True, slots=True)
class PostgresFetchOutcome(Generic[FallbackT]):
    """Describe either a fetched record or a failed fetch."""

    job: PostgresFetchJob[FallbackT]
    record: PostgresRecord | None = None
    error: Exception | None = None


@dataclass(frozen=True, slots=True)
class _StopWorker:
    pass


_STOP_WORKER = _StopWorker()


class PostgresFetchWorker(Generic[FallbackT]):
    """Fetch queued rows serially and deliver outcomes in enqueue order."""

    def __init__(
        self,
        fetch: Callable[
            [tuple[_PostgresFetchRequest, ...]],
            Awaitable[tuple[PostgresRecord | None, ...]],
        ],
        deliver: Callable[[PostgresFetchOutcome[FallbackT]], Awaitable[None]],
        *,
        queue_limit: int,
        batch_window_seconds: float = 0,
        max_batch_size: int = 1,
    ) -> None:
        """Create a worker with a fixed pending-job limit."""
        if queue_limit <= 0:
            raise ValueError(_INVALID_QUEUE_LIMIT)
        if batch_window_seconds < 0:
            raise ValueError(_INVALID_BATCH_WINDOW)
        if not 1 <= max_batch_size <= queue_limit:
            raise ValueError(_INVALID_BATCH_SIZE)
        self._fetch = fetch
        self._deliver = deliver
        self._batch_window_seconds = batch_window_seconds
        self._max_batch_size = max_batch_size
        self._queue: asyncio.Queue[PostgresFetchJob[FallbackT] | _StopWorker] = (
            asyncio.Queue(maxsize=queue_limit)
        )
        self._state_lock = asyncio.Lock()
        self._task: asyncio.Task[None] | None = None
        self._stop_task: asyncio.Task[None] | None = None
        self._closed = False

    async def enqueue(self, job: PostgresFetchJob[FallbackT]) -> None:
        """Queue one fetch, applying backpressure when the queue is full."""
        async with self._state_lock:
            if self._closed:
                raise RuntimeError(_WORKER_CLOSED)
            self._raise_worker_failure()
            if self._task is None:
                self._task = asyncio.create_task(self._run())
            await self._put_while_running(job, self._task)

    async def close(self) -> None:
        """Drain accepted jobs and stop the worker."""
        async with self._state_lock:
            task = self._task
            if self._closed and (task is None or task.cancelled()):
                return
            if not self._closed:
                self._closed = True
            self._raise_worker_failure()
            if task is not None and self._stop_task is None:
                self._stop_task = asyncio.create_task(self._queue.put(_STOP_WORKER))
            stop_task = self._stop_task
        if task is not None and stop_task is not None:
            await self._wait_for_close(task, stop_task)

    async def abort(self) -> None:
        """Discard obsolete jobs and stop without waiting for row fetches."""
        self._closed = True
        task = self._task
        stop_task = self._stop_task
        if stop_task is not None and not stop_task.done():
            stop_task.cancel()
        if task is not None and not task.done():
            task.cancel()
        pending = tuple(
            candidate for candidate in (task, stop_task) if candidate is not None
        )
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)
        self._discard_pending()

    def _raise_worker_failure(self) -> None:
        task = self._task
        if task is not None and task.done():
            task.result()

    async def _put_while_running(
        self,
        job: PostgresFetchJob[FallbackT],
        task: asyncio.Task[None],
    ) -> None:
        put_task = asyncio.create_task(self._queue.put(job))
        try:
            completed, _pending = await asyncio.wait(
                (task, put_task),
                return_when=asyncio.FIRST_COMPLETED,
            )
        finally:
            if not put_task.done():
                put_task.cancel()
                await asyncio.gather(put_task, return_exceptions=True)
        if task in completed:
            if task.cancelled():
                raise RuntimeError(_WORKER_CLOSED)
            task.result()
        await put_task

    def _discard_pending(self) -> None:
        while not self._queue.empty():
            self._queue.get_nowait()
            self._queue.task_done()

    async def _wait_for_close(
        self,
        task: asyncio.Task[None],
        stop_task: asyncio.Task[None],
    ) -> None:
        completed, _pending = await asyncio.wait(
            (task, stop_task),
            return_when=asyncio.FIRST_COMPLETED,
        )
        if task in completed:
            try:
                task.result()
            except BaseException:
                stop_task.cancel()
                await asyncio.gather(stop_task, return_exceptions=True)
                raise
        await asyncio.shield(stop_task)
        await asyncio.shield(task)

    async def _run(self) -> None:
        pending: PostgresFetchJob[FallbackT] | _StopWorker | None = None
        while True:
            item = pending if pending is not None else await self._queue.get()
            pending = None
            batch: list[PostgresFetchJob[FallbackT]] = []
            try:
                if isinstance(item, _StopWorker):
                    return
                batch.append(item)
                pending = await self._collect_batch(batch)
                await self._fetch_and_deliver(batch)
            finally:
                self._queue.task_done()
                for _job in batch[1:]:
                    self._queue.task_done()

    async def _collect_batch(
        self,
        batch: list[PostgresFetchJob[FallbackT]],
    ) -> PostgresFetchJob[FallbackT] | _StopWorker | None:
        first_request = batch[0].request
        if first_request is None or self._max_batch_size == 1:
            return None
        deadline = asyncio.get_running_loop().time() + self._batch_window_seconds
        while len(batch) < self._max_batch_size:
            remaining = deadline - asyncio.get_running_loop().time()
            if remaining <= 0:
                return None
            try:
                async with asyncio.timeout(remaining):
                    candidate = await self._queue.get()
            except TimeoutError:
                return None
            if isinstance(candidate, _StopWorker):
                return candidate
            request = candidate.request
            if (
                request is None
                or not self._same_fetch(first_request, request)
                or self._repeats_row(batch, request)
            ):
                return candidate
            batch.append(candidate)
        return None

    @staticmethod
    def _same_fetch(
        first: _PostgresFetchRequest,
        request: _PostgresFetchRequest,
    ) -> bool:
        return (
            first.database_name,
            first.access_token,
            first.table,
        ) == (
            request.database_name,
            request.access_token,
            request.table,
        )

    @staticmethod
    def _repeats_row(
        batch: list[PostgresFetchJob[FallbackT]],
        request: _PostgresFetchRequest,
    ) -> bool:
        return any(
            job.request is not None and job.request.row_id == request.row_id
            for job in batch
        )

    async def _fetch_and_deliver(
        self,
        jobs: list[PostgresFetchJob[FallbackT]],
    ) -> None:
        requests = tuple(job.request for job in jobs if job.request is not None)
        if not requests:
            await self._deliver(PostgresFetchOutcome(job=jobs[0]))
            return
        (result,) = await asyncio.gather(
            self._fetch(requests),
            return_exceptions=True,
        )
        if isinstance(result, BaseException):
            if not isinstance(result, Exception):
                raise result
            for job in jobs:
                await self._deliver(PostgresFetchOutcome(job=job, error=result))
            return
        if len(result) != len(jobs):
            raise RuntimeError(_INVALID_RESULT_COUNT)
        for job, record in zip(jobs, result, strict=True):
            await self._deliver(PostgresFetchOutcome(job=job, record=record))
