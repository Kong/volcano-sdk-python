"""Durable function authoring API.

A durable function checkpoints its progress as it runs, so one execution can
span many invocations and run for hours. This module is what the function
itself is written against; starting an execution and reading its result are
done through `client.durable`, the CLI, or the dashboard.

    from volcano_sdk.durable_authoring import durable

    @durable
    def handler(event, ctx):
        charge = ctx.step("charge", lambda scope: charge_card(event["order_id"]))
        ctx.wait("settle", "30s")
        return {"charged": charge["id"]}

Every context operation is checkpointed: what finished is recorded, and a
resumed execution replays those recorded outcomes instead of doing the work
again. That is also the one rule the handler has to respect -- the code between
the operations runs again on every resume, so it has to reach the same
operations in the same order.

Authoring a durable function needs a durable-capable runtime: python3.13 or
python3.14.
"""

from __future__ import annotations

import functools
import importlib
from collections.abc import Callable
from dataclasses import dataclass, replace
from typing import (
    TYPE_CHECKING,
    Generic,
    Never,
    ParamSpec,
    Protocol,
    TypeAlias,
    TypeGuard,
    overload,
)

from typing_extensions import TypeVar

from ._callbacks import require_callable

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from aws_durable_execution_sdk_python.config import (
        CompletionConfig,
        ParallelConfig,
        StepConfig,
        StepSemantics,
    )
    from aws_durable_execution_sdk_python.config import Duration as EngineDuration
    from aws_durable_execution_sdk_python.retries import (
        RetryDecision,
        RetryStrategyConfig,
    )

T = TypeVar("T", default=object)
U = TypeVar("U", default=object)
# An unsubscripted public handler can accept a specific input type without
# promising that callers may pass an arbitrary object to it.
_Input = TypeVar("_Input", default=Never)
_Output = TypeVar("_Output", default=object)
_P = ParamSpec("_P")
# A duration: "30s", "5m", "2h", "1d", a compound string like "1m30s", a whole
# number of seconds, or the mapping form.
Duration: TypeAlias = "str | int | dict[str, int]"
# What a durable function is written as, and what the platform invokes it as.
# The second argument differs: the handler is given a durable context, and the
# wrapper is given the invocation's own context.
DurableHandler: TypeAlias = Callable[[_Input, "DurableContext"], _Output]
# Invocation envelopes are distinct from the user handler's input and result.
FunctionHandler: TypeAlias = "Callable[[object, object], object]"

# A deployed durable function gets the runtime from the build and needs no
# extra. This is for running a handler in your own tests, which is the one place
# a reader still installs it themselves.
_ENGINE_EXTRA = "volcano-sdk-python[durable]"
_ENGINE_MODULE = "aws_durable_execution_sdk_python"
_DURATION_FIELDS = ("days", "hours", "minutes", "seconds")
# No milliseconds: a durable duration is held by the platform between
# invocations and its wire form carries whole seconds, so a millisecond value
# could only be rounded -- and a rounded "400ms" is no wait at all.
_DURATION_UNITS = {"s": 1, "m": 60, "h": 3600, "d": 86400}
_FIELD_UNITS = {"days": 86400, "hours": 3600, "minutes": 60, "seconds": 1}
# The bounds the platform puts on one wait: at least a second, and no longer
# than an execution may live. Checked here because a zero wait reaches the
# platform as a wait of nothing and fails the execution after earlier steps
# have run and been charged.
_MIN_WAIT_SECONDS = 1
_MAX_WAIT_SECONDS = 31622400
_REQUIRES_HANDLER = "durable(handler) requires a callable"
_REQUIRES_UNTIL = "wait_until() requires an `until` predicate"
_REQUIRES_INITIAL_STATE = (
    "wait_until() requires an `initial_state`, which is what `until` is given "
    "until the state changes"
)
# A condition is bounded by how many times it is checked, not by a deadline:
# the platform holds the wait between checks and has no clock to compare
# against when it resumes. Refused rather than ignored, because a wait meant to
# give up after an hour would otherwise poll to the execution's own ceiling.
_NO_TIMEOUT = (
    "wait_until() has no `timeout`: bound the wait with `max_attempts`, "
    "`interval` and `max_interval`"
)
_INVALID_RETRY = "retry must be False, a callable, or a RetryOptions"
_INVALID_BRANCH = "a parallel branch is a callable, or a ParallelBranch"
_INVALID_ITEMS = "map() requires a sequence of items"
_INVALID_WAIT_ARGS = "wait() takes a name and a duration, or a duration alone"


# Distinguishes an omitted initial_state from an explicit None, which is a
# legitimate state for a condition to start from.
class _Unset:
    __slots__ = ()


_UNSET = _Unset()


class DurableRuntimeMissingError(Exception):
    """Raised when the durable runtime is not available.

    Volcano installs the runtime when it builds a function deployed as
    durable, so this means the handler is running somewhere durable execution
    does not exist: a function that was not deployed as durable, or a local
    script.
    """

    def __init__(self, cause: BaseException | None = None) -> None:
        """Explain that durable execution is not available here."""
        super().__init__(
            "Durable execution is not available here. Volcano provides the "
            "durable runtime when it builds a function deployed as durable, so "
            "deploy this one that way (`volcano cloud durable deploy`, or "
            "`kind: durable` in volcano-config.yaml). Durable execution is a "
            f"cloud capability and does not run locally; to exercise a handler "
            f"in your own tests, install `{_ENGINE_EXTRA}`."
        )
        self.__cause__ = cause


class _DurableEngine(Protocol):
    """The operations the Volcano facade needs from the optional runtime."""

    def seconds(self, value: int) -> object: ...

    def step_options(self, *, retry: Retry, at_most_once: bool) -> object: ...

    def wait_condition_options(self, options: WaitUntilOptions[T]) -> object: ...

    def map_options(self, options: BatchOptions | None) -> object: ...

    def parallel_options(self, options: BatchOptions | None) -> object: ...

    def named_branch(
        self, run: Callable[[_RuntimeContext], object], name: str | None
    ) -> object: ...


class _OperationScope(Protocol):
    logger: DurableLogger
    attempt: int


class _RuntimeBatchItem(Protocol[T]):
    index: int
    status: object
    result: T | None
    error: object


class _RuntimeBatch(Protocol[T]):
    success_count: int
    failure_count: int
    completion_reason: object

    def succeeded(self) -> list[_RuntimeBatchItem[T]]: ...

    def failed(self) -> list[_RuntimeBatchItem[T]]: ...

    def get_results(self) -> list[T]: ...

    def get_errors(self) -> list[object]: ...

    def throw_if_error(self) -> None: ...


class _RuntimeContext(Protocol):
    logger: DurableLogger

    def step(
        self,
        func: Callable[[_OperationScope], T],
        name: str | None,
        config: object,
    ) -> T: ...

    def wait(self, duration: object, name: str | None = None) -> None: ...

    def run_in_child_context(
        self, func: Callable[[_RuntimeContext], T], name: str | None
    ) -> T: ...

    def wait_for_condition(
        self,
        func: Callable[[T, _OperationScope], T],
        config: object,
        name: str | None,
    ) -> T: ...

    def map(
        self,
        items: list[U],
        func: Callable[[_RuntimeContext, U, int, list[U]], T],
        name: str | None,
        config: object,
    ) -> _RuntimeBatch[T]: ...

    def parallel(
        self,
        branches: list[Callable[[_RuntimeContext], T] | object],
        name: str | None,
        config: object,
    ) -> _RuntimeBatch[T]: ...

    def set_logger(self, logger: object) -> None: ...


class _Engine:
    """The durable protocol, from the AWS durable execution SDK.

    Resolved on first use rather than imported at module scope, because the
    Volcano SDK also runs in standard functions and scripts where the runtime
    is absent, and a missing engine is worth a real error message instead of
    an ImportError from an unfamiliar package.
    """

    _loaded: _Engine | None = None

    def __init__(self) -> None:
        """Resolve the engine's public surface.

        Raises:
            DurableRuntimeMissingError: The runtime or a required module cannot
                be imported.

        """
        try:
            config = importlib.import_module(f"{_ENGINE_MODULE}.config")
            retries = importlib.import_module(f"{_ENGINE_MODULE}.retries")
            waits = importlib.import_module(f"{_ENGINE_MODULE}.waits")
            root = importlib.import_module(_ENGINE_MODULE)
        except ImportError as error:
            raise DurableRuntimeMissingError from error
        self.durable_execution = root.durable_execution
        self.duration: type[EngineDuration] = config.Duration
        self.step_config: type[StepConfig] = config.StepConfig
        self.step_semantics: type[StepSemantics] = config.StepSemantics
        self.map_config = config.MapConfig
        self.parallel_config: type[ParallelConfig] = config.ParallelConfig
        self.completion_config: type[CompletionConfig] = config.CompletionConfig
        self.parallel_branch = config.ParallelBranch
        self.create_retry_strategy: Callable[
            [RetryStrategyConfig], Callable[[Exception, int], RetryDecision]
        ] = retries.create_retry_strategy
        self.retry_strategy_config: type[RetryStrategyConfig] = (
            retries.RetryStrategyConfig
        )
        self.retry_decision: type[RetryDecision] = retries.RetryDecision
        self.create_wait_strategy = waits.create_wait_strategy
        self.wait_strategy_config = waits.WaitStrategyConfig
        self.wait_for_condition_config = waits.WaitForConditionConfig

    @classmethod
    def load(cls) -> _Engine:
        """Resolve the engine once per process.

        Returns:
            The cached engine adapter.

        """
        if cls._loaded is None:
            cls._loaded = cls()
        return cls._loaded

    def seconds(self, value: int) -> EngineDuration:
        """Build the runtime's duration from whole seconds.

        Returns:
            The runtime duration.

        """
        return self.duration.from_seconds(value)

    def step_options(self, *, retry: Retry, at_most_once: bool) -> StepConfig:
        """Build the runtime's step options.

        Returns:
            The runtime step configuration.

        """
        config = self.step_config()
        if at_most_once:
            config = replace(
                config, step_semantics=self.step_semantics.AT_MOST_ONCE_PER_RETRY
            )
        strategy = self._retry_strategy(retry)
        if strategy is not None:
            config = replace(config, retry_strategy=strategy)
        return config

    def _retry_strategy(
        self, retry: object
    ) -> Callable[[Exception, int], RetryDecision] | None:
        if retry is None or retry is True:
            return None
        # False disables the runtime's default retry policy for this step.
        if retry is False:
            return self._never_retry()
        return self._custom_retry_strategy(retry)

    def _custom_retry_strategy(
        self, retry: object
    ) -> Callable[[Exception, int], RetryDecision]:
        if isinstance(retry, RetryOptions):
            return self.create_retry_strategy(self._retry_config(retry))
        if callable(retry):

            def decide(error: Exception, attempt: int) -> RetryDecision:
                result = retry(error, attempt)
                if not isinstance(result, self.retry_decision):
                    raise TypeError(_INVALID_RETRY)
                return result

            return decide
        raise TypeError(_INVALID_RETRY)

    def _never_retry(self) -> Callable[[Exception, int], RetryDecision]:
        no_delay = self.seconds(0)

        def never_retry(_error: Exception, _attempt: int) -> RetryDecision:
            return self.retry_decision(should_retry=False, delay=no_delay)

        return never_retry

    def _retry_config(self, retry: RetryOptions) -> RetryStrategyConfig:
        config = self.retry_strategy_config()
        self._set_retry_timing(config, retry)
        self._set_retry_filters(config, retry)
        return config

    def _set_retry_timing(
        self, config: RetryStrategyConfig, retry: RetryOptions
    ) -> None:
        if retry.attempts is not None:
            config.max_attempts = retry.attempts
        if retry.initial_delay is not None:
            config.initial_delay = self.seconds(
                _to_seconds(retry.initial_delay, "initial_delay")
            )
        if retry.max_delay is not None:
            config.max_delay = self.seconds(_to_seconds(retry.max_delay, "max_delay"))
        if retry.backoff_rate is not None:
            config.backoff_rate = retry.backoff_rate

    @staticmethod
    def _set_retry_filters(config: RetryStrategyConfig, retry: RetryOptions) -> None:
        if retry.retry_on is not None:
            config.retryable_errors = list(retry.retry_on)
        if retry.retry_on_types is not None:
            config.retryable_error_types = list(retry.retry_on_types)

    def _optional_duration(
        self, value: Duration | None, field_name: str
    ) -> EngineDuration | None:
        return None if value is None else self.seconds(_to_seconds(value, field_name))

    def wait_condition_options(self, options: WaitUntilOptions[T]) -> object:
        """Build the runtime's polling options.

        Returns:
            The runtime wait condition configuration.

        """
        until = options.until

        def keep_polling(state: T) -> bool:
            return not until(state)

        strategy = self.wait_strategy_config(
            **_engine_kwargs(
                should_continue_polling=keep_polling,
                max_attempts=options.max_attempts,
                initial_delay=self._optional_duration(options.interval, "interval"),
                max_delay=self._optional_duration(options.max_interval, "max_interval"),
                backoff_rate=options.backoff_rate,
            )
        )
        return self.wait_for_condition_config(
            wait_strategy=self.create_wait_strategy(strategy),
            initial_state=options.initial_state,
        )

    def map_options(self, options: BatchOptions | None) -> object:
        """Build the runtime's map options.

        Returns:
            The runtime map configuration.

        """
        resolved = BatchOptions() if options is None else options
        config = self.map_config()
        if resolved.concurrency is not None:
            config = replace(config, max_concurrency=resolved.concurrency)
        if resolved.min_succeeded is not None:
            config = replace(
                config,
                completion_config=self.completion_config(
                    min_successful=resolved.min_succeeded
                ),
            )
        return config

    def parallel_options(self, options: BatchOptions | None) -> ParallelConfig:
        """Build the runtime's parallel options.

        Returns:
            The runtime parallel configuration.

        """
        resolved = BatchOptions() if options is None else options
        config = self.parallel_config()
        if resolved.concurrency is not None:
            config = replace(config, max_concurrency=resolved.concurrency)
        if resolved.min_succeeded is not None:
            config = replace(
                config,
                completion_config=self.completion_config(
                    min_successful=resolved.min_succeeded
                ),
            )
        return config

    def named_branch(
        self, run: Callable[[_RuntimeContext], object], name: str | None
    ) -> object:
        """Build a named runtime branch.

        Returns:
            The runtime branch.

        """
        return self.parallel_branch(func=run, name=name)


@dataclass(frozen=True, slots=True)
class RetryOptions:
    """How a step retries after a failed attempt.

    What is left unset is left unset: the option is omitted from the config
    handed to the runtime, so the runtime's own default applies to that field
    alone. Naming particular numbers here would be asserting defaults this
    package does not own and cannot keep current.
    """

    # Total attempts, including the first.
    attempts: int | None = None
    initial_delay: Duration | None = None
    max_delay: Duration | None = None
    backoff_rate: float | None = None
    # Retry only errors whose message matches one of these.
    retry_on: Sequence[str] | None = None
    retry_on_types: Sequence[type[Exception]] | None = None


Retry: TypeAlias = (
    "bool | RetryOptions | Callable[[Exception, int], RetryDecision] | None"
)


@dataclass(frozen=True, slots=True)
class WaitUntilOptions(Generic[T]):
    """How `wait_until` polls, and what it polls for."""

    # Stop waiting once this returns true for the state the check returned.
    until: Callable[[T], bool]
    # The state a check receives. Required, and distinguished from an explicit
    # None: the wait starts by asking `until` about it. Treat it as the state
    # every check starts from rather than an accumulator -- a check should
    # decide from what it observes now, because the platform does not promise
    # to carry a previous check's return into the next one.
    initial_state: T | _Unset = _UNSET
    # Delay before the second check, then multiplied by backoff_rate up to
    # max_interval.
    interval: Duration | None = None
    max_interval: Duration | None = None
    backoff_rate: float | None = None
    # How many times to check before giving up. Running out fails the
    # execution rather than returning the last state.
    max_attempts: int | None = None
    # Refused rather than honoured; see _NO_TIMEOUT.
    timeout: Duration | None = None


@dataclass(frozen=True, slots=True)
class BatchOptions:
    """How many items of a `map` or `parallel` run at once, and when to stop."""

    # How many items or branches run at once. Unlimited by default.
    concurrency: int | None = None
    # Finish as soon as this many items have succeeded.
    min_succeeded: int | None = None


@dataclass(frozen=True, slots=True)
class ParallelBranch(Generic[T]):
    """A branch of `ctx.parallel`, named for the execution history."""

    run: Callable[[DurableContext], T]
    name: str | None = None


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


@dataclass(frozen=True, slots=True)
class StepScope:
    """What a step's function is given: logging, and which attempt it is on.

    A step gets a scope rather than a context on purpose: it is one atomic
    operation and cannot contain durable operations of its own. Grouping
    belongs in `ctx.child`, and handing something context-shaped to a step
    would invite exactly the mistake the engine then rejects.
    """

    log: DurableLogger
    # 1 on the first attempt.
    attempt: int


@dataclass(frozen=True, slots=True)
class BatchFailure:
    """Why one item of a batch failed.

    The platform reports a failed item as its own wire object, which this
    reduces to the three fields worth reading: what went wrong, how the
    platform classified it, and whatever the failure carried with it. A handler
    logs or returns those.

    `throw_if_failed` raises the real error, for a handler that would rather
    propagate the failure than report it.
    """

    message: str | None
    type: str | None = None
    data: str | None = None


@dataclass(frozen=True, slots=True)
class BatchItem(Generic[T]):
    """One item's outcome in a `map` or `parallel` batch."""

    index: int
    status: str
    result: T | None = None
    error: BatchFailure | None = None


class BatchResult(Generic[T]):
    """The outcome of a `map` or `parallel` batch.

    Reduced to plain data from the engine's own result, which carries methods
    and enum-valued statuses: a batch is usually inspected, logged, and
    returned from the handler, so a JSON-serializable shape is worth more here
    than the engine's convenience methods.

    Only the parts that survive a replay are carried over. A batch that
    finishes early -- `min_succeeded` reached, say -- leaves items still in
    flight, and the platform does not promise to reproduce those when the
    execution resumes: the in-flight entries and the total it counted live can
    both come back different. A handler branching on one would take a different
    path the second time through, which is the thing durable execution exists
    to rule out. So `items` holds the items that finished, `completed` counts
    them, and `completion_reason` says why the batch ended.
    """

    __slots__ = (
        "_batch",
        "completed",
        "completion_reason",
        "errors",
        "failed",
        "items",
        "results",
        "succeeded",
    )

    def __init__(self, batch: _RuntimeBatch[T]) -> None:
        """Flatten an engine batch result."""
        self._batch = batch
        self.items: tuple[BatchItem[T], ...] = tuple(
            BatchItem(
                index=item.index,
                status=str(getattr(item.status, "value", item.status)).lower(),
                result=item.result,
                error=_batch_failure(item.error),
            )
            for item in _batch_items(batch)
        )
        # Only the items that succeeded, so not aligned with the input when
        # some failed.
        self.results: tuple[T, ...] = tuple(batch.get_results())
        self.errors: tuple[BatchFailure, ...] = tuple(
            failure
            for failure in (_batch_failure(error) for error in batch.get_errors())
            if failure is not None
        )
        self.succeeded: int = batch.success_count
        self.failed: int = batch.failure_count
        self.completed: int = batch.success_count + batch.failure_count
        self.completion_reason: str | None = _completion_reason(batch)

    def throw_if_failed(self) -> None:
        """Raise the first failure, if there was one."""
        self._batch.throw_if_error()


def _batch_items(batch: _RuntimeBatch[T]) -> list[_RuntimeBatchItem[T]]:
    """List the items that finished, in input order.

    The in-flight ones are left out on purpose: see `BatchResult`.

    Returns:
        Succeeded and failed items sorted by their input index.

    """
    items = [*batch.succeeded(), *batch.failed()]
    return sorted(items, key=lambda item: item.index)


def _batch_failure(error: object) -> BatchFailure | None:
    if error is None:
        return None
    return BatchFailure(
        message=getattr(error, "message", None) or str(error),
        type=getattr(error, "type", None),
        data=getattr(error, "data", None),
    )


def _completion_reason(batch: object) -> str | None:
    reason = getattr(batch, "completion_reason", None)
    if reason is None:
        return None
    return str(getattr(reason, "value", reason)).lower()


class DurableContext:
    """The durable context.

    Every method on it is checkpointed: a resumed execution replays what
    already finished instead of running it again.

    This is a facade rather than a re-export. It keeps the authoring surface to
    the operations Volcano supports, in Volcano's vocabulary, and lets
    durations be written as `"30s"` rather than `Duration.from_seconds(30)`.

    Callbacks are the deliberate omission. The engine can suspend on one, but
    completing it is an AWS API call, and nothing in Volcano -- not the
    function's own role, not the API -- can make it. Wait on your own state
    with `wait_until` instead.
    """

    __slots__ = ("_context", "_engine", "log")

    def __init__(self, context: _RuntimeContext, engine: _DurableEngine) -> None:
        """Wrap an engine context."""
        self._context = context
        self._engine = engine
        # Logs, suppressed while an operation is being replayed.
        self.log: DurableLogger = context.logger

    def step(
        self,
        name: str | Callable[[StepScope], T],
        func: Callable[[StepScope], T] | None = None,
        *,
        retry: Retry = None,
        at_most_once: bool = False,
    ) -> T:
        """Run one atomic operation and record its result.

        A step cannot contain durable operations; use `child` to group those.
        Both forms work -- a name is what the step is recorded under and is
        worth giving, but a single obvious operation reads better without one.

        `at_most_once` checkpoints before running rather than after, so an
        attempt interrupted mid-flight is not repeated on replay. Use it for
        work that must not run twice within an attempt, and pair it with
        `retry=False` to make that hold across attempts too.

        Returns:
            The operation's result, restored from its checkpoint during replay.

        """
        step_name, step_func = _named(name, func, "step")

        def run(scope: _OperationScope) -> T:
            return step_func(StepScope(scope.logger, scope.attempt))

        return self._context.step(
            run,
            step_name,
            self._engine.step_options(retry=retry, at_most_once=at_most_once),
        )

    def wait(self, name: str | Duration, duration: Duration | None = None) -> None:
        """Suspend the execution for a duration.

        The execution is not running, and not billed, while it waits.

        One argument is always the duration: a name and a duration can both be
        strings, so `wait("30s")` would otherwise be ambiguous.

        Raises:
            TypeError: A separate duration is supplied with a non-string name.

        """
        if duration is None:
            self._context.wait(self._wait_duration(name))
            return
        if not isinstance(name, str):
            raise TypeError(_INVALID_WAIT_ARGS)
        self._context.wait(self._wait_duration(duration), name)

    def child(
        self,
        name: str | Callable[[DurableContext], T],
        func: Callable[[DurableContext], T] | None = None,
    ) -> T:
        """Group operations under one recorded context, with its own replay scope.

        Returns:
            The child function's result.

        """
        child_name, child_func = _named(name, func, "child")
        engine = self._engine

        def run(context: _RuntimeContext) -> T:
            return child_func(DurableContext(context, engine))

        return self._context.run_in_child_context(run, child_name)

    def wait_until(
        self,
        check: Callable[[T, StepScope], T],
        options: WaitUntilOptions[T],
        name: str | None = None,
    ) -> T:
        """Poll until a condition holds, suspending between checks.

        The check reports the current state and `options.until` decides
        whether that is good enough; what `until` accepts is what the wait
        returns. Have the check read the state it cares about each time rather
        than build on its own previous return.

        Running out of `options.max_attempts` fails the execution rather than
        returning the last state.

        Returns:
            The first checked state accepted by `options.until`.

        """
        check_func = _callable(check, "wait_until")
        _validate_wait_options(options)
        engine = self._engine

        def check_state(state: T, scope: _OperationScope) -> T:
            return check_func(state, StepScope(scope.logger, scope.attempt))

        return self._context.wait_for_condition(
            check_state,
            engine.wait_condition_options(options),
            name,
        )

    def map(
        self,
        items: Sequence[U],
        func: Callable[[U, DurableContext, int], T],
        name: str | None = None,
        options: BatchOptions | None = None,
    ) -> BatchResult[T]:
        """Run the same work over every item, each in its own child context.

        Returns:
            Results and failures recorded before the batch's completion policy
            is satisfied.

        Raises:
            TypeError: `items` is a string rather than a sequence of items.

        """
        map_func = _callable(func, "map")
        # A string is a sequence, so mapping over one would silently run the
        # work per character rather than refuse.
        if isinstance(items, str):
            raise TypeError(_INVALID_ITEMS)
        engine = self._engine

        def run(context: _RuntimeContext, item: U, index: int, _all: list[U]) -> T:
            return map_func(item, DurableContext(context, engine), index)

        return BatchResult(
            self._context.map(
                list(items),
                run,
                name,
                engine.map_options(options),
            )
        )

    def parallel(
        self,
        branches: Sequence[Callable[[DurableContext], T] | ParallelBranch[T]],
        name: str | None = None,
        options: BatchOptions | None = None,
    ) -> BatchResult[T]:
        """Run different branches at the same time, each in its own child context.

        Returns:
            Results and failures recorded before the batch's completion policy
            is satisfied.

        """
        engine = self._engine
        return BatchResult(
            self._context.parallel(
                [self._branch(branch) for branch in branches],
                name,
                engine.parallel_options(options),
            )
        )

    def _branch(
        self, branch: Callable[[DurableContext], T] | ParallelBranch[T]
    ) -> object:
        """Adapt one branch to the engine.

        The branch's own result type is not carried through: what goes to the
        engine is an untyped callable either way, and `parallel` keeps the
        type on its own signature.

        Returns:
            A named engine branch or a callable that wraps the engine context.

        Raises:
            TypeError: The branch is neither `ParallelBranch` nor callable.

        """
        engine = self._engine
        if isinstance(branch, ParallelBranch):
            named: Callable[[DurableContext], T] = branch.run

            def run_named(context: _RuntimeContext) -> T:
                return named(DurableContext(context, engine))

            return engine.named_branch(run_named, branch.name)
        require_callable(branch, _INVALID_BRANCH)
        bare: Callable[[DurableContext], T] = branch

        def run_bare(context: _RuntimeContext) -> object:
            return bare(DurableContext(context, engine))

        return run_bare

    def _wait_duration(self, value: object) -> object:
        seconds = _to_seconds(value, "wait")
        if seconds < _MIN_WAIT_SECONDS:
            message = f"wait must be at least {_MIN_WAIT_SECONDS} second"
            raise TypeError(message)
        if seconds > _MAX_WAIT_SECONDS:
            message = f"wait must be at most {_MAX_WAIT_SECONDS} seconds (366 days)"
            raise TypeError(message)
        return self._engine.seconds(seconds)


@overload
def durable(
    handler: DurableHandler[T, U], *, logger: object = ...
) -> FunctionHandler: ...


@overload
def durable(
    handler: None = ..., *, logger: object = ...
) -> Callable[[DurableHandler[T, U]], FunctionHandler]: ...


def durable(
    handler: DurableHandler[T, U] | None = None,
    *,
    logger: object = None,
) -> FunctionHandler | Callable[[DurableHandler[T, U]], FunctionHandler]:
    """Wrap a handler so Volcano runs it as a durable execution.

    Usable bare or with options::

        @durable
        def handler(event, ctx): ...

        @durable(logger=my_logger)
        def handler(event, ctx): ...

    The handler is called with the execution's input and a durable context, in
    that order, matching a standard function's `(event, context)`.

    Returns:
        The wrapped handler, or a decorator when no handler is supplied.

    Raises:
        TypeError: The supplied handler is not callable.

    """
    if handler is None:

        def decorate(func: DurableHandler[T, U]) -> FunctionHandler:
            return durable(func, logger=logger)

        return decorate
    require_callable(handler, _REQUIRES_HANDLER)

    return _wrap_durable(handler, logger)


def _wrap_durable(
    handler: Callable[[T, DurableContext], object], logger: object
) -> FunctionHandler:
    # Wrapped on the first invocation, not here: resolving the engine is what
    # fails when the runtime is absent, and a decorator that raises at import
    # time would break a module that merely mentions a durable handler.
    wrapped: list[FunctionHandler] = []

    # functools.wraps rather than copying two attributes: __qualname__,
    # __module__, __dict__ and __wrapped__ matter to inspect.unwrap and to a
    # traceback, and leaving them pointing at this closure makes the SDK's
    # wrapper the thing a user sees when their handler fails.
    @functools.wraps(handler)
    def invoke(event: object, function_context: object) -> object:
        if not wrapped:
            engine = _Engine.load()

            def run(input_value: T, context: _RuntimeContext) -> object:
                if logger is not None:
                    context.set_logger(logger)
                return handler(input_value, DurableContext(context, engine))

            wrapped.append(engine.durable_execution(run))
        return wrapped[0](event, function_context)

    return invoke


def _validate_wait_options(options: WaitUntilOptions[T]) -> None:
    if not callable(options.until):
        raise TypeError(_REQUIRES_UNTIL)
    if options.timeout is not None:
        raise TypeError(_NO_TIMEOUT)
    if options.initial_state is _UNSET:
        raise TypeError(_REQUIRES_INITIAL_STATE)


def _named(
    name: str | Callable[_P, T] | None,
    func: Callable[_P, T] | None,
    operation: str,
) -> tuple[str | None, Callable[_P, T]]:
    """Accept both the named and unnamed form of an operation.

    The name is what the operation is recorded under, so it is worth
    encouraging, but a single obvious operation reads better without one.

    Returns:
        The optional recording name and the operation's callable.

    """
    if isinstance(name, str) or name is None:
        return name, _callable(func, operation)
    return None, _callable(name, operation)


def _callable(func: Callable[_P, T] | None, operation: str) -> Callable[_P, T]:
    if not callable(func):
        message = f"{operation}() requires a function to run"
        raise TypeError(message)
    return func


def _engine_kwargs(**entries: object) -> dict[str, object]:
    """Drop what the caller left out.

    The engine's configs are dataclasses with real defaults, so passing None
    for an absent option would override the default with a value that is then
    read for a unit it does not have.

    Returns:
        The entries whose values are not `None`.

    """
    return {key: value for key, value in entries.items() if value is not None}


def _to_seconds(value: object, field_name: str) -> int:
    """Read a duration as whole seconds.

    Accepts `"30s"`, `"1m30s"`, a whole number of seconds, or a mapping of
    days/hours/minutes/seconds.

    Returns:
        The duration in non-negative whole seconds.

    Raises:
        TypeError: The value is not a supported numeric, mapping, or string form.

    """
    if isinstance(value, (int, float)):
        return _numeric_seconds(value, field_name)
    if _is_string_keyed_mapping(value):
        return _mapping_seconds(value, field_name)
    if isinstance(value, dict):
        raise TypeError(_duration_type_error(field_name))
    if not isinstance(value, str):
        raise TypeError(_duration_type_error(field_name))
    return _parse_duration(value.strip(), field_name)


def _is_string_keyed_mapping(value: object) -> TypeGuard[dict[str, object]]:
    if not _is_object_dict(value):
        return False
    return all(isinstance(key, str) for key in value)


def _is_object_dict(value: object) -> TypeGuard[dict[object, object]]:
    return isinstance(value, dict)


def _numeric_seconds(value: object, field_name: str) -> int:
    if isinstance(value, bool):
        raise TypeError(_duration_type_error(field_name))
    if not isinstance(value, int):
        # Fractions would silently change the requested wait.
        message = f"{field_name} must be a whole number of seconds, not a fraction"
        raise TypeError(message)
    if value < 0:
        message = f"{field_name} must be a non-negative whole number of seconds"
        raise ValueError(message)
    return value


def _duration_type_error(field_name: str) -> str:
    return (
        f"{field_name} must be a duration string, a whole number of seconds, "
        f"or a mapping of {', '.join(_DURATION_FIELDS)}"
    )


def _mapping_seconds(value: dict[str, object], field_name: str) -> int:
    """Read the mapping form, refusing keys it does not have.

    Unknown keys are the reason this checks rather than forwards: a
    `{"milliseconds": 500}` would otherwise be a duration of nothing.

    Returns:
        The sum of the supplied duration fields, converted to seconds.

    Raises:
        TypeError: The mapping has unknown keys or no non-null duration fields.

    """
    unknown = sorted(key for key in value if key not in _DURATION_FIELDS)
    if unknown:
        message = (
            f"{field_name} duration takes {', '.join(_DURATION_FIELDS)} "
            f"(got {', '.join(unknown)})"
        )
        raise TypeError(message)
    if not any(value.get(key) is not None for key in _DURATION_FIELDS):
        message = f"{field_name} duration needs one of {', '.join(_DURATION_FIELDS)}"
        raise TypeError(message)
    return sum(
        _duration_part(value.get(key), field_name, key) * _FIELD_UNITS[key]
        for key in _DURATION_FIELDS
    )


def _duration_part(part: object, field_name: str, key: str) -> int:
    if part is None:
        return 0
    if isinstance(part, bool) or not isinstance(part, int) or part < 0:
        message = f"{field_name} duration {key} must be a non-negative whole number"
        raise ValueError(message)
    return part


def _parse_duration(text: str, field_name: str) -> int:
    """Scan a whole number and a unit, repeated.

    Scanned rather than matched because every pattern for this grammar is
    either unreadable or the kind with adjacent quantifiers that backtracks on
    a hostile string. Whole numbers only -- "90m" says what "1.5h" would.

    Returns:
        The sum of the parsed duration segments in seconds.

    Raises:
        ValueError: The text is empty or contains an invalid number or unit.

    """
    seconds = 0
    segments = 0
    at = 0
    while at < len(text):
        if text[at] == " ":
            at += 1
            continue
        number_end = _scan(text, at, str.isdigit)
        unit_end = _scan(text, number_end, str.islower)
        unit = text[number_end:unit_end]
        if number_end == at or unit not in _DURATION_UNITS:
            break
        seconds += int(text[at:number_end]) * _DURATION_UNITS[unit]
        segments += 1
        at = unit_end
    if segments == 0 or at != len(text):
        message = (
            f"{field_name} must be a duration in whole seconds, such as '30s', "
            f"'5m', '2h', '1d' or '1m30s' (got {text!r})"
        )
        raise ValueError(message)
    return seconds


def _scan(text: str, start: int, accept: Callable[[str], bool]) -> int:
    for at in range(start, len(text)):
        if not accept(text[at]):
            return at
    return len(text)
