"""Immutable batch outcomes from the durable runtime."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic

from typing_extensions import TypeVar

if TYPE_CHECKING:
    from ._durable_protocols import RuntimeBatch, RuntimeBatchItem

T = TypeVar("T", default=object)


@dataclass(frozen=True, slots=True)
class BatchFailure:
    """Why one item of a batch failed.

    The platform reports a failed item as its own wire object, which this
    reduces to the three fields worth reading: what went wrong, how the
    platform classified it, and whatever the failure carried with it. A handler
    logs or returns those.

    `throw_if_failed` raises the real error, for a handler that would rather
    propagate the failure than report it.
    """

    message: str | None
    type: str | None = None
    data: str | None = None


@dataclass(frozen=True, slots=True)
class BatchItem(Generic[T]):
    """One item's outcome in a `map` or `parallel` batch."""

    index: int
    status: str
    result: T | None = None
    error: BatchFailure | None = None


class BatchResult(Generic[T]):
    """The outcome of a `map` or `parallel` batch.

    Reduced to plain data from the engine's own result, which carries methods
    and enum-valued statuses: a batch is usually inspected, logged, and
    returned from the handler, so a JSON-serializable shape is worth more here
    than the engine's convenience methods.

    Only the parts that survive a replay are carried over. A batch that
    finishes early -- `min_succeeded` reached, say -- leaves items still in
    flight, and the platform does not promise to reproduce those when the
    execution resumes: the in-flight entries and the total it counted live can
    both come back different. A handler branching on one would take a different
    path the second time through, which is the thing durable execution exists
    to rule out. So `items` holds the items that finished, `completed` counts
    them, and `completion_reason` says why the batch ended.
    """

    __slots__: tuple[str, ...] = (
        "_batch",
        "completed",
        "completion_reason",
        "errors",
        "failed",
        "items",
        "results",
        "succeeded",
    )

    def __init__(self, batch: RuntimeBatch[T]) -> None:
        """Flatten an engine batch result."""
        self._batch: RuntimeBatch[T] = batch
        self.items: tuple[BatchItem[T], ...] = tuple(
            BatchItem(
                index=item.index,
                status=str(getattr(item.status, "value", item.status)).lower(),
                result=item.result,
                error=_batch_failure(item.error),
            )
            for item in _batch_items(batch)
        )
        # Only the items that succeeded, so not aligned with the input when
        # some failed.
        self.results: tuple[T, ...] = tuple(batch.get_results())
        self.errors: tuple[BatchFailure, ...] = tuple(
            failure
            for failure in (_batch_failure(error) for error in batch.get_errors())
            if failure is not None
        )
        self.succeeded: int = batch.success_count
        self.failed: int = batch.failure_count
        self.completed: int = batch.success_count + batch.failure_count
        self.completion_reason: str | None = completion_reason(batch)

    def throw_if_failed(self) -> None:
        """Raise the first failure, if there was one."""
        self._batch.throw_if_error()


def _batch_items(batch: RuntimeBatch[T]) -> list[RuntimeBatchItem[T]]:
    """List the items that finished, in input order.

    The in-flight ones are left out on purpose: see `BatchResult`.

    Returns:
        Succeeded and failed items sorted by their input index.

    """
    items = [*batch.succeeded(), *batch.failed()]
    return sorted(items, key=lambda item: item.index)


def _batch_failure(error: object) -> BatchFailure | None:
    if error is None:
        return None
    return BatchFailure(
        message=getattr(error, "message", None) or str(error),
        type=getattr(error, "type", None),
        data=getattr(error, "data", None),
    )


def completion_reason(batch: object) -> str | None:
    """Read the optional completion reason from a runtime batch.

    Returns:
        The normalized status, or None if it is absent.

    """
    reason: object = getattr(batch, "completion_reason", None)
    if reason is None:
        return None
    return str(getattr(reason, "value", reason)).lower()
