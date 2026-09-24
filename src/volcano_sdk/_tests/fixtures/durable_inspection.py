"""Test-owned views of protected durable adapter operations."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aws_durable_execution_sdk_python_testing.scheduler import Scheduler
from typing_extensions import override

from volcano_sdk._durable_engine import Engine
from volcano_sdk.durable_authoring import DurableContext

if TYPE_CHECKING:
    from collections.abc import Callable

    from aws_durable_execution_sdk_python.retries import (
        RetryDecision,
        RetryStrategyConfig,
    )

    from volcano_sdk.durable_authoring import RetryOptions


class InspectedEngine(Engine):
    """Inspect option translation without changing the SDK interface."""

    def retry_configuration(self, options: RetryOptions) -> RetryStrategyConfig:
        return self._retry_config(options)

    def custom_retry_strategy(
        self, retry: object
    ) -> Callable[[Exception, int], RetryDecision]:
        return self._custom_retry_strategy(retry)


class InspectedDurableContext(DurableContext):
    """Inspect duration validation without exposing a public test hook."""

    def wait_duration(self, value: object) -> object:
        return self._wait_duration(value)


class ClosingScheduler(Scheduler):
    """Close the upstream scheduler loop after its worker thread stops."""

    @override
    def stop(self) -> None:
        stop: Callable[[], None] = super().stop
        stop()
        if not self._loop.is_closed():
            self._loop.close()
