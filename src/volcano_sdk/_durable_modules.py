"""Typed surfaces for the optional runtime's lazily imported modules."""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from typing_extensions import TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

    from aws_durable_execution_sdk_python.config import (
        CompletionConfig,
        Duration,
        MapConfig,
        ParallelBranch,
        ParallelConfig,
        StepConfig,
        StepSemantics,
    )
    from aws_durable_execution_sdk_python.retries import (
        RetryDecision,
        RetryStrategyConfig,
    )
    from aws_durable_execution_sdk_python.waits import (
        WaitForConditionConfig,
        WaitForConditionDecision,
        WaitStrategyConfig,
    )

    from ._durable_protocols import RuntimeContext

T = TypeVar("T")


class DurableExecution(Protocol):
    """Wrap a typed handler in the runtime's invocation envelope."""

    def __call__(
        self, func: Callable[[T, RuntimeContext], object], /
    ) -> Callable[[object, object], object]: ...


class WaitStrategyFactory(Protocol):
    """Create polling defaults while preserving the state type."""

    def __call__(
        self, *, should_continue_polling: Callable[[T], bool]
    ) -> WaitStrategyConfig[T]: ...


class WaitConfigFactory(Protocol):
    """Pair a polling strategy with its initial state."""

    def __call__(
        self,
        *,
        wait_strategy: Callable[[T, int], WaitForConditionDecision],
        initial_state: T,
    ) -> WaitForConditionConfig[T]: ...


class CreateWaitStrategy(Protocol):
    """Preserve state typing when compiling polling configuration."""

    def __call__(
        self, config: WaitStrategyConfig[T], /
    ) -> Callable[[T, int], WaitForConditionDecision]: ...


@runtime_checkable
class RootModule(Protocol):
    """The optional runtime's handler wrapper."""

    durable_execution: DurableExecution


@runtime_checkable
class ConfigModule(Protocol):
    """Configuration constructors used by the authoring adapter."""

    Duration: type[Duration]
    StepConfig: type[StepConfig]
    StepSemantics: type[StepSemantics]
    MapConfig: type[MapConfig[object]]
    ParallelConfig: type[ParallelConfig]
    CompletionConfig: type[CompletionConfig]
    ParallelBranch: type[ParallelBranch[object]]


@runtime_checkable
class RetriesModule(Protocol):
    """Retry configuration and strategy constructors."""

    create_retry_strategy: Callable[
        [RetryStrategyConfig], Callable[[Exception, int], RetryDecision]
    ]
    RetryStrategyConfig: type[RetryStrategyConfig]
    RetryDecision: type[RetryDecision]


@runtime_checkable
class WaitsModule(Protocol):
    """Generic polling constructors exposed by the optional runtime."""

    create_wait_strategy: CreateWaitStrategy
    WaitStrategyConfig: WaitStrategyFactory
    WaitForConditionConfig: WaitConfigFactory


def load_config() -> ConfigModule:
    """Validate the optional runtime's config module.

    Returns:
        The validated module interface.

    Raises:
        TypeError: The installed runtime lacks a required public export.

    """
    module = importlib.import_module("aws_durable_execution_sdk_python.config")
    if not isinstance(module, ConfigModule):
        message = (
            "aws_durable_execution_sdk_python.config does not provide ConfigModule"
        )
        raise TypeError(message)
    return module


def load_retries() -> RetriesModule:
    """Validate the optional runtime's retries module.

    Returns:
        The validated module interface.

    Raises:
        TypeError: The installed runtime lacks a required public export.

    """
    module = importlib.import_module("aws_durable_execution_sdk_python.retries")
    if not isinstance(module, RetriesModule):
        message = (
            "aws_durable_execution_sdk_python.retries does not provide RetriesModule"
        )
        raise TypeError(message)
    return module


def load_waits() -> WaitsModule:
    """Validate the optional runtime's waits module.

    Returns:
        The validated module interface.

    Raises:
        TypeError: The installed runtime lacks a required public export.

    """
    module = importlib.import_module("aws_durable_execution_sdk_python.waits")
    if not isinstance(module, WaitsModule):
        message = "aws_durable_execution_sdk_python.waits does not provide WaitsModule"
        raise TypeError(message)
    return module


def load_root() -> RootModule:
    """Validate the optional runtime's root module.

    Returns:
        The validated module interface.

    Raises:
        TypeError: The installed runtime lacks a required public export.

    """
    module = importlib.import_module("aws_durable_execution_sdk_python")
    if not isinstance(module, RootModule):
        message = "aws_durable_execution_sdk_python does not provide RootModule"
        raise TypeError(message)
    return module
