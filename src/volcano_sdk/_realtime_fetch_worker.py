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


@dataclass(frozen=True, slots=True)
class PostgresFetchJob(Generic[FallbackT]):
    """Pair a captured row request with its lightweight fallback."""

    request: _PostgresFetchRequest
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
        fetch: Callable[[_PostgresFetchRequest], PostgresRecord | None],
        deliver: Callable[[PostgresFetchOutcome[FallbackT]], Awaitable[None]],
        *,
        queue_limit: int,
    ) -> None:
        """Create a worker with a fixed pending-job limit."""
        if queue_limit <= 0:
            raise ValueError(_INVALID_QUEUE_LIMIT)
        self._fetch = fetch
        self._deliver = deliver
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
            if not self._closed:
                self._closed = True
            self._raise_worker_failure()
            if task is not None and self._stop_task is None:
                self._stop_task = asyncio.create_task(self._queue.put(_STOP_WORKER))
            stop_task = self._stop_task
        if task is not None and stop_task is not None:
            await self._wait_for_close(task, stop_task)

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
            task.result()
        await put_task

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
        while True:
            item = await self._queue.get()
            try:
                if isinstance(item, _StopWorker):
                    return
                await self._fetch_and_deliver(item)
            finally:
                self._queue.task_done()

    async def _fetch_and_deliver(self, job: PostgresFetchJob[FallbackT]) -> None:
        (result,) = await asyncio.gather(
            asyncio.to_thread(self._fetch, job.request),
            return_exceptions=True,
        )
        if isinstance(result, BaseException):
            if not isinstance(result, Exception):
                raise result
            outcome = PostgresFetchOutcome(job=job, error=result)
        else:
            outcome = PostgresFetchOutcome(job=job, record=result)
        await self._deliver(outcome)
