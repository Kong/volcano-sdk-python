from __future__ import annotations

from typing import TYPE_CHECKING

from volcano_sdk.durable_authoring import WaitUntilOptions

if TYPE_CHECKING:
    from volcano_sdk.durable_authoring import DurableContext


def non_callable_predicate() -> WaitUntilOptions:
    # This invalid consumer example must fail mypy's arg-type check; the
    # unused-ignore check fails if the constructor stops enforcing its type.
    return WaitUntilOptions(until=None, initial_state=False)  # type: ignore[arg-type]


def invalid_wait_duration(context: DurableContext, duration: object) -> None:
    context.wait("cool-off", duration)  # type: ignore[arg-type]
