from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


@contextmanager
def worker_pool(
    max_workers: int | None = None, thread_name_prefix: str = ""
) -> Generator[ThreadPoolExecutor]:
    """Run concurrent test calls without an unbounded join on exit.

    ``ThreadPoolExecutor.__exit__`` joins every worker without a timeout, so a
    defect that leaves one waiting turns the test's bounded assertion into a
    hang. Tests bound every ``Future`` wait instead. The executor keeps each
    call's exception in its future rather than reporting it after the test.

    Yields:
        An executor that is shut down without waiting when the context exits.
    """
    pool = ThreadPoolExecutor(max_workers, thread_name_prefix)
    try:
        yield pool
    finally:
        pool.shutdown(wait=False, cancel_futures=True)
