from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

from aws_durable_execution_sdk_python.config import Duration, JitterStrategy
from aws_durable_execution_sdk_python.serdes import SerDes

_T = TypeVar("_T")

@dataclass
class WaitStrategyConfig(Generic[_T]):
    should_continue_polling: Callable[[_T], bool]
    max_attempts: int = ...
    initial_delay: Duration = ...
    max_delay: Duration = ...
    backoff_rate: int | float = ...
    jitter_strategy: JitterStrategy = ...
    @property
    def initial_delay_seconds(self) -> int: ...
    @property
    def max_delay_seconds(self) -> int: ...

@dataclass(frozen=True)
class WaitForConditionDecision:
    should_continue: bool
    delay: Duration
    @property
    def delay_seconds(self) -> int: ...
    @classmethod
    def continue_waiting(cls, delay: Duration) -> WaitForConditionDecision: ...
    @classmethod
    def stop_polling(cls) -> WaitForConditionDecision: ...

@dataclass(frozen=True)
class WaitForConditionConfig(Generic[_T]):
    wait_strategy: Callable[[_T, int], WaitForConditionDecision]
    initial_state: _T
    serdes: SerDes[object] | None = ...

def create_wait_strategy(
    config: WaitStrategyConfig[_T],
) -> Callable[[_T, int], WaitForConditionDecision]: ...
