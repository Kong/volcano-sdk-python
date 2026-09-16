"""Durable authoring tests.

The handler tests run against the AWS durable execution SDK's local runner, so
they exercise real checkpointing and replay rather than a stand-in for it.
"""

from __future__ import annotations

import importlib
import json
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

import pytest
from aws_durable_execution_sdk_python.config import Duration
from aws_durable_execution_sdk_python.retries import RetryDecision
from aws_durable_execution_sdk_python_testing import DurableFunctionTestRunner

from volcano_sdk import durable_authoring
from volcano_sdk.durable_authoring import (
    BatchFailure,
    BatchOptions,
    DurableContext,
    DurableRuntimeMissingError,
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


@contextmanager
def local_runner(handler: Any) -> Generator[DurableFunctionTestRunner]:
    """Run a handler on the local runner, then close what it leaves open.

    The runner's own close() stops its scheduler's event loop without closing
    it, so the loop and its self-pipe sockets stay open. The repository turns
    warnings into errors, and an unraisable ResourceWarning cannot be filtered
    from inside the test, so the loop is closed here instead.
    """
    runner = DurableFunctionTestRunner(handler)
    try:
        yield runner
    finally:
        runner.close()  # type: ignore[no-untyped-call]
        loop = runner._scheduler._loop
        if not loop.is_closed():
            loop.close()


def run_handler(handler: Any, event: object = None) -> Any:
    """Run a durable handler to completion on the local runner."""
    with local_runner(handler) as runner:
        result = runner.run(input=json.dumps({} if event is None else event))
    if result.error is not None:
        raise AssertionError(result.error.message)
    return None if result.result is None else json.loads(result.result)


def failing_handler(handler: Any, event: object = None) -> str:
    """Run a handler expected to fail, and return the failure message."""
    with local_runner(handler) as runner:
        result = runner.run(input=json.dumps({} if event is None else event))
    if result.error is None:
        raise AssertionError(_EXPECTED_FAILURE)
    return str(result.error.message or "")


def test_a_step_result_is_recorded_and_returned() -> None:
    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
        return ctx.step("charge", lambda scope: {"id": "ch_1", "on": scope.attempt})

    assert run_handler(handler, {"order_id": "o-1"}) == {"id": "ch_1", "on": 1}


def test_an_unnamed_step_still_runs() -> None:
    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
        return ctx.step(lambda _scope: "done")

    assert run_handler(handler) == "done"


def test_the_handler_receives_the_execution_input() -> None:
    @durable
    def handler(event: Any, ctx: DurableContext) -> Any:
        return ctx.step("echo", lambda _scope: event["order_id"])

    assert run_handler(handler, {"order_id": "o-42"}) == "o-42"


def test_a_wait_suspends_and_resumes_the_execution() -> None:
    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
        first = ctx.step("first", lambda _scope: 1)
        ctx.wait("settle", "1s")
        return first + ctx.step("second", lambda _scope: 1)

    assert run_handler(handler) == 2


def test_a_wait_takes_a_duration_alone() -> None:
    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
        ctx.wait("1s")
        return "resumed"

    assert run_handler(handler) == "resumed"


def test_operations_are_recorded_under_their_names() -> None:
    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
        ctx.step("charge", lambda _scope: "ch_1")
        ctx.wait("settle", "1s")
        return ctx.child("fulfil", lambda child: child.step("ship", lambda _s: "ok"))

    with local_runner(handler) as runner:
        result = runner.run(input=json.dumps({}))

    assert result.error is None
    assert result.get_step("charge") is not None
    assert result.get_wait("settle") is not None
    # Nested, not top-level: a child context owns the operations run inside it,
    # which is the scope a resumed execution replays them in.
    child = result.get_context("fulfil")
    assert [operation.name for operation in child.child_operations] == ["ship"]


def test_a_child_context_groups_its_own_operations() -> None:
    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
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
    def handler(_event: Any, ctx: DurableContext) -> Any:
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
    def handler(_event: Any, ctx: DurableContext) -> Any:
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
    def handler(_event: Any, ctx: DurableContext) -> Any:
        branches: list[Callable[[DurableContext], str] | ParallelBranch[str]] = [
            ParallelBranch(lambda child: child.step(lambda _s: "a"), name="alpha"),
            lambda child: child.step(lambda _s: "b"),
        ]
        batch = ctx.parallel(branches, "fan-out")
        return {"results": sorted(batch.results), "completed": batch.completed}

    assert run_handler(handler) == {"results": ["a", "b"], "completed": 2}


def test_a_batch_reports_the_item_that_failed() -> None:
    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
        def work(item: int, child: DurableContext, _index: int) -> int:
            def run(_scope: StepScope) -> int:
                if item == 2:
                    message = "item two is bad"
                    raise ValueError(message)
                return item

            return child.step(run, retry=False)

        batch = ctx.map([1, 2, 3], work, "some-fail")
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


def test_a_failure_is_reported_in_the_facade_s_own_shape() -> None:
    """A failed item reports the platform's wire object, not an exception.

    The facade reduces it to its own three fields, so a handler reads the same
    `message`, `type` and `data` here as in the other SDKs and nothing of the
    runtime's own vocabulary reaches it.
    """

    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
        def work(item: int, child: DurableContext, _index: int) -> int:
            def run(_scope: StepScope) -> int:
                if item == 2:
                    message = "item two is bad"
                    raise ValueError(message)
                return item

            return child.step(run, retry=False)

        batch = ctx.map([1, 2], work, "one-fails")
        failure = batch.items[1].error
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
    def handler(_event: Any, ctx: DurableContext) -> Any:
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

    assert "started" not in result["statuses"], (
        "an in-flight item is not guaranteed to come back on a replay"
    )
    assert result["completed"] == len(result["statuses"])
    assert result["reason"] == "min_successful_reached"


def test_throw_if_failed_surfaces_a_batch_failure() -> None:
    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
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
    def handler(_event: Any, ctx: DurableContext) -> Any:
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
    def handler(_event: Any, ctx: DurableContext) -> Any:
        def always(scope: StepScope) -> int:
            message = f"failed on attempt {scope.attempt}"
            raise RuntimeError(message)

        return ctx.step("once", always, retry=False)

    # retry=False is not the same as leaving retry unset: the platform retries
    # by default, so a first-attempt failure proves the strategy was applied.
    assert "failed on attempt 1" in failing_handler(handler)


def test_retry_options_stop_after_their_attempt_budget() -> None:
    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
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
    def handler(_event: Any, ctx: DurableContext) -> Any:
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


def test_a_custom_retry_callable_decides_per_attempt() -> None:
    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
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
    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
        return ctx.step("charge", lambda _scope: "charged", at_most_once=True)

    assert run_handler(handler) == "charged"


def test_wait_until_polls_until_the_condition_holds() -> None:
    polls = {"count": 0}

    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
        def check(_state: Any, _scope: StepScope) -> Any:
            polls["count"] += 1
            return {"ready": polls["count"] >= 3, "polls": polls["count"]}

        return ctx.wait_until(
            check,
            WaitUntilOptions(
                until=lambda state: bool(state["ready"]),
                initial_state={"ready": False, "polls": 0},
                interval="1s",
                max_attempts=10,
            ),
            "await-ready",
        )

    assert run_handler(handler) == {"ready": True, "polls": 3}


def test_wait_until_fails_when_it_runs_out_of_attempts() -> None:
    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
        return ctx.wait_until(
            lambda _state, _scope: {"ready": False},
            WaitUntilOptions(
                until=lambda state: bool(state["ready"]),
                initial_state={"ready": False},
                interval="1s",
                max_attempts=2,
            ),
            "never-ready",
        )

    # Running out fails the execution rather than returning the last state.
    assert "exhausted 2 attempts" in failing_handler(handler)


def test_the_logger_is_reachable_on_the_context() -> None:
    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
        ctx.log.info("starting order o-1")
        return ctx.step("noop", lambda scope: scope.log is not None)

    assert run_handler(handler) is True


def test_a_replacement_logger_is_installed() -> None:
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

    recorder = Recorder()

    @durable(logger=recorder)
    def handler(_event: Any, ctx: DurableContext) -> Any:
        ctx.log.info("from the handler")
        return "logged"

    assert run_handler(handler) == "logged"
    assert "from the handler" in recorder.messages


def test_durable_is_usable_bare_and_called() -> None:
    @durable
    def bare(_event: Any, _ctx: DurableContext) -> Any:
        return "bare"

    @durable()
    def called(_event: Any, _ctx: DurableContext) -> Any:
        return "called"

    assert run_handler(bare) == "bare"
    assert run_handler(called) == "called"


def test_the_wrapper_keeps_the_handler_name() -> None:
    @durable
    def order_pipeline(_event: Any, _ctx: DurableContext) -> Any:
        """Handle an order."""
        return None

    assert order_pipeline.__name__ == "order_pipeline"
    assert order_pipeline.__doc__ == "Handle an order."


def test_durable_refuses_something_that_is_not_callable() -> None:
    with pytest.raises(TypeError, match="requires a callable"):
        durable("not a handler")  # type: ignore[call-overload]


@pytest.mark.parametrize("operation", ["step", "child"])
def test_an_operation_refuses_a_non_callable(operation: str) -> None:
    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
        return getattr(ctx, operation)("named", "not a function")

    assert f"{operation}() requires a function to run" in failing_handler(handler)


def test_wait_refuses_a_name_that_is_not_a_string() -> None:
    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
        return ctx.wait(30, "30s")

    assert "takes a name and a duration" in failing_handler(handler)


def test_wait_until_refuses_a_timeout() -> None:
    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
        return ctx.wait_until(
            lambda state, _scope: state,
            WaitUntilOptions(until=bool, initial_state=False, timeout="1h"),
        )

    # A condition is bounded by checks, not by a deadline: the platform holds
    # the wait between them and has no clock to compare against on resume.
    assert "has no `timeout`" in failing_handler(handler)


def test_wait_until_requires_an_initial_state() -> None:
    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
        return ctx.wait_until(
            lambda state, _scope: state,
            WaitUntilOptions(until=bool),
        )

    assert "requires an `initial_state`" in failing_handler(handler)


def test_wait_until_accepts_none_as_an_initial_state() -> None:
    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
        return ctx.wait_until(
            lambda _state, _scope: "ready",
            WaitUntilOptions(
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
    def handler(_event: Any, ctx: DurableContext) -> Any:
        return ctx.map("abc", lambda item, _child, _index: item)

    # A string is a sequence, so mapping over one would otherwise run the work
    # per character instead of refusing.
    assert "requires a sequence of items" in failing_handler(handler)


def test_parallel_refuses_a_branch_that_is_not_callable() -> None:
    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
        return ctx.parallel(["not a branch"])  # type: ignore[list-item]

    assert "a parallel branch is a callable" in failing_handler(handler)


def test_a_step_refuses_an_unusable_retry() -> None:
    @durable
    def handler(_event: Any, ctx: DurableContext) -> Any:
        return ctx.step("charge", lambda _scope: None, retry="aggressively")  # type: ignore[arg-type]

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
        to_seconds(value, "wait")


def test_a_negative_number_of_seconds_is_refused() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        to_seconds(-1, "wait")


def test_an_unknown_duration_field_names_what_it_accepts() -> None:
    with pytest.raises(TypeError, match="days, hours, minutes, seconds"):
        to_seconds({"milliseconds": 500}, "interval")


@pytest.fixture
def without_engine(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Hide the durable engine and clear the cached load either side."""
    durable_authoring._Engine._loaded = None

    def blocked(name: str, *args: object, **kwargs: object) -> Any:
        if name.startswith("aws_durable_execution_sdk_python"):
            message = f"No module named {name!r}"
            raise ImportError(message)
        return importlib.import_module(name, *args, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(
        "volcano_sdk.durable_authoring.importlib.import_module", blocked
    )
    yield
    durable_authoring._Engine._loaded = None


@pytest.mark.usefixtures("without_engine")
def test_a_missing_runtime_is_reported_on_invocation() -> None:
    @durable
    def handler(_event: Any, _ctx: DurableContext) -> Any:
        return None

    # Decorating has to succeed without the engine: the SDK also runs in
    # standard functions and scripts, where merely importing a module that
    # mentions a durable handler must not fail.
    with pytest.raises(DurableRuntimeMissingError, match="durable runtime"):
        handler({}, None)


@pytest.mark.usefixtures("without_engine")
def test_the_missing_runtime_error_says_to_deploy_as_durable() -> None:
    @durable
    def handler(_event: Any, _ctx: DurableContext) -> Any:
        return None

    with pytest.raises(DurableRuntimeMissingError) as raised:
        handler({}, None)

    message = str(raised.value)
    # Volcano installs the runtime when it builds a durable function, so the
    # fix is a deploy rather than an install. A function's requirements.txt
    # never names the runtime, and the error must not send a reader to add it.
    assert "deploy this one that way" in message
    assert "kind: durable" in message
    assert "does not run locally" in message
    assert "requirements.txt" not in message
    assert "aws-durable-execution-sdk-python" not in message

    # The extra is still the answer for one case, and only that one.
    assert "in your own tests, install `volcano-sdk[durable]`" in message
