from __future__ import annotations

from dataclasses import FrozenInstanceError, fields
from datetime import UTC, datetime

import pytest

from volcano_sdk import (
    AuthorizationRequest,
    AuthSession,
    EmailChangeResult,
    MessageResult,
    OAuthProvider,
    OAuthProviderName,
    OAuthTokenResult,
    Session,
    SessionPage,
    SignUpResult,
    User,
)


def test_public_auth_values_are_frozen_and_slotted() -> None:
    user = User(id="user-123", email="user@example.com")
    session = Session(access_token="access-token")
    values = (
        user,
        session,
        SignUpResult(
            confirmation_required=True,
            message="Check your email",
            user=user,
            session=session,
        ),
        MessageResult(message="Done"),
        EmailChangeResult(
            message="Check your email",
            new_email="new@example.com",
            email_change_token="email-change-token",
        ),
        AuthorizationRequest(
            authorization_url="https://auth.example/authorize?state=oauth-state",
            state="oauth-state",
        ),
        OAuthProvider(
            provider="github",
            linked_at=datetime(2026, 8, 28, tzinfo=UTC),
        ),
        OAuthTokenResult(
            provider="github",
            expires_in=3600,
            message="Refreshed",
        ),
        AuthSession(
            id="session-123",
            user_id="user-123",
            provider="email",
            expires_at=datetime(2026, 8, 29, tzinfo=UTC),
            is_active=True,
            is_current=True,
        ),
        SessionPage(
            sessions=(),
            total=0,
            page=1,
            limit=20,
            total_pages=0,
        ),
    )

    for value in values:
        assert not hasattr(value, "__dict__")
        first_field = fields(value)[0].name
        with pytest.raises(FrozenInstanceError):
            setattr(value, first_field, None)


def test_public_auth_value_annotations_do_not_expose_generated_models() -> None:
    public_values = (
        User,
        Session,
        SignUpResult,
        MessageResult,
        EmailChangeResult,
        AuthorizationRequest,
        OAuthProvider,
        OAuthTokenResult,
        AuthSession,
        SessionPage,
    )

    for value_type in public_values:
        annotations = repr(value_type.__annotations__)
        assert "volcano_sdk._generated" not in annotations


def test_secret_auth_fields_are_absent_from_repr() -> None:
    session = Session(
        access_token="access-token",
        refresh_token="refresh-token",
    )
    email_change = EmailChangeResult(
        message="Check your email",
        new_email="new@example.com",
        email_change_token="email-change-token",
    )
    authorization = AuthorizationRequest(
        authorization_url="https://auth.example/authorize?state=oauth-state",
        state="oauth-state",
    )

    assert "access-token" not in repr(session)
    assert "refresh-token" not in repr(session)
    assert "email-change-token" not in repr(email_change)
    assert "oauth-state" not in repr(authorization)


def test_oauth_provider_name_accepts_the_supported_providers() -> None:
    providers: tuple[OAuthProviderName, ...] = (
        "google",
        "github",
        "microsoft",
        "apple",
    )

    assert providers == ("google", "github", "microsoft", "apple")
