"""The optional engine retains concrete types behind the facade boundary."""

from __future__ import annotations

from typing import TYPE_CHECKING, assert_type

from aws_durable_execution_sdk_python.config import (
    CompletionConfig,
    ParallelConfig,
    StepConfig,
    StepSemantics,
)
from aws_durable_execution_sdk_python.config import Duration as EngineDuration
from aws_durable_execution_sdk_python.retries import RetryDecision, RetryStrategyConfig

if TYPE_CHECKING:
    from volcano_sdk.durable_authoring import DurableContext, _DurableEngine, _Engine


def configuration_types(engine: _Engine, context: DurableContext) -> None:
    interface: _DurableEngine = engine
    interface.seconds(5)
    delay = engine.duration.from_seconds(5)
    assert_type(delay, EngineDuration)
    assert_type(engine.step_config(), StepConfig)
    assert_type(engine.step_semantics, type[StepSemantics])
    assert_type(engine.parallel_config(), ParallelConfig)
    assert_type(engine.completion_config(), CompletionConfig)
    assert_type(engine.retry_strategy_config(), RetryStrategyConfig)
    assert_type(engine.retry_decision(should_retry=False, delay=delay), RetryDecision)
    assert_type(engine.step_options(retry=False, at_most_once=True), StepConfig)
    assert_type(engine._never_retry()(ValueError("failure"), 1), RetryDecision)
    assert_type(engine.seconds(5), EngineDuration)
    assert_type(context._wait_duration("5s"), object)
    assert_type(engine._optional_duration(None, "interval"), EngineDuration | None)


def invalid_configuration(engine: _Engine) -> None:
    engine.duration.from_seconds("five")  # type: ignore[arg-type]
    engine.step_config(step_semantics="once")  # type: ignore[arg-type]
    engine.parallel_config(max_concurrency="one")  # type: ignore[arg-type]
    engine.completion_config(min_successful="one")  # type: ignore[arg-type]
    engine.retry_strategy_config(max_attempts="one")  # type: ignore[arg-type]
    engine.retry_decision(should_retry=False, delay="5s")  # type: ignore[arg-type]
