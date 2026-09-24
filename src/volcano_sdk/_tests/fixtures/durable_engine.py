"""Check the optional runtime's dynamic import boundary before scheduling work."""

from __future__ import annotations

from aws_durable_execution_sdk_python import config, retries, waits

from volcano_sdk._durable_engine import load_engine
from volcano_sdk._durable_modules import load_root


def assert_runtime_surface() -> None:
    """Fail promptly if the installed runtime lacks an adapter dependency."""
    engine = load_engine()

    wrapper = load_root().durable_execution
    assert engine.durable_execution is wrapper
    assert engine.duration is config.Duration
    assert engine.step_config is config.StepConfig
    assert engine.step_semantics is config.StepSemantics
    assert engine.map_config is config.MapConfig
    assert engine.parallel_config is config.ParallelConfig
    assert engine.completion_config is config.CompletionConfig
    assert engine.parallel_branch is config.ParallelBranch
    assert engine.create_retry_strategy is retries.create_retry_strategy
    assert engine.retry_strategy_config is retries.RetryStrategyConfig
    assert engine.retry_decision is retries.RetryDecision
    assert engine.create_wait_strategy is waits.create_wait_strategy
    assert engine.wait_strategy_config is waits.WaitStrategyConfig
    assert engine.wait_for_condition_config is waits.WaitForConditionConfig
