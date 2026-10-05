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
from collections.abc import Callable
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Generic,
    Never,
    TypeAlias,
    overload,
)

from typing_extensions import TypeVar

from ._callbacks import named_operation, operation_callable, require_callable
from ._durable_duration import to_seconds
from ._durable_engine import DurableRuntimeMissingError, load_engine
from ._durable_options import (
    BatchOptions,
    Duration,
    Retry,
    RetryOptions,
    WaitUntilOptions,
)
from ._durable_protocols import (
    DurableEngine,
    DurableLogger,
    OperationScope,
    RuntimeContext,
)
from ._durable_results import BatchFailure, BatchItem, BatchResult

if TYPE_CHECKING:
    from collections.abc import Sequence


__all__ = [
    "BatchFailure",
    "BatchItem",
    "BatchOptions",
    "BatchResult",
    "DurableContext",
    "DurableHandler",
    "DurableLogger",
    "DurableRuntimeMissingError",
    "Duration",
    "FunctionHandler",
    "ParallelBranch",
    "Retry",
    "RetryOptions",
    "StepScope",
    "WaitUntilOptions",
    "durable",
]

T = TypeVar("T", default=object)
U = TypeVar("U", default=object)
# An unsubscripted public handler can accept a specific input type without
# promising that callers may pass an arbitrary object to it.
_Input = TypeVar("_Input", default=Never)
_Output = TypeVar("_Output", default=object)
# A duration: "30s", "5m", "2h", "1d", a compound string like "1m30s", a whole
# number of seconds, or the mapping form.
# What a durable function is written as, and what the platform invokes it as.
# The second argument differs: the handler is given a durable context, and the
# wrapper is given the invocation's own context.
DurableHandler: TypeAlias = Callable[[_Input, "DurableContext"], _Output]
# Invocation envelopes are distinct from the user handler's input and result.
FunctionHandler: TypeAlias = "Callable[[object, object], object]"

_MIN_WAIT_SECONDS = 1
_MAX_WAIT_SECONDS = 31622400
_REQUIRES_HANDLER = "durable(handler) requires a callable"
_REQUIRES_UNTIL = "wait_until() requires an `until` predicate"
# A condition is bounded by how many times it is checked, not by a deadline:
# the platform holds the wait between checks and has no clock to compare
# against when it resumes. Refused rather than ignored, because a wait meant to
# give up after an hour would otherwise poll to the execution's own ceiling.
_NO_TIMEOUT = (
    "wait_until() has no `timeout`: bound the wait with `max_attempts`, "
    "`interval` and `max_interval`"
)
_INVALID_BRANCH = "a parallel branch is a callable, or a ParallelBranch"
_INVALID_ITEMS = "map() requires a sequence of items"
_INVALID_WAIT_ARGS = "wait() takes a name and a duration, or a duration alone"


@dataclass(frozen=True, slots=True)
class ParallelBranch(Generic[T]):
    """A branch of `ctx.parallel`, named for the execution history."""

    run: Callable[[DurableContext], T]
    name: str | None = None


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

    __slots__: tuple[str, ...] = ("_context", "_engine", "log")

    def __init__(self, context: RuntimeContext, engine: DurableEngine) -> None:
        """Wrap an engine context."""
        self._context: RuntimeContext = context
        self._engine: DurableEngine = engine
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
        step_name, step_func = named_operation(name, func, "step")

        def run(scope: OperationScope) -> T:
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
        child_name, child_func = named_operation(name, func, "child")
        engine = self._engine

        def run(context: RuntimeContext) -> T:
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
        check_func = operation_callable(check, "wait_until")
        _validate_wait_options(options)
        engine = self._engine

        def check_state(state: T, scope: OperationScope) -> T:
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
        map_func = operation_callable(func, "map")
        # A string is a sequence, so mapping over one would silently run the
        # work per character rather than refuse.
        if isinstance(items, str):
            raise TypeError(_INVALID_ITEMS)
        engine = self._engine

        def run(context: RuntimeContext, item: U, index: int, _all: list[U]) -> T:
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

        """
        engine = self._engine
        if isinstance(branch, ParallelBranch):
            named: Callable[[DurableContext], T] = branch.run

            def run_named(context: RuntimeContext) -> T:
                return named(DurableContext(context, engine))

            return engine.named_branch(run_named, branch.name)
        require_callable(branch, _INVALID_BRANCH)
        bare: Callable[[DurableContext], T] = branch

        def run_bare(context: RuntimeContext) -> object:
            return bare(DurableContext(context, engine))

        return run_bare

    def _wait_duration(self, value: object) -> object:
        seconds = to_seconds(value, "wait")
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
            engine = load_engine()

            def run(input_value: T, context: RuntimeContext) -> object:
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
