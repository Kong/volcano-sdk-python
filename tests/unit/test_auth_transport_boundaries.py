"""Optional auth operations reject transports without the requested capability."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from transport_fixtures import RejectingTransport

from volcano_sdk import Session, VolcanoClient

if TYPE_CHECKING:
    from collections.abc import Callable

    from volcano_sdk.auth import Auth


_AUTH_OPERATIONS: tuple[Callable[[Auth], object], ...] = (
    lambda auth: auth.sign_up(email="user@example.com", password="password"),
    lambda auth: auth.sign_in_anonymously(),
    lambda auth: auth.reset_password_for_email(email="user@example.com"),
    lambda auth: auth.confirm_email(token="confirmation-token"),
    lambda auth: auth.resend_confirmation(email="user@example.com"),
    lambda auth: auth.reset_password(
        token="recovery-token", new_password="new-password"
    ),
)


@pytest.mark.parametrize(
    "operation",
    _AUTH_OPERATIONS,
    ids=(
        "sign-up",
        "anonymous-sign-up",
        "forgot-password",
        "confirm-email",
        "resend-confirmation",
        "reset-password",
    ),
)
def test_optional_auth_operation_requires_transport_capability(
    operation: Callable[[Auth], object],
) -> None:
    client = VolcanoClient(anon_key="anon", _transport=RejectingTransport())

    with pytest.raises(TypeError, match="requested auth operation"):
        operation(client.auth)


_EMAIL_CHANGE_OPERATIONS: tuple[Callable[[Auth], object], ...] = (
    lambda auth: auth.request_email_change(new_email="new@example.com"),
    lambda auth: auth.cancel_email_change(),
    lambda auth: auth.confirm_email_change(token="confirmation-token"),
)


@pytest.mark.parametrize(
    "operation",
    _EMAIL_CHANGE_OPERATIONS,
    ids=("request-email-change", "cancel-email-change", "confirm-email-change"),
)
def test_email_change_requires_transport_capability_after_session_check(
    operation: Callable[[Auth], object],
) -> None:
    client = VolcanoClient(anon_key="anon", _transport=RejectingTransport())
    client.auth.set_session(Session("access", "refresh", "user"))

    with pytest.raises(TypeError, match="requested auth operation"):
        operation(client.auth)
