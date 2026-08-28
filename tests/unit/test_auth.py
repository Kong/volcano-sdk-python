from __future__ import annotations

import json
from base64 import urlsafe_b64encode
from dataclasses import FrozenInstanceError, dataclass, fields
from datetime import UTC, datetime
from threading import Event, Thread
from typing import TYPE_CHECKING, Any, cast

import pytest
from typing_extensions import override

from volcano_sdk import (
    AuthIdentity,
    AuthMethod,
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


def _user_payload(
    *,
    email: str = "user@example.com",
    email_confirmed: bool = True,
) -> dict[str, Any]:
    return {
        "id": "user-123",
        "email": email,
        "project_id": "project-123",
        "email_confirmed": email_confirmed,
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


def _access_token_for_session(session_id: str) -> str:
    payload = urlsafe_b64encode(
        json.dumps({"session_id": session_id}).encode()
    ).decode()
    return f"header.{payload.rstrip('=')}.signature"


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

    def auth_signup_anonymous(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_signup_anonymous", kwargs)

    def auth_convert_anonymous(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_convert_anonymous", kwargs)

    def auth_confirm_email(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_confirm_email", kwargs)

    def auth_resend_confirmation(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_resend_confirmation", kwargs)

    def auth_forgot_password(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_forgot_password", kwargs)

    def auth_reset_password(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_reset_password", kwargs)

    def auth_request_email_change(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_request_email_change", kwargs)

    def auth_confirm_email_change(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_confirm_email_change", kwargs)

    def auth_cancel_email_change(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_cancel_email_change", kwargs)

    def auth_oauth_authorize(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_oauth_authorize", kwargs)

    def auth_oauth_exchange(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_oauth_exchange", kwargs)

    def auth_link_oauth_provider(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_link_oauth_provider", kwargs)

    def auth_unlink_oauth_provider(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_unlink_oauth_provider", kwargs)

    def auth_list_oauth_providers(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_list_oauth_providers", kwargs)

    def auth_list_identities(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_list_identities", kwargs)

    def auth_unlink_identity(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_unlink_identity", kwargs)

    def auth_list_methods(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_list_methods", kwargs)

    def auth_promote_method(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_promote_method", kwargs)

    def refresh_oauth_provider_token(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("refresh_oauth_provider_token", kwargs)

    def get_oauth_provider_token(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("get_oauth_provider_token", kwargs)

    def call_oauth_provider_api(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("call_oauth_provider_api", kwargs)

    def auth_get_my_sessions(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_get_my_sessions", kwargs)

    def auth_delete_my_session(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_delete_my_session", kwargs)

    def auth_delete_all_my_sessions(self, **kwargs: Any) -> AuthResponse:
        return self._invoke("auth_delete_all_my_sessions", kwargs)


class BlockingAuthTransport(AuthTransport):
    def __init__(self, operation: str) -> None:
        super().__init__()
        self._operation = operation
        self._blocked = False
        self.entered = Event()
        self.release = Event()
        self.called = Event()

    @override
    def _invoke(self, operation: str, kwargs: dict[str, Any]) -> AuthResponse:
        response = super()._invoke(operation, kwargs)
        self.called.set()
        if operation == self._operation and not self._blocked:
            self._blocked = True
            self.entered.set()
            if not self.release.wait(timeout=1):
                message = "timed out waiting to release auth transport"
                raise AssertionError(message)
        return response


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
        AuthIdentity(
            id="identity-id",
            email="user@example.com",
            email_verified=True,
            is_primary=True,
            created_at=datetime(2026, 8, 27, tzinfo=UTC),
        ),
        AuthMethod(
            id="method-id",
            type="password",
            identity_id="identity-id",
            email="user@example.com",
            is_primary=True,
            created_at=datetime(2026, 8, 27, tzinfo=UTC),
            updated_at=datetime(2026, 8, 28, tzinfo=UTC),
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


def test_user_metadata_is_defensively_deeply_frozen() -> None:
    metadata: dict[str, Any] = {"nested": [{"value": "kept"}]}
    user = User(id="user-123", email="user@example.com", user_metadata=metadata)
    metadata["nested"][0]["value"] = "changed"

    nested = cast("Any", user.user_metadata)["nested"]
    assert nested[0]["value"] == "kept"
    with pytest.raises(TypeError):
        nested[0]["value"] = "changed"


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


@pytest.mark.parametrize(
    "payload",
    [
        {"message": "Check your email"},
        {"confirmation_required": True},
        {"confirmation_required": "yes", "message": "Check your email"},
    ],
)
def test_sign_up_rejects_malformed_acknowledgements(payload: dict[str, Any]) -> None:
    transport = AuthTransport()
    transport.queue("auth_signup", AuthResponse(201, payload))
    client = VolcanoClient(anon_key="anon-key", _transport=transport)

    with pytest.raises(AuthenticationError, match="missing required fields"):
        client.auth.sign_up(email="user@example.com", password="secret")


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


def test_auth_listener_can_wait_for_an_operation_on_another_thread() -> None:
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
    transport.queue(
        "auth_get_user",
        AuthResponse(
            200,
            {
                "user": _token_payload(
                    access_token="access-token",
                    refresh_token="refresh-token",
                )["user"]
            },
        ),
    )
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    completed = Event()
    outcomes: list[bool] = []
    workers: list[Thread] = []
    started = False

    def load_user() -> None:
        client.auth.get_user()
        completed.set()

    def listener(user: User | None) -> None:
        nonlocal started
        if user is None or started:
            return
        started = True
        worker = Thread(target=load_user)
        workers.append(worker)
        worker.start()
        outcomes.append(completed.wait(0.2))

    client.auth.on_auth_state_change(listener)
    client.auth.sign_in(email="user@example.com", password="secret")
    workers[0].join(timeout=1)

    assert outcomes == [True]


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


def test_authenticated_facade_normalizes_a_missing_session() -> None:
    client = VolcanoClient(anon_key="anon-key", _transport=AuthTransport())

    with pytest.raises(AuthenticationError, match="No active session"):
        client.auth.get_user()


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


def test_rejected_access_only_session_clears_local_auth() -> None:
    transport = AuthTransport()
    transport.queue(
        "auth_get_user",
        AuthResponse(401, {"error": "Access token expired"}),
    )
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="access-token",
        _transport=transport,
    )
    client._set_user(User(id="user-123", email="user@example.com"))

    with pytest.raises(AuthenticationError, match="Access token expired"):
        client.auth.get_user()

    assert client.current_session is None
    assert client.current_user is None


def test_rejected_post_refresh_retry_clears_rotated_auth() -> None:
    transport = AuthTransport()
    transport.queue(
        "auth_get_user",
        AuthResponse(401, {"error": "Access token expired"}),
        AuthResponse(401, {"error": "Session revoked"}),
    )
    transport.queue(
        "auth_refresh",
        AuthResponse(
            200,
            _token_payload(
                access_token="rotated-access",
                refresh_token="rotated-refresh",
            ),
        ),
    )
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="expired-access",
        refresh_token="refresh-token",
        _transport=transport,
    )

    with pytest.raises(AuthenticationError, match="Session revoked"):
        client.auth.get_user()

    assert client.current_session is None
    assert client.current_user is None


def test_refresh_without_local_auth_does_not_emit_another_signed_out_event() -> None:
    client = VolcanoClient(anon_key="anon-key")
    observations: list[User | None] = []
    client.auth.on_auth_state_change(observations.append)
    observations.clear()

    with pytest.raises(AuthenticationError, match="No refresh token available"):
        client.auth.refresh_session()

    assert observations == []


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


def test_immediate_auth_listener_does_not_invert_auth_state_locks() -> None:
    transport = BlockingAuthTransport("auth_get_user")
    transport.queue(
        "auth_get_user",
        AuthResponse(200, {"user": _user_payload()}),
        AuthResponse(200, {"user": _user_payload()}),
    )
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="access-token",
        _transport=transport,
    )
    client._set_user(User(id="user-123", email="user@example.com"))
    loading = Thread(target=client.auth.get_user)
    loading.start()
    assert transport.entered.wait(timeout=1)
    callback_entered = Event()

    def listener(_user: User | None) -> None:
        callback_entered.set()
        client.auth.get_user()

    subscribing = Thread(target=lambda: client.auth.on_auth_state_change(listener))
    subscribing.start()
    assert callback_entered.wait(timeout=1)
    transport.release.set()
    loading.join(timeout=1)
    subscribing.join(timeout=1)

    assert not loading.is_alive()
    assert not subscribing.is_alive()


def test_auth_listener_subscription_preserves_transition_order() -> None:
    client = VolcanoClient(anon_key="anon-key")
    user = User(id="user-123", email="user@example.com")
    client._set_user(user)
    initial_entered = Event()
    release_initial = Event()
    observations: list[User | None] = []

    def listener(current_user: User | None) -> None:
        if current_user is user:
            initial_entered.set()
            assert release_initial.wait(timeout=1)
        observations.append(current_user)

    subscribing = Thread(target=lambda: client.auth.on_auth_state_change(listener))
    subscribing.start()
    assert initial_entered.wait(timeout=1)
    client._clear_auth()
    release_initial.set()
    subscribing.join(timeout=1)

    assert not subscribing.is_alive()
    assert observations == [user, None]


def test_restored_session_listener_waits_for_user_hydration() -> None:
    transport = AuthTransport()
    transport.queue("auth_get_user", AuthResponse(200, {"user": _user_payload()}))
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="restored-access",
        _transport=transport,
    )
    observations: list[User | None] = []

    client.auth.on_auth_state_change(observations.append)
    assert observations == []

    user = client.auth.get_user()
    assert observations == [user]


def test_anonymous_and_email_account_flows_return_public_values() -> None:
    transport = AuthTransport()
    transport.queue(
        "auth_signup_anonymous",
        AuthResponse(
            201,
            _token_payload(
                access_token="anonymous-access",
                refresh_token="anonymous-refresh",
            ),
        ),
    )
    transport.queue(
        "auth_convert_anonymous",
        AuthResponse(200, {"user": _user_payload()}),
    )
    transport.queue(
        "auth_refresh",
        AuthResponse(
            200,
            _token_payload(
                access_token="converted-access",
                refresh_token="converted-refresh",
            ),
        ),
    )
    for operation in (
        "auth_resend_confirmation",
        "auth_forgot_password",
        "auth_reset_password",
        "auth_cancel_email_change",
    ):
        transport.queue(operation, AuthResponse(200, {"message": "Done"}))
    transport.queue(
        "auth_confirm_email_change",
        AuthResponse(200, {"message": "Done", "user": _user_payload()}),
    )
    transport.queue(
        "auth_request_email_change",
        AuthResponse(
            200,
            {
                "message": "Check your email",
                "new_email": "new@example.com",
                "email_change_token": "development-token",
            },
        ),
    )
    transport.queue("auth_get_user", AuthResponse(200, {"user": _user_payload()}))
    client = VolcanoClient(anon_key="anon-key", _transport=transport)

    anonymous = client.auth.sign_up_anonymous(user_metadata={"display_name": "Guest"})
    converted = client.auth.convert_anonymous(
        email="user@example.com",
        password="secret",
        user_metadata={"plan": "developer"},
    )
    messages = (
        client.auth.resend_confirmation(email="user@example.com"),
        client.auth.forgot_password(email="user@example.com"),
    )
    email_change = client.auth.request_email_change(new_email="new@example.com")
    confirm_change = client.auth.confirm_email_change(token="email-change-token")
    cancel_change = client.auth.cancel_email_change()
    user_before_reset = client.current_user
    password_reset = client.auth.reset_password(
        token="recovery-token",
        new_password="new-password",
    )

    assert anonymous is not None
    assert anonymous.access_token == "anonymous-access"
    assert client.current_session is not None
    assert client.current_session.access_token == "converted-access"
    assert user_before_reset == converted
    assert all(result == MessageResult(message="Done") for result in messages)
    assert email_change == EmailChangeResult(
        message="Check your email",
        new_email="new@example.com",
        email_change_token="development-token",
    )
    assert "development-token" not in repr(email_change)
    assert confirm_change == MessageResult(message="Done")
    assert cancel_change == MessageResult(message="Done")
    assert password_reset == MessageResult(message="Done")
    assert client.current_session is not None
    assert transport.calls[:2] == [
        (
            "auth_signup_anonymous",
            {
                "authorization": "anon-key",
                "user_metadata": {"display_name": "Guest"},
            },
        ),
        (
            "auth_convert_anonymous",
            {
                "authorization": "anonymous-access",
                "email": "user@example.com",
                "password": "secret",
                "user_metadata": {"plan": "developer"},
            },
        ),
    ]


def test_confirm_email_refreshes_current_user_and_notifies_listeners() -> None:
    transport = AuthTransport()
    transport.queue("auth_confirm_email", AuthResponse(200, {"message": "Done"}))
    transport.queue(
        "auth_get_user",
        AuthResponse(200, {"user": _user_payload(email_confirmed=True)}),
    )
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="access-token",
        refresh_token="refresh-token",
        _transport=transport,
    )
    client._set_user(
        User(id="user-123", email="user@example.com", email_confirmed=False)
    )
    observations: list[User | None] = []
    client.auth.on_auth_state_change(observations.append)

    result = client.auth.confirm_email(token="confirmation-token")

    assert result == MessageResult(message="Done")
    assert client.current_user is not None
    assert client.current_user.email_confirmed is True
    assert observations[-1] is client.current_user


def test_password_reset_clears_a_revoked_current_session() -> None:
    transport = AuthTransport()
    transport.queue("auth_reset_password", AuthResponse(200, {"message": "Done"}))
    transport.queue(
        "auth_get_user",
        AuthResponse(401, {"error": "Access token expired"}),
    )
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

    result = client.auth.reset_password(token="recovery-token", new_password="next")

    assert result == MessageResult(message="Done")
    assert client.current_session is None


def test_convert_anonymous_preserves_success_when_session_refresh_fails() -> None:
    transport = AuthTransport()
    transport.queue(
        "auth_convert_anonymous",
        AuthResponse(200, {"user": _user_payload(email="converted@example.com")}),
    )
    transport.queue(
        "auth_refresh",
        AuthResponse(503, {"error": "Temporarily unavailable"}),
    )
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="anonymous-access",
        refresh_token="anonymous-refresh",
        _transport=transport,
    )

    converted = client.auth.convert_anonymous(
        email="converted@example.com",
        password="secret",
    )

    assert converted.email == "converted@example.com"
    assert client.current_session is None


def test_convert_anonymous_serializes_replacement_auth() -> None:
    transport = BlockingAuthTransport("auth_convert_anonymous")
    transport.queue(
        "auth_convert_anonymous",
        AuthResponse(200, {"user": _user_payload(email="converted@example.com")}),
    )
    transport.queue(
        "auth_refresh",
        AuthResponse(
            200,
            _token_payload(
                access_token="converted-access",
                refresh_token="converted-refresh",
                email="converted@example.com",
            ),
        ),
    )
    transport.queue(
        "auth_signin",
        AuthResponse(
            200,
            _token_payload(
                access_token="replacement-access",
                refresh_token="replacement-refresh",
                email="replacement@example.com",
            ),
        ),
    )
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="anonymous-access",
        refresh_token="anonymous-refresh",
        _transport=transport,
    )
    converted: list[User] = []
    conversion = Thread(
        target=lambda: converted.append(
            client.auth.convert_anonymous(
                email="converted@example.com",
                password="secret",
            )
        )
    )
    conversion.start()
    assert transport.entered.wait(timeout=1)
    transport.called.clear()
    replacement = Thread(
        target=lambda: client.auth.sign_in(
            email="replacement@example.com",
            password="secret",
        )
    )
    replacement.start()
    assert transport.called.wait(timeout=1)
    transport.release.set()
    conversion.join(timeout=1)
    replacement.join(timeout=1)

    assert converted[0].email == "converted@example.com"
    assert client.current_user is not None
    assert client.current_user.email == "replacement@example.com"


def test_confirm_email_preserves_success_when_user_refresh_fails() -> None:
    transport = AuthTransport()
    transport.queue("auth_confirm_email", AuthResponse(200, {"message": "Done"}))
    transport.queue(
        "auth_get_user",
        AuthResponse(503, {"error": "Temporarily unavailable"}),
    )
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="access-token",
        refresh_token="refresh-token",
        _transport=transport,
    )

    result = client.auth.confirm_email(token="confirmation-token")

    assert result == MessageResult(message="Done")


def test_hosted_and_oauth_authorization_urls_bind_caller_state(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fixed_state(_size: int) -> str:
        return "fixed-state"

    monkeypatch.setattr("volcano_sdk.auth.token_urlsafe", fixed_state)
    transport = AuthTransport()
    transport.queue(
        "auth_oauth_authorize",
        AuthResponse(
            307,
            headers={"Location": "https://github.com/login/oauth/authorize"},
        ),
    )
    transport.queue(
        "auth_link_oauth_provider",
        AuthResponse(
            200, {"authorization_url": "https://accounts.google.com/o/oauth2"}
        ),
    )
    client = VolcanoClient(
        api_url="https://api.test.volcano.dev",
        anon_key="anon key",
        access_token="access-token",
        _transport=transport,
    )

    hosted = client.auth.get_hosted_auth_url(
        project_id="project/id",
        action="signup",
    )
    oauth = client.auth.get_oauth_authorization_url(
        provider="github",
        redirect_url="https://app.example/callback",
    )
    linked = client.auth.link_oauth_provider(
        provider="google",
        redirect_url="https://app.example/link-callback",
    )

    assert hosted == AuthorizationRequest(
        authorization_url=(
            "https://api.test.volcano.dev/projects/project%2Fid/auth/hosted"
            "?anon_key=anon+key&action=signup&state=fixed-state"
        ),
        state="fixed-state",
    )
    assert oauth == AuthorizationRequest(
        authorization_url="https://github.com/login/oauth/authorize",
        state="fixed-state",
    )
    assert linked == AuthorizationRequest(
        authorization_url="https://accounts.google.com/o/oauth2",
        state="fixed-state",
    )
    assert transport.calls == [
        (
            "auth_oauth_authorize",
            {
                "authorization": "anon key",
                "provider": "github",
                "redirect_url": "https://app.example/callback",
                "state": "fixed-state",
            },
        ),
        (
            "auth_link_oauth_provider",
            {
                "authorization": "access-token",
                "provider": "google",
                "redirect_url": "https://app.example/link-callback",
                "state": "fixed-state",
            },
        ),
    ]


def test_oauth_exchange_validates_state_before_committing() -> None:
    transport = AuthTransport()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)

    with pytest.raises(ValidationError, match="OAuth state does not match"):
        client.auth.exchange_oauth_code(
            code="oauth-code",
            redirect_url="https://app.example/callback",
            state="callback-state",
            expected_state="stored-state",
        )

    with pytest.raises(ValidationError, match="Unsupported OAuth provider"):
        client.auth.get_oauth_authorization_url(
            provider=cast("OAuthProviderName", "twitter"),
            redirect_url="https://app.example/callback",
        )

    assert transport.calls == []

    transport.queue(
        "auth_oauth_exchange",
        AuthResponse(
            200,
            _token_payload(
                access_token="oauth-access",
                refresh_token="oauth-refresh",
            ),
        ),
    )

    session = client.auth.exchange_oauth_code(
        code="oauth-code",
        redirect_url="https://app.example/callback",
        state="stored-state",
        expected_state="stored-state",
    )

    assert session is client.current_session
    assert client.current_user is not None
    assert transport.calls == [
        (
            "auth_oauth_exchange",
            {
                "authorization": "anon-key",
                "code": "oauth-code",
                "redirect_url": "https://app.example/callback",
            },
        )
    ]


def test_oauth_exchange_rejects_non_ascii_state_without_calling_transport() -> None:
    transport = AuthTransport()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)

    with pytest.raises(ValidationError, match="OAuth state does not match"):
        client.auth.exchange_oauth_code(
            code="oauth-code",
            redirect_url="https://app.example/callback",
            state="café",
            expected_state="cafe",
        )

    assert transport.calls == []


def test_identity_management_returns_public_immutable_values() -> None:
    transport = AuthTransport()
    identity_payload = {
        "id": "3cd3e058-e3ff-42a5-ae4d-650ef9b45746",
        "email": "user@example.com",
        "email_verified": True,
        "is_primary": True,
        "created_at": "2026-08-27T12:00:00Z",
    }
    method_payload = {
        "id": "7f518a4b-407b-4121-907b-d72a2c7c1ac6",
        "type": "oauth",
        "provider": "github",
        "identity_id": identity_payload["id"],
        "email": identity_payload["email"],
        "is_primary": True,
        "last_used_at": "2026-08-28T12:00:00Z",
        "created_at": "2026-08-27T12:00:00Z",
        "updated_at": "2026-08-28T12:00:00Z",
    }
    transport.queue(
        "auth_list_identities",
        AuthResponse(200, {"identities": [identity_payload]}),
    )
    transport.queue(
        "auth_list_methods",
        AuthResponse(200, {"methods": [method_payload]}),
    )
    transport.queue("auth_promote_method", AuthResponse(200, method_payload))
    transport.queue("auth_unlink_identity", AuthResponse(204))
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="access-token",
        _transport=transport,
    )

    identities = client.auth.list_identities()
    methods = client.auth.list_methods()
    identity_id = cast("str", identity_payload["id"])
    method_id = cast("str", method_payload["id"])
    promoted = client.auth.promote_method(method_id=method_id)
    client.auth.unlink_identity(identity_id=identity_id)

    assert identities == (
        AuthIdentity(
            id=identity_id,
            email="user@example.com",
            email_verified=True,
            is_primary=True,
            created_at=datetime(2026, 8, 27, 12, tzinfo=UTC),
        ),
    )
    assert methods == (promoted,)
    assert promoted == AuthMethod(
        id=method_id,
        type="oauth",
        provider="github",
        identity_id=identity_id,
        email="user@example.com",
        is_primary=True,
        last_used_at=datetime(2026, 8, 28, 12, tzinfo=UTC),
        created_at=datetime(2026, 8, 27, 12, tzinfo=UTC),
        updated_at=datetime(2026, 8, 28, 12, tzinfo=UTC),
    )


def test_provider_and_device_session_flows_return_public_values() -> None:
    transport = AuthTransport()
    transport.queue("auth_unlink_oauth_provider", AuthResponse(204))
    transport.queue(
        "auth_list_oauth_providers",
        AuthResponse(
            200,
            {
                "providers": [
                    {
                        "provider": "github",
                        "linked_at": "2026-08-27T12:00:00Z",
                        "updated_at": "2026-08-28T12:00:00Z",
                    }
                ]
            },
        ),
    )
    token_payload = {
        "provider": "github",
        "expires_in": 3600,
        "message": "Ready",
    }
    transport.queue("refresh_oauth_provider_token", AuthResponse(200, token_payload))
    transport.queue("get_oauth_provider_token", AuthResponse(200, token_payload))
    transport.queue(
        "call_oauth_provider_api",
        AuthResponse(200, {"login": "octocat", "private": False}),
    )
    transport.queue(
        "auth_get_my_sessions",
        AuthResponse(
            200,
            {
                "sessions": [
                    {
                        "id": "3cd3e058-e3ff-42a5-ae4d-650ef9b45746",
                        "user_id": "user-123",
                        "provider": "email",
                        "expires_at": "2026-08-29T12:00:00Z",
                        "is_active": True,
                        "is_current": True,
                    }
                ],
                "total": 1,
                "page": 1,
                "limit": 20,
                "total_pages": 1,
            },
        ),
        AuthResponse(
            200,
            {
                "sessions": [],
                "total": 1,
                "page": 2,
                "limit": 20,
                "total_pages": 2,
            },
        ),
    )
    transport.queue("auth_delete_my_session", AuthResponse(204))
    transport.queue("auth_delete_all_my_sessions", AuthResponse(204))
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="access-token",
        refresh_token="refresh-token",
        _transport=transport,
    )

    client.auth.unlink_oauth_provider(provider="github")
    providers = client.auth.get_linked_oauth_providers()
    refreshed = client.auth.refresh_oauth_token(provider="github")
    current = client.auth.get_oauth_provider_token(provider="github")
    provider_data = client.auth.call_oauth_api(
        provider="github",
        endpoint="/user",
    )
    sessions = client.auth.get_sessions(page=1, limit=20)
    client.auth.get_sessions(page=2, limit=20)
    client.auth.delete_all_other_sessions()
    client.auth.delete_session(session_id="3cd3e058-e3ff-42a5-ae4d-650ef9b45746")

    assert providers == (
        OAuthProvider(
            provider="github",
            linked_at=datetime(2026, 8, 27, 12, tzinfo=UTC),
            updated_at=datetime(2026, 8, 28, 12, tzinfo=UTC),
        ),
    )
    assert refreshed == OAuthTokenResult(
        provider="github",
        expires_in=3600,
        message="Ready",
    )
    assert current == refreshed
    assert provider_data == {"login": "octocat", "private": False}
    assert sessions == SessionPage(
        sessions=(
            AuthSession(
                id="3cd3e058-e3ff-42a5-ae4d-650ef9b45746",
                user_id="user-123",
                provider="email",
                expires_at=datetime(2026, 8, 29, 12, tzinfo=UTC),
                is_active=True,
                is_current=True,
            ),
        ),
        total=1,
        page=1,
        limit=20,
        total_pages=1,
    )


def test_session_listing_exposes_filters_and_cursor_navigation() -> None:
    transport = AuthTransport()
    transport.queue(
        "auth_get_my_sessions",
        AuthResponse(
            200,
            {
                "data": [],
                "total": 3,
                "limit": 1,
                "has_more": True,
                "next_cursor": "next",
                "prev_cursor": "previous",
            },
        ),
    )
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="access-token",
        _transport=transport,
    )

    page = client.auth.get_sessions(
        sort="created_at",
        status="active",
        cursor="cursor",
        offset=1,
        limit=1,
    )

    assert page == SessionPage(
        total=3,
        limit=1,
        has_more=True,
        next_cursor="next",
        prev_cursor="previous",
    )
    assert transport.calls[-1][1] == {
        "authorization": "access-token",
        "page": None,
        "limit": 1,
        "sort": "created_at",
        "status": "active",
        "cursor": "cursor",
        "offset": 1,
    }


def test_deleting_current_session_survives_automatic_refresh() -> None:
    current_session_id = "3cd3e058-e3ff-42a5-ae4d-650ef9b45746"
    transport = AuthTransport()
    transport.queue(
        "auth_get_my_sessions",
        AuthResponse(
            200,
            {
                "sessions": [
                    {
                        "id": current_session_id,
                        "user_id": "user-123",
                        "provider": "email",
                        "expires_at": "2026-08-29T12:00:00Z",
                        "is_active": True,
                        "is_current": True,
                    }
                ],
                "total": 1,
                "page": 1,
                "limit": 20,
                "total_pages": 1,
            },
        ),
    )
    transport.queue(
        "auth_delete_my_session",
        AuthResponse(401, {"error": "Access token expired"}),
        AuthResponse(204),
    )
    transport.queue(
        "auth_refresh",
        AuthResponse(
            200,
            _token_payload(
                access_token="rotated-access",
                refresh_token="rotated-refresh",
            ),
        ),
    )
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="access-token",
        refresh_token="refresh-token",
        _transport=transport,
    )

    client.auth.get_sessions()
    client.auth.delete_session(session_id=current_session_id)

    assert client.current_session is None


def test_delete_session_normalizes_current_uuid_before_matching() -> None:
    current_session_id = "3cd3e058-e3ff-42a5-ae4d-650ef9b45746"
    transport = AuthTransport()
    transport.queue(
        "auth_get_my_sessions",
        AuthResponse(
            200,
            {
                "sessions": [
                    {
                        "id": current_session_id,
                        "user_id": "user-123",
                        "provider": "email",
                        "expires_at": "2026-08-29T12:00:00Z",
                        "is_active": True,
                        "is_current": True,
                    }
                ]
            },
        ),
    )
    transport.queue("auth_delete_my_session", AuthResponse(204))
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="access-token",
        _transport=transport,
    )

    client.auth.get_sessions()
    client.auth.delete_session(session_id=f"{{{current_session_id.upper()}}}")

    assert client.current_session is None
    assert transport.calls[-1][1]["session_id"] == current_session_id


def test_provider_401_uses_structured_code_to_preserve_session() -> None:
    transport = AuthTransport()
    transport.queue(
        "call_oauth_provider_api",
        AuthResponse(
            401,
            {"error": "Provider unavailable", "code": "provider_not_linked"},
        ),
    )
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="access-token",
        refresh_token="refresh-token",
        _transport=transport,
    )

    with pytest.raises(AuthenticationError, match="Provider unavailable") as raised:
        client.auth.call_oauth_api(provider="github", endpoint="/user")

    assert raised.value.code == "provider_not_linked"
    assert client.current_session is not None
    assert client.current_session.access_token == "access-token"


def test_provider_401_without_optional_code_preserves_session() -> None:
    transport = AuthTransport()
    transport.queue(
        "call_oauth_provider_api",
        AuthResponse(401, {"error": "Provider is not linked"}),
    )
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="access-token",
        refresh_token="refresh-token",
        _transport=transport,
    )

    with pytest.raises(AuthenticationError, match="Provider is not linked"):
        client.auth.call_oauth_api(provider="github", endpoint="/user")

    assert client.current_session is not None
    assert client.current_session.access_token == "access-token"


def test_provider_401_clears_an_access_only_session() -> None:
    transport = AuthTransport()
    transport.queue(
        "call_oauth_provider_api",
        AuthResponse(401, {"error": "Session expired"}),
    )
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="access-token",
        _transport=transport,
    )

    with pytest.raises(AuthenticationError, match="Session expired"):
        client.auth.call_oauth_api(provider="github", endpoint="/user")

    assert client.current_session is None


def test_provider_api_refreshes_an_expired_session_once() -> None:
    transport = AuthTransport()
    transport.queue(
        "call_oauth_provider_api",
        AuthResponse(401, {"error": "Not authenticated"}),
        AuthResponse(200, {"login": "octocat"}),
    )
    transport.queue(
        "auth_refresh",
        AuthResponse(
            200,
            _token_payload(
                access_token="rotated-access",
                refresh_token="rotated-refresh",
            ),
        ),
    )
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="expired-access",
        refresh_token="refresh-token",
        _transport=transport,
    )

    result = client.auth.call_oauth_api(provider="github", endpoint="/user")

    assert result == {"login": "octocat"}
    assert client.current_session is not None
    assert client.current_session.access_token == "rotated-access"


def test_provider_api_clears_auth_after_a_rejected_retry() -> None:
    transport = AuthTransport()
    transport.queue(
        "call_oauth_provider_api",
        AuthResponse(401, {"error": "Expired"}),
        AuthResponse(401, {"error": "Session revoked"}),
    )
    transport.queue(
        "auth_refresh",
        AuthResponse(
            200,
            _token_payload(
                access_token="rotated-access",
                refresh_token="rotated-refresh",
            ),
        ),
    )
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="expired-access",
        refresh_token="refresh-token",
        _transport=transport,
    )

    with pytest.raises(AuthenticationError, match="Session revoked"):
        client.auth.call_oauth_api(provider="github", endpoint="/user")

    assert client.current_session is None


def test_delete_session_rejects_a_malformed_identifier() -> None:
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="access-token",
        refresh_token="refresh-token",
        _transport=AuthTransport(),
    )

    with pytest.raises(ValidationError, match="session_id must be a valid UUID"):
        client.auth.delete_session(session_id="not-a-uuid")


def test_direct_current_session_deletion_clears_restored_auth() -> None:
    current_id = "3cd3e058-e3ff-42a5-ae4d-650ef9b45746"
    transport = AuthTransport()
    transport.queue("auth_delete_my_session", AuthResponse(204))
    client = VolcanoClient(
        anon_key="anon-key",
        access_token=_access_token_for_session(current_id),
        refresh_token="refresh-token",
        _transport=transport,
    )
    client._set_user(User(id="user-123", email="user@example.com"))

    client.auth.delete_session(session_id=current_id)

    assert client.current_session is None
    assert client.current_user is None


def test_replacing_auth_invalidates_cached_current_device_ids() -> None:
    previous_id = "3cd3e058-e3ff-42a5-ae4d-650ef9b45746"
    transport = AuthTransport()
    transport.queue(
        "auth_get_my_sessions",
        AuthResponse(
            200,
            {
                "sessions": [
                    {
                        "id": previous_id,
                        "user_id": "user-123",
                        "provider": "email",
                        "expires_at": "2026-08-29T12:00:00Z",
                        "is_active": True,
                        "is_current": True,
                    }
                ]
            },
        ),
    )
    transport.queue(
        "auth_signin",
        AuthResponse(
            200,
            _token_payload(
                access_token="replacement-access",
                refresh_token="replacement-refresh",
            ),
        ),
    )
    transport.queue("auth_delete_my_session", AuthResponse(204))
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="previous-access",
        refresh_token="previous-refresh",
        _transport=transport,
    )

    client.auth.get_sessions()
    replacement = client.auth.sign_in(email="user@example.com", password="secret")
    client.auth.delete_session(session_id=previous_id)

    assert client.current_session is replacement


def test_session_listing_serializes_replacement_auth() -> None:
    previous_id = "3cd3e058-e3ff-42a5-ae4d-650ef9b45746"
    transport = BlockingAuthTransport("auth_get_my_sessions")
    transport.queue(
        "auth_get_my_sessions",
        AuthResponse(
            200,
            {
                "sessions": [
                    {
                        "id": previous_id,
                        "user_id": "user-123",
                        "provider": "email",
                        "expires_at": "2026-08-29T12:00:00Z",
                        "is_active": True,
                        "is_current": True,
                    }
                ]
            },
        ),
    )
    transport.queue(
        "auth_signin",
        AuthResponse(
            200,
            _token_payload(
                access_token="replacement-access",
                refresh_token="replacement-refresh",
            ),
        ),
    )
    transport.queue("auth_delete_my_session", AuthResponse(204))
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="previous-access",
        refresh_token="previous-refresh",
        _transport=transport,
    )
    listing = Thread(target=client.auth.get_sessions)
    listing.start()
    assert transport.entered.wait(timeout=1)
    transport.called.clear()
    replacement = Thread(
        target=lambda: client.auth.sign_in(
            email="user@example.com",
            password="secret",
        )
    )
    replacement.start()
    assert transport.called.wait(timeout=1)
    transport.release.set()
    listing.join(timeout=1)
    replacement.join(timeout=1)
    client.auth.delete_session(session_id=previous_id)

    assert client.current_session is not None
    assert client.current_session.access_token == "replacement-access"


def test_refresh_preserves_cached_current_device_identity() -> None:
    current_id = "3cd3e058-e3ff-42a5-ae4d-650ef9b45746"
    transport = AuthTransport()
    transport.queue(
        "auth_get_my_sessions",
        AuthResponse(
            200,
            {
                "sessions": [
                    {
                        "id": current_id,
                        "user_id": "user-123",
                        "provider": "email",
                        "expires_at": "2026-08-29T12:00:00Z",
                        "is_active": True,
                        "is_current": True,
                    }
                ]
            },
        ),
    )
    transport.queue(
        "auth_refresh",
        AuthResponse(
            200,
            _token_payload(
                access_token="rotated-access",
                refresh_token="rotated-refresh",
            ),
        ),
    )
    transport.queue("auth_delete_my_session", AuthResponse(204))
    client = VolcanoClient(
        anon_key="anon-key",
        access_token="access-token",
        refresh_token="refresh-token",
        _transport=transport,
    )

    client.auth.get_sessions()
    client.auth.refresh_session()
    client.auth.delete_session(session_id=current_id)

    assert client.current_session is None
