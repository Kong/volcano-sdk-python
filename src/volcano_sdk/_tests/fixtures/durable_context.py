"""A typed runtime context that records batch calls without scheduling them."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from typing_extensions import override

from volcano_sdk._durable_protocols import RuntimeBatch, RuntimeContext
from volcano_sdk._tests.typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

    from volcano_sdk._durable_protocols import (
        DurableLogger,
        OperationScope,
        RuntimeBatchItem,
    )

T = TypeVar("T")
U = TypeVar("U")
_UNEXPECTED_OPERATION = "unexpected runtime operation in batch test"


class EmptyBatch(RuntimeBatch[T]):
    """A completed batch with no items."""

    success_count: int = 0
    failure_count: int = 0
    completion_reason: object = "all_completed"

    @override
    def succeeded(self) -> list[RuntimeBatchItem[T]]:
        return []

    @override
    def failed(self) -> list[RuntimeBatchItem[T]]:
        return []

    @override
    def get_results(self) -> list[T]:
        return []

    @override
    def get_errors(self) -> list[object]:
        return []

    @override
    def throw_if_error(self) -> None:
        return


@dataclass(frozen=True)
class RecordedFailure:
    """Error fields preserved by the public batch result."""

    message: str
    type: str
    data: str


@dataclass
class RecordedItem:
    """One settled item in a recorded batch."""

    index: int
    status: object
    result: str | None
    error: object


class RecordedBatch(EmptyBatch[str]):
    """A settled success and failure with plain statuses and error details."""

    success_count: int = 1
    failure_count: int = 1
    completion_reason: object = "FINISHED"

    def __init__(self, error: object) -> None:
        self._error: object = error

    @override
    def succeeded(self) -> list[RuntimeBatchItem[str]]:
        return [RecordedItem(1, "SUCCEEDED", "done", None)]

    @override
    def failed(self) -> list[RuntimeBatchItem[str]]:
        return [RecordedItem(0, "FAILED", None, self._error)]

    @override
    def get_results(self) -> list[str]:
        return ["done"]

    @override
    def get_errors(self) -> list[object]:
        return [self._error]


class RecordingContext(RuntimeContext):
    """Implement the runtime context and capture its batch calls."""

    logger: DurableLogger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.branches: list[object] | None = None
        self.name: str | None = None
        self.config: object = None
        self.map_items: list[object] | None = None
        self.map_result: object = None

    @override
    def step(
        self,
        func: Callable[[OperationScope], T],
        name: str | None,
        config: object,
    ) -> T:
        _ = (func, name)
        self.config = config
        raise AssertionError(_UNEXPECTED_OPERATION)

    @override
    def wait(self, duration: object, name: str | None = None) -> None:
        _ = (duration, name)
        raise AssertionError(_UNEXPECTED_OPERATION)

    @override
    def run_in_child_context(
        self, func: Callable[[RuntimeContext], T], name: str | None
    ) -> T:
        _ = (func, name)
        raise AssertionError(_UNEXPECTED_OPERATION)

    @override
    def wait_for_condition(
        self,
        func: Callable[[T, OperationScope], T],
        config: object,
        name: str | None,
    ) -> T:
        _ = func
        self.config = config
        self.name = name
        raise AssertionError(_UNEXPECTED_OPERATION)

    @override
    def map(
        self,
        items: list[U],
        func: Callable[[RuntimeContext, U, int, list[U]], T],
        name: str | None,
        config: object,
    ) -> RuntimeBatch[T]:
        if not items:
            raise AssertionError(_UNEXPECTED_OPERATION)
        self.name = name
        self.config = config
        self.map_items = list(items)
        self.map_result = func(self, items[0], 7, items)
        return EmptyBatch[T]()

    @override
    def parallel(
        self,
        branches: list[Callable[[RuntimeContext], T] | object],
        name: str | None,
        config: object,
    ) -> RuntimeBatch[T]:
        self.branches = list(branches)
        self.name = name
        self.config = config
        return EmptyBatch[T]()

    @override
    def set_logger(self, logger: object) -> None:
        _ = logger
        raise AssertionError(_UNEXPECTED_OPERATION)
