"""A typed runtime context that records batch calls without scheduling them."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

from typing_extensions import override

if TYPE_CHECKING:
    from collections.abc import Callable

    from volcano_sdk.durable_authoring import (
        DurableLogger,
        _OperationScope,
        _RuntimeBatch,
        _RuntimeBatchItem,
        _RuntimeContext,
    )

T = TypeVar("T")
U = TypeVar("U")
_UNEXPECTED_OPERATION = "unexpected runtime operation in batch test"


class EmptyBatch(Generic[T]):
    """A completed batch with no items."""

    success_count = 0
    failure_count = 0
    completion_reason: object = "all_completed"

    def succeeded(self) -> list[_RuntimeBatchItem[T]]:
        return []

    def failed(self) -> list[_RuntimeBatchItem[T]]:
        return []

    def get_results(self) -> list[T]:
        return []

    def get_errors(self) -> list[object]:
        return []

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

    success_count = 1
    failure_count = 1
    completion_reason: object = "FINISHED"

    def __init__(self, error: object) -> None:
        self._error = error

    @override
    def succeeded(self) -> list[_RuntimeBatchItem[str]]:
        return [RecordedItem(1, "SUCCEEDED", "done", None)]

    @override
    def failed(self) -> list[_RuntimeBatchItem[str]]:
        return [RecordedItem(0, "FAILED", None, self._error)]

    @override
    def get_results(self) -> list[str]:
        return ["done"]

    @override
    def get_errors(self) -> list[object]:
        return [self._error]


class RecordingContext:
    """Implement the runtime context and capture its batch calls."""

    logger: DurableLogger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.branches: list[object] | None = None
        self.name: str | None = None
        self.config: object = None
        self.map_items: list[object] | None = None
        self.map_result: object = None

    def step(
        self,
        func: Callable[[_OperationScope], T],
        name: str | None,
        config: object,
    ) -> T:
        _ = (func, name, config)
        raise AssertionError(_UNEXPECTED_OPERATION)

    def wait(self, duration: object, name: str | None = None) -> None:
        _ = (duration, name)
        raise AssertionError(_UNEXPECTED_OPERATION)

    def run_in_child_context(
        self, func: Callable[[_RuntimeContext], T], name: str | None
    ) -> T:
        _ = (func, name)
        raise AssertionError(_UNEXPECTED_OPERATION)

    def wait_for_condition(
        self,
        func: Callable[[T, _OperationScope], T],
        config: object,
        name: str | None,
    ) -> T:
        _ = func
        self.config = config
        self.name = name
        raise AssertionError(_UNEXPECTED_OPERATION)

    def map(
        self,
        items: list[U],
        func: Callable[[_RuntimeContext, U, int, list[U]], T],
        name: str | None,
        config: object,
    ) -> _RuntimeBatch[T]:
        if not items:
            raise AssertionError(_UNEXPECTED_OPERATION)
        self.name = name
        self.config = config
        self.map_items = list(items)
        self.map_result = func(self, items[0], 7, items)
        return EmptyBatch[T]()

    def parallel(
        self,
        branches: list[Callable[[_RuntimeContext], T] | object],
        name: str | None,
        config: object,
    ) -> _RuntimeBatch[T]:
        self.branches = list(branches)
        self.name = name
        self.config = config
        return EmptyBatch[T]()

    def set_logger(self, logger: object) -> None:
        _ = logger
        raise AssertionError(_UNEXPECTED_OPERATION)
