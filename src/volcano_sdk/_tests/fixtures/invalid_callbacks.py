"""Invalid callback arguments checked statically and exercised at runtime."""

from __future__ import annotations

from volcano_sdk._tests.typing import TYPE_CHECKING
from volcano_sdk.durable_authoring import WaitUntilOptions, durable

if TYPE_CHECKING:
    from volcano_sdk.auth import Auth
    from volcano_sdk.durable_authoring import DurableContext


def register_non_callable_auth(auth: Auth) -> None:
    _ = auth.on_auth_state_change(None)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


def decorate_non_callable() -> None:
    durable("not a handler")  # type: ignore[call-overload]  # pyright: ignore[reportArgumentType, reportCallIssue]


def register_non_callable_branch(context: DurableContext) -> None:
    _ = context.parallel(["not a branch"])  # type: ignore[list-item]  # pyright: ignore[reportArgumentType]


def register_non_callable_map(context: DurableContext) -> None:
    _ = context.map([1], None)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


def register_non_callable_wait(context: DurableContext) -> None:
    options = WaitUntilOptions(until=lambda state: state, initial_state=False)
    _ = context.wait_until(None, options)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


def run_non_callable_operation(context: DurableContext, operation: str) -> object:
    if operation == "step":
        return context.step("named", "not a function")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
    return context.child("named", "not a function")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


def use_non_callable_retry(context: DurableContext) -> None:
    context.step("charge", lambda _scope: None, retry="aggressively")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
