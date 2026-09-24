"""Structural interfaces implemented by the optional durable runtime."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from typing_extensions import TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from ._durable_options import BatchOptions, Retry, WaitUntilOptions

T = TypeVar("T", default=object)
U = TypeVar("U", default=object)


class DurableLogger(Protocol):
    """Replay-aware logging methods exposed by durable contexts and steps."""

    def debug(
        self, msg: object, *args: object, extra: Mapping[str, object] | None = None
    ) -> None:
        """Log a debug message unless the operation is replaying."""
        ...

    def info(
        self, msg: object, *args: object, extra: Mapping[str, object] | None = None
    ) -> None:
        """Log an informational message unless the operation is replaying."""
        ...

    def warning(
        self, msg: object, *args: object, extra: Mapping[str, object] | None = None
    ) -> None:
        """Log a warning unless the operation is replaying."""
        ...

    def error(
        self, msg: object, *args: object, extra: Mapping[str, object] | None = None
    ) -> None:
        """Log an error unless the operation is replaying."""
        ...

    def exception(
        self, msg: object, *args: object, extra: Mapping[str, object] | None = None
    ) -> None:
        """Log an exception unless the operation is replaying."""
        ...


class DurableEngine(Protocol):
    """The operations the Volcano facade needs from the optional runtime."""

    def seconds(self, value: int) -> object: ...

    def step_options(self, *, retry: Retry, at_most_once: bool) -> object: ...

    def wait_condition_options(self, options: WaitUntilOptions[T]) -> object: ...

    def map_options(self, options: BatchOptions | None) -> object: ...

    def parallel_options(self, options: BatchOptions | None) -> object: ...

    def named_branch(
        self, run: Callable[[RuntimeContext], object], name: str | None
    ) -> object: ...


class OperationScope(Protocol):
    logger: DurableLogger
    attempt: int


class RuntimeBatchItem(Protocol[T]):
    index: int
    status: object
    result: T | None
    error: object


class RuntimeBatch(Protocol[T]):
    success_count: int
    failure_count: int
    completion_reason: object

    def succeeded(self) -> list[RuntimeBatchItem[T]]: ...

    def failed(self) -> list[RuntimeBatchItem[T]]: ...

    def get_results(self) -> list[T]: ...

    def get_errors(self) -> list[object]: ...

    def throw_if_error(self) -> None: ...


class RuntimeContext(Protocol):
    logger: DurableLogger

    def step(
        self,
        func: Callable[[OperationScope], T],
        name: str | None,
        config: object,
    ) -> T: ...

    def wait(self, duration: object, name: str | None = None) -> None: ...

    def run_in_child_context(
        self, func: Callable[[RuntimeContext], T], name: str | None
    ) -> T: ...

    def wait_for_condition(
        self,
        func: Callable[[T, OperationScope], T],
        config: object,
        name: str | None,
    ) -> T: ...

    def map(
        self,
        items: list[U],
        func: Callable[[RuntimeContext, U, int, list[U]], T],
        name: str | None,
        config: object,
    ) -> RuntimeBatch[T]: ...

    def parallel(
        self,
        branches: list[Callable[[RuntimeContext], T] | object],
        name: str | None,
        config: object,
    ) -> RuntimeBatch[T]: ...

    def set_logger(self, logger: object) -> None: ...
