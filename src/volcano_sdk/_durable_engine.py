"""Translate authoring options to the lazily imported durable runtime."""

from __future__ import annotations

from dataclasses import replace
from functools import cache
from typing import TYPE_CHECKING

from typing_extensions import TypeVar

from ._durable_duration import to_seconds
from ._durable_modules import load_config, load_retries, load_root, load_waits
from ._durable_options import BatchOptions, RetryOptions, Unset

if TYPE_CHECKING:
    from collections.abc import Callable

    from aws_durable_execution_sdk_python.config import (
        CompletionConfig,
        MapConfig,
        ParallelBranch,
        ParallelConfig,
        StepConfig,
        StepSemantics,
    )
    from aws_durable_execution_sdk_python.config import Duration as EngineDuration
    from aws_durable_execution_sdk_python.retries import (
        RetryDecision,
        RetryStrategyConfig,
    )
    from aws_durable_execution_sdk_python.waits import WaitStrategyConfig

    from ._durable_modules import (
        CreateWaitStrategy,
        DurableExecution,
        WaitConfigFactory,
        WaitStrategyFactory,
    )
    from ._durable_options import Retry, WaitUntilOptions
    from ._durable_protocols import RuntimeContext

T = TypeVar("T", default=object)
_ENGINE_EXTRA = "volcano-sdk-python[durable]"
_INVALID_RETRY = "retry must be False, a callable, or a RetryOptions"


class DurableRuntimeMissingError(Exception):
    """Raised when the durable runtime is not available.

    Volcano installs the runtime when it builds a function deployed as
    durable, so this means the handler is running somewhere durable execution
    does not exist: a function that was not deployed as durable, or a local
    script.
    """

    def __init__(self, cause: BaseException | None = None) -> None:
        """Explain that durable execution is not available here."""
        message = (
            "Durable execution is not available here. Volcano provides the "
            "durable runtime when it builds a function deployed as durable, so "
            "deploy this one that way (`volcano cloud durable deploy`, or "
            "`kind: durable` in volcano-config.yaml). Durable execution is a "
            f"cloud capability and does not run locally; to exercise a handler "
            f"in your own tests, install `{_ENGINE_EXTRA}`."
        )
        super().__init__(message)
        self.__cause__: BaseException | None = cause


class Engine:
    """The durable protocol, from the AWS durable execution SDK.

    Resolved on first use rather than imported at module scope, because the
    Volcano SDK also runs in standard functions and scripts where the runtime
    is absent, and a missing engine is worth a real error message instead of
    an ImportError from an unfamiliar package.
    """

    def __init__(self) -> None:
        """Resolve the engine's public surface.

        Raises:
            DurableRuntimeMissingError: The runtime or a required module cannot
                be imported.

        """
        try:
            config = load_config()
            retries = load_retries()
            waits = load_waits()
            root = load_root()
        except ImportError as error:
            raise DurableRuntimeMissingError from error
        self.durable_execution: DurableExecution = root.durable_execution
        self.duration: type[EngineDuration] = config.Duration
        self.step_config: type[StepConfig] = config.StepConfig
        self.step_semantics: type[StepSemantics] = config.StepSemantics
        self.map_config: type[MapConfig[object]] = config.MapConfig
        self.parallel_config: type[ParallelConfig] = config.ParallelConfig
        self.completion_config: type[CompletionConfig] = config.CompletionConfig
        self.parallel_branch: type[ParallelBranch[object]] = config.ParallelBranch
        self.create_retry_strategy: Callable[
            [RetryStrategyConfig], Callable[[Exception, int], RetryDecision]
        ] = retries.create_retry_strategy
        self.retry_strategy_config: type[RetryStrategyConfig] = (
            retries.RetryStrategyConfig
        )
        self.retry_decision: type[RetryDecision] = retries.RetryDecision
        self.create_wait_strategy: CreateWaitStrategy = waits.create_wait_strategy
        self.wait_strategy_config: WaitStrategyFactory = waits.WaitStrategyConfig
        self.wait_for_condition_config: WaitConfigFactory = waits.WaitForConditionConfig

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
                to_seconds(retry.initial_delay, "initial_delay")
            )
        if retry.max_delay is not None:
            config.max_delay = self.seconds(to_seconds(retry.max_delay, "max_delay"))
        if retry.backoff_rate is not None:
            config.backoff_rate = retry.backoff_rate

    @staticmethod
    def _set_retry_filters(config: RetryStrategyConfig, retry: RetryOptions) -> None:
        if retry.retry_on is not None:
            config.retryable_errors = list(retry.retry_on)
        if retry.retry_on_types is not None:
            config.retryable_error_types = list(retry.retry_on_types)

    def wait_condition_options(self, options: WaitUntilOptions[T]) -> object:
        """Build the runtime's polling options.

        Returns:
            The runtime wait condition configuration.

        Raises:
            TypeError: The caller omitted the required initial state.

        """
        initial_state = options.initial_state
        if isinstance(initial_state, Unset):
            message = (
                "wait_until() requires an `initial_state`, which is what `until` "
                "is given until the state changes"
            )
            raise TypeError(message)
        until = options.until

        def keep_polling(state: T) -> bool:
            return not until(state)

        strategy = self.wait_strategy_config(should_continue_polling=keep_polling)
        self._set_wait_timing(strategy, options)
        return self.wait_for_condition_config(
            wait_strategy=self.create_wait_strategy(strategy),
            initial_state=initial_state,
        )

    def _set_wait_timing(
        self, config: WaitStrategyConfig[T], options: WaitUntilOptions[T]
    ) -> None:
        if options.max_attempts is not None:
            config.max_attempts = options.max_attempts
        if options.interval is not None:
            config.initial_delay = self.seconds(
                to_seconds(options.interval, "interval")
            )
        if options.max_interval is not None:
            config.max_delay = self.seconds(
                to_seconds(options.max_interval, "max_interval")
            )
        if options.backoff_rate is not None:
            config.backoff_rate = options.backoff_rate

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
        self, run: Callable[[RuntimeContext], object], name: str | None
    ) -> object:
        """Build a named runtime branch.

        Returns:
            The runtime branch.

        """
        return self.parallel_branch(func=run, name=name)


@cache
def load_engine() -> Engine:
    """Resolve the optional engine once per process.

    Returns:
        The cached engine adapter.

    """
    return Engine()
