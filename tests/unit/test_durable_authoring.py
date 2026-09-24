"""Durable authoring tests.

The handler tests run against the AWS durable execution SDK's local runner, so
they exercise real checkpointing and replay rather than a stand-in for it.
"""

from __future__ import annotations

import importlib
import inspect
import json
import logging
from collections.abc import Mapping
from contextlib import contextmanager
from types import ModuleType, SimpleNamespace
from typing import TYPE_CHECKING, TypeGuard

import pytest
from aws_durable_execution_sdk_python.config import (
    Duration,
    MapConfig,
    ParallelConfig,
    StepConfig,
    StepSemantics,
)
from aws_durable_execution_sdk_python.config import (
    ParallelBranch as EngineParallelBranch,
)
from aws_durable_execution_sdk_python.exceptions import WaitForConditionError
from aws_durable_execution_sdk_python.retries import RetryDecision
from aws_durable_execution_sdk_python.waits import (
    WaitForConditionConfig,
    WaitForConditionDecision,
    WaitStrategyConfig,
    create_wait_strategy,
)
from aws_durable_execution_sdk_python_testing import DurableFunctionTestRunner
from fixtures.durable_context import (
    RecordedBatch,
    RecordedFailure,
    RecordingContext,
)
from fixtures.durable_engine import assert_runtime_surface
from fixtures.invalid_callbacks import (
    decorate_non_callable,
    register_non_callable_branch,
    register_non_callable_map,
    register_non_callable_wait,
    run_non_callable_operation,
    use_non_callable_retry,
)
from fixtures.invalid_wait_options import invalid_wait_duration, non_callable_predicate

from volcano_sdk import durable_authoring
from volcano_sdk.durable_authoring import (
    BatchFailure,
    BatchItem,
    BatchOptions,
    BatchResult,
    DurableContext,
    DurableRuntimeMissingError,
    FunctionHandler,
    ParallelBranch,
    RetryOptions,
    StepScope,
    WaitUntilOptions,
    durable,
)
from volcano_sdk.durable_authoring import (
    _to_seconds as to_seconds,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Generator, Iterator

# The local runner's scheduler calls asyncio.iscoroutinefunction, which Python
# 3.14 deprecates, and the suite turns warnings into errors. It comes from the
# runner rather than from the durable runtime a deployed function uses, so it
# says nothing about 3.14 as a durable runtime, and there is no release of the
# runner that avoids it. Scoped to this module so every other test still fails
# on a deprecation, and narrowed to the one call so a real one here still would.
pytestmark = pytest.mark.filterwarnings(
    "ignore:'asyncio.iscoroutinefunction' is deprecated:DeprecationWarning"
)

_EXPECTED_FAILURE = "expected the execution to fail"


def _is_mapping(value: object) -> TypeGuard[Mapping[object, object]]:
    return isinstance(value, Mapping)


def _is_object_list(value: object) -> TypeGuard[list[object]]:
    return isinstance(value, list)


def _is_map_config(value: object) -> TypeGuard[MapConfig[object]]:
    return isinstance(value, MapConfig)


def _is_wait_config(value: object) -> TypeGuard[WaitForConditionConfig[bool]]:
    return isinstance(value, WaitForConditionConfig)


def _ready(state: object) -> bool:
    if not _is_mapping(state):
        msg = "expected a state mapping"
        raise TypeError(msg)
    ready: object = state.get("ready")
    if not isinstance(ready, bool):
        msg = "expected a boolean ready state"
        raise TypeError(msg)
    return ready


def test_an_omitted_mapping_duration_part_is_zero() -> None:
    assert to_seconds({"seconds": 5}, "wait") == 5


@pytest.mark.parametrize("value", [{1: 5}, {"seconds": 5, 1: 3}])
def test_duration_mapping_refuses_non_string_keys(value: object) -> None:
    with pytest.raises(TypeError, match="must be a duration string"):
        _ = to_seconds(value, "wait")


def test_retry_false_produces_an_immediate_no_retry_decision() -> None:
    decision = durable_authoring._Engine()._never_retry()(RuntimeError("failed"), 1)

    assert isinstance(decision, RetryDecision)
    assert decision.should_retry is False
    assert decision.delay.to_seconds() == 0


def test_custom_retry_receives_the_original_error() -> None:
    engine = durable_authoring._Engine()
    failure = RuntimeError("failed")
    seen: list[Exception] = []

    def decide(error: Exception, _attempt: int) -> RetryDecision:
        seen.append(error)
        return RetryDecision(should_retry=False, delay=Duration.from_seconds(0))

    retry = engine._custom_retry_strategy(decide)

    assert retry(failure, 1).should_retry is False
    assert seen == [failure]
    assert seen[0] is failure


def test_wait_options_forward_predicate_timing_and_attempt_budget(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine = durable_authoring._Engine()
    captured: list[WaitStrategyConfig[bool]] = []

    def record(
        config: WaitStrategyConfig[bool],
    ) -> Callable[[bool, int], WaitForConditionDecision]:
        captured.append(config)
        return create_wait_strategy(config)

    monkeypatch.setattr(engine, "create_wait_strategy", record)
    configured = engine.wait_condition_options(
        WaitUntilOptions(
            until=lambda state: state,
            initial_state=False,
            interval="3s",
            max_interval="8s",
            backoff_rate=1.25,
            max_attempts=7,
        )
    )

    assert len(captured) == 1
    config = captured[0]
    incomplete = False
    complete = True
    assert config.should_continue_polling(incomplete) is True
    assert config.should_continue_polling(complete) is False
    assert config.max_attempts == 7
    assert config.initial_delay.to_seconds() == 3
    assert config.max_delay.to_seconds() == 8
    assert config.backoff_rate == pytest.approx(1.25)
    assert _is_wait_config(configured)
    assert configured.initial_state is False


def test_wait_options_name_invalid_timing_fields() -> None:
    engine = durable_authoring._Engine()

    with pytest.raises(ValueError, match=r"^interval must be a duration"):
        _ = engine.wait_condition_options(
            WaitUntilOptions(
                until=lambda state: state, initial_state=False, interval="bad"
            )
        )
    with pytest.raises(ValueError, match=r"^max_interval must be a duration"):
        _ = engine.wait_condition_options(
            WaitUntilOptions(
                until=lambda state: state,
                initial_state=False,
                max_interval="bad",
            )
        )


def test_wait_until_validates_callback_and_forwards_name() -> None:
    runtime = RecordingContext()
    context = DurableContext(runtime, durable_authoring._Engine())
    options = WaitUntilOptions(until=lambda state: state, initial_state=False)

    with pytest.raises(TypeError, match=r"wait_until\(\) requires a function"):
        register_non_callable_wait(context)
    with pytest.raises(AssertionError, match="unexpected runtime operation"):
        _ = context.wait_until(lambda state, _scope: state, options, "poll-ready")
    assert runtime.name == "poll-ready"


def test_wait_accepts_the_maximum_and_names_an_invalid_duration() -> None:
    context = DurableContext(RecordingContext(), durable_authoring._Engine())
    maximum = context._wait_duration(31_622_400)

    assert isinstance(maximum, Duration)
    assert maximum.to_seconds() == 31_622_400
    with pytest.raises(ValueError, match=r"^wait must be a duration"):
        _ = context._wait_duration("bad")


def test_map_options_forward_both_batch_limits() -> None:
    config = durable_authoring._Engine().map_options(
        BatchOptions(concurrency=2, min_succeeded=1)
    )

    assert isinstance(config, MapConfig)
    assert config.max_concurrency == 2
    assert config.completion_config.min_successful == 1


def test_map_forwards_items_callback_index_name_and_batch_limits() -> None:
    runtime = RecordingContext()
    context = DurableContext(runtime, durable_authoring._Engine())
    observed: list[tuple[int, int]] = []

    def run(item: int, _child: DurableContext, index: int) -> int:
        observed.append((item, index))
        return item * 10

    result = context.map(
        [2, 3], run, "batch", BatchOptions(concurrency=2, min_succeeded=1)
    )

    assert result.completed == 0
    assert runtime.map_items == [2, 3]
    assert runtime.map_result == 20
    assert observed == [(2, 7)]
    assert runtime.name == "batch"
    assert _is_map_config(runtime.config)
    assert runtime.config.max_concurrency == 2
    assert runtime.config.completion_config.min_successful == 1


def test_map_requires_a_callable() -> None:
    context = DurableContext(RecordingContext(), durable_authoring._Engine())

    with pytest.raises(TypeError, match=r"map\(\) requires a function to run"):
        register_non_callable_map(context)


def test_batch_result_preserves_settled_items_and_failure_details() -> None:
    failure = BatchFailure("failed", "RemoteError", "trace")
    result = BatchResult(
        RecordedBatch(RecordedFailure("failed", "RemoteError", "trace"))
    )

    assert result.items == (
        BatchItem(0, "failed", None, failure),
        BatchItem(1, "succeeded", "done", None),
    )
    assert result.results == ("done",)
    assert result.errors == (failure,)
    assert result.succeeded == 1
    assert result.failed == 1
    assert result.completed == 2
    assert result.completion_reason == "finished"


def test_batch_result_keeps_a_plain_exception_message() -> None:
    failure = BatchFailure("boom")
    result = BatchResult(RecordedBatch(RuntimeError("boom")))

    assert result.items[0].error == failure
    assert result.errors == (failure,)


def test_parallel_forwards_branches_name_and_batch_limits() -> None:
    runtime = RecordingContext()
    context = DurableContext(runtime, durable_authoring._Engine())
    result = context.parallel(
        [ParallelBranch(lambda _child: "named", name="alpha"), lambda _child: "bare"],
        "fan-out",
        BatchOptions(concurrency=2, min_succeeded=1),
    )

    assert result.completed == 0
    assert runtime.name == "fan-out"
    assert isinstance(runtime.config, ParallelConfig)
    assert runtime.config.max_concurrency == 2
    assert runtime.config.completion_config.min_successful == 1
    assert runtime.branches is not None
    assert len(runtime.branches) == 2
    assert isinstance(runtime.branches[0], EngineParallelBranch)
    assert runtime.branches[0].name == "alpha"
    assert callable(runtime.branches[1])


@contextmanager
def local_runner(handler: FunctionHandler) -> Generator[DurableFunctionTestRunner]:
    """Run a handler on the local runner, then close what it leaves open.

    The runner's own close() stops its scheduler's event loop without closing
    it, so the loop and its self-pipe sockets stay open. The repository turns
    warnings into errors, and an unraisable ResourceWarning cannot be filtered
    from inside the test, so the loop is closed here instead.

    Yields:
        The local runner, closed when the context exits.
    """
    # Fail an unavailable or malformed runtime before entering the scheduler:
    # it otherwise waits for a result that the handler cannot produce.
    assert_runtime_surface()
    assert to_seconds({"seconds": 5}, "wait") == 5
    assert to_seconds("1s", "wait") == 1
    engine = durable_authoring._Engine.load()
    wait_config = engine.wait_condition_options(
        WaitUntilOptions(until=lambda state: state, initial_state=False, max_attempts=2)
    )
    assert _is_wait_config(wait_config)
    not_ready = False
    ready = True
    assert wait_config.wait_strategy(not_ready, 1).should_continue is True
    assert wait_config.wait_strategy(ready, 1).should_continue is False
    # An invalid retry policy can leave the scheduler waiting forever.
    assert engine.step_options(retry=None, at_most_once=False).retry_strategy is None
    assert engine.step_options(retry=True, at_most_once=False).retry_strategy is None
    no_retry_strategy = engine.step_options(
        retry=False, at_most_once=False
    ).retry_strategy
    assert no_retry_strategy is not None
    no_retry = no_retry_strategy(RuntimeError("preflight"), 1)
    assert no_retry.should_retry is False
    assert no_retry.delay.to_seconds() == 0
    runner = DurableFunctionTestRunner(handler)
    try:
        yield runner
    finally:
        close_runner: Callable[[], None] = runner.close
        close_runner()
        loop = runner._scheduler._loop
        if not loop.is_closed():
            loop.close()


def run_handler(handler: FunctionHandler, event: object = None) -> object:
    """Run a durable handler to completion on the local runner.

    Returns:
        The decoded result, or None when the handler returns no result.

    Raises:
        AssertionError: If the handler fails.
    """
    with local_runner(handler) as runner:
        result = runner.run(input=json.dumps({} if event is None else event))
    if result.error is not None:
        raise AssertionError(result.error.message)
    return None if result.result is None else json.loads(result.result)


def failing_handler(handler: FunctionHandler, event: object = None) -> str:
    """Run a handler expected to fail.

    Returns:
        The failure message, or an empty string if it has no message.

    Raises:
        AssertionError: If the handler succeeds.
    """
    with local_runner(handler) as runner:
        result = runner.run(input=json.dumps({} if event is None else event))
    if result.error is None:
        raise AssertionError(_EXPECTED_FAILURE)
    return str(result.error.message or "")


def test_a_step_result_is_recorded_and_returned() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        return ctx.step("charge", lambda scope: {"id": "ch_1", "on": scope.attempt})

    assert run_handler(handler, {"order_id": "o-1"}) == {"id": "ch_1", "on": 1}


def test_an_unnamed_step_still_runs() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        return ctx.step(lambda _scope: "done")

    assert run_handler(handler) == "done"


def test_the_handler_receives_the_execution_input() -> None:
    @durable
    def handler(event: dict[str, str], ctx: DurableContext) -> object:
        return ctx.step("echo", lambda _scope: event["order_id"])

    assert run_handler(handler, {"order_id": "o-42"}) == "o-42"


def test_a_wait_suspends_and_resumes_the_execution() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        first = ctx.step("first", lambda _scope: 1)
        ctx.wait("settle", "1s")
        return first + ctx.step("second", lambda _scope: 1)

    assert run_handler(handler) == 2


def test_a_wait_takes_a_duration_alone() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        ctx.wait("1s")
        return "resumed"

    assert run_handler(handler) == "resumed"


def test_operations_are_recorded_under_their_names() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        _ = ctx.step("charge", lambda _scope: "ch_1")
        ctx.wait("settle", "1s")
        return ctx.child("fulfil", lambda child: child.step("ship", lambda _s: "ok"))

    with local_runner(handler) as runner:
        result = runner.run(input=json.dumps({}))

    assert result.error is None
    assert result.get_step("charge").name == "charge"
    assert result.get_wait("settle").name == "settle"
    # Nested, not top-level: a child context owns the operations run inside it,
    # which is the scope a resumed execution replays them in.
    child = result.get_context("fulfil")
    assert [operation.name for operation in child.child_operations] == ["ship"]


def test_a_child_context_groups_its_own_operations() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        return ctx.child(
            "fulfil",
            lambda child: {
                "picked": child.step("pick", lambda _s: "picked"),
                "shipped": child.step("ship", lambda _s: "shipped"),
            },
        )

    assert run_handler(handler) == {"picked": "picked", "shipped": "shipped"}


def test_map_runs_the_work_over_every_item() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        batch = ctx.map(
            [1, 2, 3],
            lambda item, child, _index: child.step(lambda _s: item * 10),
            "double",
        )
        return {
            "results": sorted(batch.results),
            "succeeded": batch.succeeded,
            "failed": batch.failed,
            "completed": batch.completed,
            "reason": batch.completion_reason,
            "statuses": sorted(item.status for item in batch.items),
        }

    assert run_handler(handler) == {
        "results": [10, 20, 30],
        "succeeded": 3,
        "failed": 0,
        "completed": 3,
        "reason": "all_completed",
        "statuses": ["succeeded", "succeeded", "succeeded"],
    }


def test_map_respects_a_concurrency_limit() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        batch = ctx.map(
            [1, 2, 3, 4],
            lambda item, child, _index: child.step(lambda _s: item),
            "serial",
            BatchOptions(concurrency=1),
        )
        return sorted(batch.results)

    assert run_handler(handler) == [1, 2, 3, 4]


def test_parallel_runs_named_and_bare_branches() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        branches: list[Callable[[DurableContext], str] | ParallelBranch[str]] = [
            ParallelBranch(lambda child: child.step(lambda _s: "a"), name="alpha"),
            lambda child: child.step(lambda _s: "b"),
        ]
        batch = ctx.parallel(branches, "fan-out")
        return {"results": sorted(batch.results), "completed": batch.completed}

    assert run_handler(handler) == {"results": ["a", "b"], "completed": 2}


def test_parallel_options_apply_both_batch_limits() -> None:
    engine = durable_authoring._Engine.load()
    config = engine.parallel_options(BatchOptions(concurrency=2, min_succeeded=1))

    assert config.max_concurrency == 2
    assert config.completion_config.min_successful == 1


def test_a_batch_reports_the_item_that_failed() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        def work(item: int, child: DurableContext, _index: int) -> int:
            def run(_scope: StepScope) -> int:
                if item == 2:
                    message = "item two is bad"
                    raise ValueError(message)
                return item

            return child.step(run, retry=False)

        # The batch ends on its first failure. Finish the successful items first
        # so the exact result below does not depend on concurrent scheduling.
        batch = ctx.map([1, 3, 2], work, "some-fail", BatchOptions(concurrency=1))
        return {
            "succeeded": batch.succeeded,
            "failed": batch.failed,
            "results": sorted(batch.results),
        }

    assert run_handler(handler) == {
        "succeeded": 2,
        "failed": 1,
        "results": [1, 3],
    }


def fail_second_item(item: int, child: DurableContext, _index: int) -> int:
    def run(_scope: StepScope) -> int:
        if item == 2:
            message = "item two is bad"
            raise ValueError(message)
        return item

    return child.step(run, retry=False)


def test_a_failure_is_reported_in_the_facade_s_own_shape() -> None:
    """A failed item reports the platform's wire object, not an exception.

    The facade reduces it to its own three fields, so a handler reads the same
    `message`, `type` and `data` here as in the other SDKs and nothing of the
    runtime's own vocabulary reaches it.
    """

    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        batch = ctx.map([1, 2], fail_second_item, "one-fails")
        # Found rather than indexed. `items` carries the items that settled,
        # and a batch can come back the moment the failure does -- leaving the
        # sibling that was still running out of it -- so the failed item's
        # position is not something the facade promises.
        failure = next(
            (item.error for item in batch.items if item.error is not None), None
        )
        if not isinstance(failure, BatchFailure):
            message = f"expected a BatchFailure, got {type(failure).__name__}"
            raise TypeError(message)
        # The platform's own classification of the failure, which for a step
        # that raised is its step error rather than the raised type.
        classification = (failure.type or "").rsplit(".", 1)[-1]
        return {
            "message": failure.message,
            "type": classification,
            "errors": [error.message for error in batch.errors],
        }

    assert run_handler(handler) == {
        "message": "item two is bad",
        "type": "StepError",
        "errors": ["item two is bad"],
    }


def test_an_early_completion_reports_only_what_finished() -> None:
    """`min_succeeded` ends a batch with items still in flight.

    The platform does not promise to reproduce those when the execution
    resumes, so a handler that saw them could take one path live and another on
    the replay. The facade reports the finished items, how many finished, and
    why the batch ended -- all of which are the same both times.
    """

    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        def work(item: int, child: DurableContext, _index: int) -> int:
            def run(_scope: StepScope) -> int:
                # The later items outlive the completion threshold, so the batch
                # finishes while they are still going.
                if item > 1:
                    child.wait("1s")
                return item

            return child.step(run)

        batch = ctx.map([1, 2, 3], work, "quorum", BatchOptions(min_succeeded=1))
        return {
            "statuses": sorted(item.status for item in batch.items),
            "completed": batch.completed,
            "reason": batch.completion_reason,
        }

    result = run_handler(handler)
    assert _is_mapping(result)
    statuses: object = result.get("statuses")
    assert _is_object_list(statuses)
    assert "started" not in statuses, (
        "an in-flight item is not guaranteed to come back on a replay"
    )
    assert result["completed"] == len(statuses)
    assert result["reason"] == "min_successful_reached"


def test_throw_if_failed_surfaces_a_batch_failure() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        def work(_item: int, child: DurableContext, _index: int) -> int:
            def run(_scope: StepScope) -> int:
                message = "always bad"
                raise ValueError(message)

            return child.step(run, retry=False)

        ctx.map([1], work, "all-fail").throw_if_failed()
        return "unreachable"

    assert "always bad" in failing_handler(handler)


def test_a_step_retries_until_it_succeeds() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        def flaky(scope: StepScope) -> int:
            if scope.attempt < 3:
                message = f"attempt {scope.attempt} failed"
                raise RuntimeError(message)
            return scope.attempt

        return ctx.step(
            "flaky",
            flaky,
            retry=RetryOptions(attempts=5, initial_delay="1s"),
        )

    assert run_handler(handler) == 3


def test_retry_false_fails_on_the_first_error() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        def always(scope: StepScope) -> int:
            message = f"failed on attempt {scope.attempt}"
            raise RuntimeError(message)

        return ctx.step("once", always, retry=False)

    # retry=False is not the same as leaving retry unset: the platform retries
    # by default, so a first-attempt failure proves the strategy was applied.
    assert "failed on attempt 1" in failing_handler(handler)


def test_retry_options_stop_after_their_attempt_budget() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        def always(scope: StepScope) -> int:
            message = f"failed on attempt {scope.attempt}"
            raise RuntimeError(message)

        return ctx.step(
            "bounded",
            always,
            retry=RetryOptions(attempts=2, initial_delay="1s"),
        )

    assert "failed on attempt 2" in failing_handler(handler)


def test_retry_on_limits_which_errors_are_retried() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        def always(scope: StepScope) -> int:
            message = f"unretryable on attempt {scope.attempt}"
            raise RuntimeError(message)

        return ctx.step(
            "filtered",
            always,
            retry=RetryOptions(
                attempts=4,
                initial_delay="1s",
                retry_on=["a message that never matches"],
            ),
        )

    assert "unretryable on attempt 1" in failing_handler(handler)


def test_retry_config_keeps_unset_defaults_and_sets_requested_fields() -> None:
    engine = durable_authoring._Engine.load()
    defaults = engine.retry_strategy_config()
    config = engine._retry_config(
        RetryOptions(
            max_delay="9s",
            backoff_rate=1.25,
            retry_on_types=[ValueError],
        )
    )

    assert config.max_attempts == defaults.max_attempts
    assert config.initial_delay == defaults.initial_delay
    assert config.max_delay.to_seconds() == 9
    assert config.backoff_rate == pytest.approx(1.25)
    assert config.retryable_error_types == [ValueError]


@pytest.mark.parametrize(
    ("options", "field"),
    [
        (RetryOptions(initial_delay="invalid"), "initial_delay"),
        (RetryOptions(max_delay="invalid"), "max_delay"),
    ],
)
def test_retry_config_names_an_invalid_duration(
    options: RetryOptions, field: str
) -> None:
    with pytest.raises(ValueError, match=rf"^{field} must be a duration"):
        _ = durable_authoring._Engine()._retry_config(options)


def test_custom_retry_must_return_a_runtime_decision() -> None:
    engine = durable_authoring._Engine.load()

    def invalid_retry(_error: Exception, _attempt: int) -> str:
        return "invalid"

    retry = engine._custom_retry_strategy(invalid_retry)

    with pytest.raises(TypeError, match="retry must be False"):
        _ = retry(RuntimeError("failed"), 1)


def test_a_custom_retry_callable_decides_per_attempt() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        def decide(_error: Exception, attempt: int) -> RetryDecision:
            return RetryDecision(
                should_retry=attempt < 2,
                delay=Duration.from_seconds(1),
            )

        def flaky(scope: StepScope) -> int:
            if scope.attempt < 2:
                message = "retry me once"
                raise RuntimeError(message)
            return scope.attempt

        return ctx.step("custom", flaky, retry=decide)

    assert run_handler(handler) == 2


def test_at_most_once_runs_the_step_once() -> None:
    config = durable_authoring._Engine().step_options(retry=None, at_most_once=True)
    assert config.step_semantics is StepSemantics.AT_MOST_ONCE_PER_RETRY

    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        return ctx.step("charge", lambda _scope: "charged", at_most_once=True)

    assert run_handler(handler) == "charged"


def test_step_uses_at_least_once_semantics_by_default() -> None:
    runtime = RecordingContext()
    context = DurableContext(runtime, durable_authoring._Engine())

    with pytest.raises(AssertionError, match="unexpected runtime operation"):
        _ = context.step("default", lambda _scope: None)

    assert isinstance(runtime.config, StepConfig)
    assert runtime.config.step_semantics is StepSemantics.AT_LEAST_ONCE_PER_RETRY


def test_wait_until_polls_until_the_condition_holds() -> None:
    polls = {"count": 0}

    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        def check(
            _state: dict[str, int | bool], _scope: StepScope
        ) -> dict[str, int | bool]:
            polls["count"] += 1
            return {"ready": polls["count"] >= 3, "polls": polls["count"]}

        return ctx.wait_until(
            check,
            WaitUntilOptions[dict[str, int | bool]](
                until=_ready,
                initial_state={"ready": False, "polls": 0},
                interval="1s",
                max_attempts=10,
            ),
            "await-ready",
        )

    assert run_handler(handler) == {"ready": True, "polls": 3}


def test_wait_until_fails_when_it_runs_out_of_attempts() -> None:
    options = WaitUntilOptions(
        until=lambda state: state,
        initial_state=False,
        interval="1s",
        max_attempts=2,
    )
    configured = durable_authoring._Engine().wait_condition_options(options)
    assert _is_wait_config(configured)
    not_ready = False
    with pytest.raises(WaitForConditionError, match="exhausted 2 attempts"):
        _ = configured.wait_strategy(not_ready, 2)

    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        return ctx.wait_until(
            lambda _state, _scope: False,
            options,
            "never-ready",
        )

    # Running out fails the execution rather than returning the last state.
    assert "exhausted 2 attempts" in failing_handler(handler)


def test_the_context_and_step_emit_log_messages(
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO)

    @durable
    def handler(_event: object, ctx: DurableContext) -> None:
        ctx.log.info("starting order %s", "o-1", extra={"order_id": "o-1"})
        ctx.step("noop", lambda scope: scope.log.info("running the step"))

    assert run_handler(handler) is None
    assert "starting order o-1" in caplog.messages
    assert "running the step" in caplog.messages


class Recorder:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def info(self, message: str, *_args: object, **_kwargs: object) -> None:
        self.messages.append(message)

    def warn(self, message: str, *_args: object, **_kwargs: object) -> None:
        self.messages.append(message)

    def warning(self, message: str, *_args: object, **_kwargs: object) -> None:
        self.messages.append(message)

    def error(self, message: str, *_args: object, **_kwargs: object) -> None:
        self.messages.append(message)

    def debug(self, message: str, *_args: object, **_kwargs: object) -> None:
        self.messages.append(message)


def test_a_replacement_logger_is_installed() -> None:
    recorder = Recorder()

    @durable(logger=recorder)
    def handler(_event: object, ctx: DurableContext) -> object:
        ctx.log.info("from the handler")
        return "logged"

    assert run_handler(handler) == "logged"
    assert "from the handler" in recorder.messages


def test_durable_is_usable_bare_and_called() -> None:
    @durable
    def bare(_event: object, _ctx: DurableContext) -> object:
        return "bare"

    @durable()
    def called(_event: object, _ctx: DurableContext) -> object:
        return "called"

    assert run_handler(bare) == "bare"
    assert run_handler(called) == "called"


def test_the_wrapper_keeps_the_handler_name() -> None:
    def order_pipeline(_event: object, _ctx: DurableContext) -> object:
        """Handle an order.

        Returns:
            None.
        """
        return None

    wrapped = durable(order_pipeline)
    assert wrapped.__name__ == "order_pipeline"
    assert wrapped.__doc__ == order_pipeline.__doc__
    assert inspect.unwrap(wrapped) is order_pipeline
    assert inspect.signature(wrapped) == inspect.signature(order_pipeline)


def test_durable_refuses_something_that_is_not_callable() -> None:
    with pytest.raises(TypeError, match="requires a callable"):
        decorate_non_callable()


@pytest.mark.parametrize("operation", ["step", "child"])
def test_an_operation_refuses_a_non_callable(operation: str) -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        return run_non_callable_operation(ctx, operation)

    assert f"{operation}() requires a function to run" in failing_handler(handler)


def test_wait_refuses_a_name_that_is_not_a_string() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        ctx.wait(30, "30s")
        return None

    assert "takes a name and a duration" in failing_handler(handler)


# A zero wait passes every shape check and is refused by the platform, which
# means the execution fails partway through -- after earlier steps have run
# and been charged -- rather than at the call that was wrong.
@pytest.mark.parametrize(
    "duration",
    [0, "0s", {"seconds": 0}, {"minutes": 0, "seconds": 0}],
)
def test_wait_refuses_a_wait_of_nothing(duration: object) -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        invalid_wait_duration(ctx, duration)
        return None

    assert "wait must be at least 1 second" in failing_handler(handler)


def test_wait_refuses_a_wait_longer_than_an_execution_may_run() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        ctx.wait("cool-off", {"days": 367})
        return None

    assert "wait must be at most 31622400 seconds" in failing_handler(handler)


def test_wait_until_refuses_a_timeout() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        return ctx.wait_until(
            lambda state, _scope: state,
            WaitUntilOptions(until=bool, initial_state=False, timeout="1h"),
        )

    # A condition is bounded by checks, not by a deadline: the platform holds
    # the wait between them and has no clock to compare against on resume.
    assert "has no `timeout`" in failing_handler(handler)


def test_wait_until_requires_an_initial_state() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        return ctx.wait_until(
            lambda state, _scope: state,
            WaitUntilOptions[object](until=bool),
        )

    assert "requires an `initial_state`" in failing_handler(handler)


def test_wait_until_rejects_a_non_callable_predicate_at_runtime() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        return ctx.wait_until(lambda state, _scope: state, non_callable_predicate())

    assert "requires an `until` predicate" in failing_handler(handler)


@pytest.mark.parametrize(
    "batch", [SimpleNamespace(), SimpleNamespace(completion_reason=None)]
)
def test_missing_batch_completion_reason_remains_absent(batch: object) -> None:
    assert durable_authoring._completion_reason(batch) is None


def test_wait_until_accepts_none_as_an_initial_state() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        def check(_state: str | None, _scope: StepScope) -> str | None:
            return "ready"

        return ctx.wait_until(
            check,
            WaitUntilOptions[str | None](
                until=lambda state: bool(state == "ready"),
                initial_state=None,
                interval="1s",
            ),
            "none-start",
        )

    # None is a legitimate starting state, so it has to be told apart from an
    # omitted one.
    assert run_handler(handler) == "ready"


def test_map_refuses_a_string_of_items() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> object:
        return ctx.map("abc", lambda item, _child, _index: item)

    # A string is a sequence, so mapping over one would otherwise run the work
    # per character instead of refusing.
    assert "requires a sequence of items" in failing_handler(handler)


def test_parallel_refuses_a_branch_that_is_not_callable() -> None:
    context = DurableContext(RecordingContext(), durable_authoring._Engine())

    with pytest.raises(TypeError, match="a parallel branch is a callable"):
        register_non_callable_branch(context)


def test_a_step_refuses_an_unusable_retry() -> None:
    @durable
    def handler(_event: object, ctx: DurableContext) -> None:
        use_non_callable_retry(ctx)

    assert "retry must be False" in failing_handler(handler)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("30s", 30),
        ("5m", 300),
        ("2h", 7200),
        ("1d", 86400),
        ("1m30s", 90),
        ("1h 30m", 5400),
        ("1d2h3m4s", 93784),
        (45, 45),
        (0, 0),
        ({"minutes": 90}, 5400),
        ({"days": 1, "seconds": 1}, 86401),
        ({"hours": 0, "seconds": 5}, 5),
    ],
)
def test_durations_read_as_whole_seconds(value: object, expected: int) -> None:
    assert to_seconds(value, "wait") == expected


@pytest.mark.parametrize(
    "value",
    [
        # No millisecond unit: a durable wait is held by the platform between
        # invocations, so a millisecond value could only be rounded away.
        "400ms",
        "1.5h",
        "",
        "abc",
        "30",
        "s",
        "30s extra",
        "-5s",
        1.5,
        True,
        None,
        [30],
        {"milliseconds": 500},
        {},
        {"seconds": None},
        {"seconds": 1.5},
        {"seconds": True},
    ],
)
def test_unusable_durations_are_refused(value: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        _ = to_seconds(value, "wait")


def test_a_negative_number_of_seconds_is_refused() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        _ = to_seconds(-1, "wait")


def test_an_unknown_duration_field_names_what_it_accepts() -> None:
    with pytest.raises(TypeError, match="days, hours, minutes, seconds"):
        _ = to_seconds({"milliseconds": 500}, "interval")


@pytest.mark.parametrize(
    ("value", "error_type", "message"),
    [
        (
            None,
            TypeError,
            (
                "interval must be a duration string, a whole number of seconds, "
                "or a mapping of days, hours, minutes, seconds"
            ),
        ),
        (
            True,
            TypeError,
            (
                "interval must be a duration string, a whole number of seconds, "
                "or a mapping of days, hours, minutes, seconds"
            ),
        ),
        (
            1.5,
            TypeError,
            "interval must be a whole number of seconds, not a fraction",
        ),
        (
            {"seconds": 1, "years": 2, "milliseconds": 3},
            TypeError,
            (
                "interval duration takes days, hours, minutes, seconds "
                "(got milliseconds, years)"
            ),
        ),
        (
            {},
            TypeError,
            "interval duration needs one of days, hours, minutes, seconds",
        ),
        (
            {"seconds": -1},
            ValueError,
            "interval duration seconds must be a non-negative whole number",
        ),
    ],
)
def test_invalid_duration_reports_the_field_and_reason(
    value: object, error_type: type[Exception], message: str
) -> None:
    with pytest.raises(error_type) as raised:
        _ = to_seconds(value, "interval")
    assert str(raised.value) == message


@pytest.fixture
def without_engine(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Hide the durable engine and clear the cached load either side."""
    durable_authoring._Engine._loaded = None

    def blocked(name: str, package: str | None = None) -> ModuleType:
        if name.startswith("aws_durable_execution_sdk_python"):
            message = f"No module named {name!r}"
            raise ImportError(message)
        return importlib.import_module(name, package)

    monkeypatch.setattr(
        "volcano_sdk.durable_authoring.importlib.import_module", blocked
    )
    yield
    durable_authoring._Engine._loaded = None


@pytest.mark.usefixtures("without_engine")
def test_a_missing_runtime_is_reported_on_invocation() -> None:
    @durable
    def handler(_event: object, _ctx: DurableContext) -> object:
        return None

    # Decorating has to succeed without the engine: the SDK also runs in
    # standard functions and scripts, where merely importing a module that
    # mentions a durable handler must not fail.
    with pytest.raises(DurableRuntimeMissingError, match="durable runtime"):
        _ = handler({}, None)


@pytest.mark.usefixtures("without_engine")
def test_the_missing_runtime_error_says_to_deploy_as_durable() -> None:
    @durable
    def handler(_event: object, _ctx: DurableContext) -> object:
        return None

    with pytest.raises(DurableRuntimeMissingError) as raised:
        _ = handler({}, None)

    assert str(raised.value) == (
        "Durable execution is not available here. Volcano provides the "
        "durable runtime when it builds a function deployed as durable, so "
        "deploy this one that way (`volcano cloud durable deploy`, or "
        "`kind: durable` in volcano-config.yaml). Durable execution is a "
        "cloud capability and does not run locally; to exercise a handler "
        "in your own tests, install `volcano-sdk-python[durable]`."
    )
    assert isinstance(raised.value.__cause__, ImportError)


def test_runtime_missing_error_preserves_an_explicit_cause() -> None:
    cause = ImportError("missing runtime")

    assert DurableRuntimeMissingError(cause).__cause__ is cause
