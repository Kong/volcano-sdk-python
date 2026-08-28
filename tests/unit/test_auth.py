from __future__ import annotations

from dataclasses import FrozenInstanceError, dataclass, fields
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

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
    VolcanoClient,
)
from volcano_sdk.errors import AuthenticationError, ServerError, ValidationError

if TYPE_CHECKING:
    from collections.abc import Callable


@dataclass(frozen=True)
class AuthResponse:
    status_code: int
    payload: Any = None
    content: bytes = b""
    headers: dict[str, str] | None = None


def _user_payload(*, email: str = "user@example.com") -> dict[str, Any]:
    return {
        "id": "user-123",
        "email": email,
        "project_id": "project-123",
        "email_confirmed": True,
        "user_metadata": {"display_name": "User"},
        "app_metadata": {"role": "developer"},
        "avatar_url": "https://example.com/avatar.png",
        "status": "active",
        "last_sign_in_at": "2026-08-28T12:00:00Z",
        "created_at": "2026-08-27T12:00:00Z",
        "updated_at": "2026-08-28T12:00:00Z",
    }


def _token_payload(
    *,
    access_token: str,
    refresh_token: str,
    email: str = "user@example.com",
) -> dict[str, Any]:
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": 3600,
        "user": _user_payload(email=email),
    }


class AuthTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.responses: dict[str, list[AuthResponse]] = {}

    def queue(self, operation: str, *responses: AuthResponse) -> None:
        self.responses.setdefault(operation, []).extend(responses)

    def _invoke(self, operation: str, kwargs: dict[str, Any]) -> AuthResponse:
        self.calls.append((operation, kwargs))
        responses = self.responses.get(operation)
        if not responses:
            message = f"no response queued for {operation}"
            raise AssertionError(message)
        return responses.pop(0)

    def auth_signup(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_signup", kwargs)

    def auth_signin(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_signin", kwargs)

    def auth_refresh(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_refresh", kwargs)

    def auth_logout(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_logout", kwargs)

    def auth_get_user(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_get_user", kwargs)

    def auth_update_user(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_update_user", kwargs)


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


def test_sign_up_returns_a_sessionless_result() -> None:
    transport = AuthTransport()
    transport.queue(
        "auth_signup",
        AuthResponse(
            201,
            {
                "confirmation_required": True,
                "message": "Check your email",
            },
        ),
    )
    client = VolcanoClient(anon_key="anon-key", _transport=transport)

    result = client.auth.sign_up(
        email="user@example.com",
        password="secret",
        user_metadata={"display_name": "User"},
    )

    assert result == SignUpResult(
        confirmation_required=True,
        message="Check your email",
    )
    assert client.current_session is None
    assert client.current_user is None
    assert transport.calls == [
        (
            "auth_signup",
            {
                "authorization": "anon-key",
                "email": "user@example.com",
                "password": "secret",
                "user_metadata": {"display_name": "User"},
            },
        )
    ]


def test_sign_up_can_sign_in_immediately_when_confirmation_is_not_required() -> None:
    transport = AuthTransport()
    transport.queue(
        "auth_signup",
        AuthResponse(
            201,
            {
                "confirmation_required": False,
                "message": "Account created",
            },
        ),
    )
    transport.queue(
        "auth_signin",
        AuthResponse(
            200,
            _token_payload(
                access_token="access-token",
                refresh_token="refresh-token",
            ),
        ),
    )
    client = VolcanoClient(anon_key="anon-key", _transport=transport)

    result = client.auth.sign_up(
        email="user@example.com",
        password="secret",
        sign_in=True,
    )

    assert result.user is client.current_user
    assert result.session is client.current_session
    assert result.confirmation_required is False
    assert [operation for operation, _ in transport.calls] == [
        "auth_signup",
        "auth_signin",
    ]


def test_sign_up_raises_the_typed_api_error() -> None:
    transport = AuthTransport()
    transport.queue(
        "auth_signup",
        AuthResponse(422, {"error": "Password is too short"}),
    )
    client = VolcanoClient(anon_key="anon-key", _transport=transport)

    with pytest.raises(ValidationError, match="Password is too short"):
        client.auth.sign_up(email="user@example.com", password="short")


def test_sign_in_commits_session_and_user_before_notifying_listeners() -> None:
    transport = AuthTransport()
    transport.queue(
        "auth_signin",
        AuthResponse(
            200,
            _token_payload(
                access_token="access-token",
                refresh_token="refresh-token",
            ),
        ),
    )
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    observations: list[tuple[Session | None, User | None, User | None]] = []

    client.auth.on_auth_state_change(
        lambda user: observations.append(
            (client.current_session, client.current_user, user)
        )
    )

    session = client.auth.sign_in(email="user@example.com", password="secret")

    assert session == Session(
        access_token="access-token",
        refresh_token="refresh-token",
        expires_in=3600,
        user_id="user-123",
    )
    assert client.current_session is session
    assert client.current_user == User(
        id="user-123",
        email="user@example.com",
        project_id="project-123",
        email_confirmed=True,
        user_metadata={"display_name": "User"},
        app_metadata={"role": "developer"},
        avatar_url="https://example.com/avatar.png",
        status="active",
        last_sign_in_at=datetime(2026, 8, 28, 12, tzinfo=UTC),
        created_at=datetime(2026, 8, 27, 12, tzinfo=UTC),
        updated_at=datetime(2026, 8, 28, 12, tzinfo=UTC),
    )
    assert observations[0] == (None, None, None)
    assert observations[1] == (
        client.current_session,
        client.current_user,
        client.current_user,
    )


def test_get_and_update_user_preserve_the_current_session() -> None:
    transport = AuthTransport()
    transport.queue("auth_get_user", AuthResponse(200, {"user": _user_payload()}))
    transport.queue(
        "auth_update_user",
        AuthResponse(
            200,
            {"user": _user_payload(email="updated@example.com")},
        ),
    )
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="access-token",
        refresh_token="refresh-token",
        _transport=transport,
    )
    session = client.current_session

    fetched = client.auth.get_user()
    updated = client.auth.update_user(
        password="new-password",
        user_metadata={"display_name": "Updated"},
    )

    assert fetched.email == "user@example.com"
    assert updated.email == "updated@example.com"
    assert client.current_user is updated
    assert client.current_session is session
    assert transport.calls == [
        ("auth_get_user", {"authorization": "access-token"}),
        (
            "auth_update_user",
            {
                "authorization": "access-token",
                "password": "new-password",
                "user_metadata": {"display_name": "Updated"},
            },
        ),
    ]


def test_refresh_rotates_tokens_and_replaces_user_state() -> None:
    transport = AuthTransport()
    transport.queue(
        "auth_refresh",
        AuthResponse(
            200,
            _token_payload(
                access_token="access-token-2",
                refresh_token="refresh-token-2",
                email="updated@example.com",
            ),
        ),
    )
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="access-token-1",
        refresh_token="refresh-token-1",
        _transport=transport,
    )

    session = client.auth.refresh_session()

    assert session.access_token == "access-token-2"
    assert session.refresh_token == "refresh-token-2"
    assert client.current_session is session
    assert client.current_user is not None
    assert client.current_user.email == "updated@example.com"
    assert transport.calls == [
        (
            "auth_refresh",
            {
                "authorization": "anon-key",
                "refresh_token": "refresh-token-1",
            },
        )
    ]


def test_refresh_without_a_refresh_token_clears_local_auth() -> None:
    client = VolcanoClient(anon_key="anon-key", access_token="access-token")
    client._set_user(User(id="user-123", email="user@example.com"))

    with pytest.raises(AuthenticationError, match="No refresh token available"):
        client.auth.refresh_session()

    assert client.current_session is None
    assert client.current_user is None


def test_failed_refresh_clears_local_auth() -> None:
    transport = AuthTransport()
    transport.queue(
        "auth_refresh",
        AuthResponse(401, {"error": "Refresh token expired"}),
    )
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="access-token",
        refresh_token="refresh-token",
        _transport=transport,
    )
    client._set_user(User(id="user-123", email="user@example.com"))

    with pytest.raises(AuthenticationError, match="Refresh token expired"):
        client.auth.refresh_session()

    assert client.current_session is None
    assert client.current_user is None


def test_authenticated_request_refreshes_once_and_replays() -> None:
    transport = AuthTransport()
    transport.queue(
        "auth_get_user",
        AuthResponse(401, {"error": "Access token expired"}),
        AuthResponse(200, {"user": _user_payload(email="fresh@example.com")}),
    )
    transport.queue(
        "auth_refresh",
        AuthResponse(
            200,
            _token_payload(
                access_token="access-token-2",
                refresh_token="refresh-token-2",
            ),
        ),
    )
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="access-token-1",
        refresh_token="refresh-token-1",
        _transport=transport,
    )

    user = client.auth.get_user()

    assert user.email == "fresh@example.com"
    assert transport.calls == [
        ("auth_get_user", {"authorization": "access-token-1"}),
        (
            "auth_refresh",
            {
                "authorization": "anon-key",
                "refresh_token": "refresh-token-1",
            },
        ),
        ("auth_get_user", {"authorization": "access-token-2"}),
    ]


def test_sign_out_always_clears_local_auth() -> None:
    transport = AuthTransport()
    transport.queue("auth_logout", AuthResponse(204))
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="access-token",
        refresh_token="refresh-token",
        _transport=transport,
    )
    client._set_user(User(id="user-123", email="user@example.com"))

    client.auth.sign_out()

    assert client.current_session is None
    assert client.current_user is None

    transport.queue("auth_logout", AuthResponse(500, {"error": "Logout failed"}))
    client._commit_auth(
        Session(access_token="access-token", refresh_token="refresh-token"),
        User(id="user-123", email="user@example.com"),
    )

    with pytest.raises(ServerError, match="Logout failed"):
        client.auth.sign_out()

    assert client.current_session is None
    assert client.current_user is None


def test_auth_state_listeners_are_immediate_isolated_and_idempotent(
    caplog: pytest.LogCaptureFixture,
) -> None:
    client = VolcanoClient(anon_key="anon-key")
    observed: list[tuple[str, User | None]] = []
    second_unsubscribers: list[Callable[[], None]] = []

    def first(user: User | None) -> None:
        observed.append(("first", user))
        if user is not None and second_unsubscribers:
            second_unsubscribers[0]()

    def failing(_user: User | None) -> None:
        listener_error_message = "refresh-token-secret"
        raise RuntimeError(listener_error_message)

    unsubscribe_first = client.auth.on_auth_state_change(first)
    client.auth.on_auth_state_change(failing)
    second_unsubscribers.append(
        client.auth.on_auth_state_change(lambda user: observed.append(("second", user)))
    )
    observed.clear()
    caplog.clear()
    user = User(id="user-123", email="user@example.com")

    client._set_user(user)

    assert observed == [("first", user), ("second", user)]
    assert "Authentication state listener failed" in caplog.text
    assert "refresh-token-secret" not in caplog.text

    unsubscribe_first()
    unsubscribe_first()
    client._clear_auth()

    assert observed == [("first", user), ("second", user)]
