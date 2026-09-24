"""Optional auth operations reject transports without the requested capability."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from volcano_sdk import Session

from .client_inspection import InspectedClient
from .transport_fixtures import RejectingTransport

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
    client = InspectedClient(anon_key="anon", _transport=RejectingTransport())

    with pytest.raises(TypeError, match="requested auth operation"):
        _ = operation(client.auth)


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
    client = InspectedClient(anon_key="anon", _transport=RejectingTransport())
    _ = client.auth.set_session(Session("access", "refresh", "user"))

    with pytest.raises(TypeError, match="requested auth operation"):
        _ = operation(client.auth)


_SESSION_OPERATIONS: tuple[Callable[[Auth], object], ...] = (
    lambda auth: auth.delete_all_other_sessions(),
    lambda auth: auth.list_sessions(),
    lambda auth: auth.delete_session(session_id="session-id"),
)


@pytest.mark.parametrize(
    "operation",
    _SESSION_OPERATIONS,
    ids=("delete-other-sessions", "list-sessions", "delete-session"),
)
def test_session_operation_requires_transport_capability(
    operation: Callable[[Auth], object],
) -> None:
    client = InspectedClient(anon_key="anon", _transport=RejectingTransport())
    _ = client.auth.set_session(Session("access", "refresh", "user"))

    with pytest.raises(TypeError, match="requested auth operation"):
        _ = operation(client.auth)


def test_access_session_revocation_requires_transport_capability() -> None:
    client = InspectedClient(anon_key="anon", _transport=RejectingTransport())

    with pytest.raises(TypeError, match="requested auth operation"):
        client.requests.revoke_access_session(
            Session("access", "refresh", "user"),
            "session-id",
            None,
            joined=False,
        )


_PROFILE_OPERATIONS: tuple[Callable[[Auth], object], ...] = (
    lambda auth: auth.convert_anonymous(email="user@example.com", password="password"),
    lambda auth: auth.get_user(),
    lambda auth: auth.update_user(metadata={"name": "User"}),
)


@pytest.mark.parametrize(
    "operation",
    _PROFILE_OPERATIONS,
    ids=("convert-anonymous", "get-user", "update-user"),
)
def test_profile_operation_requires_transport_capability(
    operation: Callable[[Auth], object],
) -> None:
    client = InspectedClient(anon_key="anon", _transport=RejectingTransport())
    _ = client.auth.set_session(Session("access", "refresh", "user"))

    with pytest.raises(TypeError, match="requested auth operation"):
        _ = operation(client.auth)
