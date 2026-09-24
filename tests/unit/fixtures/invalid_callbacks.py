"""Invalid callback arguments checked statically and exercised at runtime."""

from __future__ import annotations

from typing import TYPE_CHECKING

from volcano_sdk.durable_authoring import durable

if TYPE_CHECKING:
    from volcano_sdk.auth import Auth
    from volcano_sdk.durable_authoring import DurableContext


def register_non_callable_auth(auth: Auth) -> None:
    _ = auth.on_auth_state_change(None)  # type: ignore[arg-type]


def decorate_non_callable() -> None:
    durable("not a handler")  # type: ignore[call-overload]


def register_non_callable_branch(context: DurableContext) -> None:
    _ = context.parallel(["not a branch"])  # type: ignore[list-item]


def use_non_callable_retry(context: DurableContext) -> None:
    context.step("charge", lambda _scope: None, retry="aggressively")  # type: ignore[arg-type]
