"""Configuration values shared by durable authoring and its runtime adapter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeAlias

from typing_extensions import TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from aws_durable_execution_sdk_python.retries import RetryDecision


T = TypeVar("T", default=object)
Duration: TypeAlias = "str | int | dict[str, int]"


class Unset:
    """Distinguish omitted initial state from the legitimate state None."""

    __slots__: tuple[str, ...] = ()


UNSET = Unset()


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
    initial_state: T | Unset = UNSET
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
