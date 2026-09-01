from __future__ import annotations

from dataclasses import FrozenInstanceError, dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any

import pytest

from volcano_sdk import (
    AuthenticationError,
    RateLimitedError,
    ServerError,
    Session,
    SessionChangedError,
    VolcanoClient,
)
from volcano_sdk._generated.models.auth_convert_anonymous_response_200 import (
    AuthConvertAnonymousResponse200,
)
from volcano_sdk._generated.models.auth_get_user_response_200 import (
    AuthGetUserResponse200,
)
from volcano_sdk._generated.models.auth_update_user_response_200 import (
    AuthUpdateUserResponse200,
)

if TYPE_CHECKING:
    from collections.abc import Callable


@dataclass(frozen=True)
class Response:
    status_code: int
    payload: Any = None
    content: bytes = b""
    headers: dict[str, str] | None = None


def _user_profile(*, email: str = "user@example.com") -> AuthGetUserResponse200:
    return AuthGetUserResponse200.from_dict(
        {
            "user": {
                "id": "00000000-0000-4000-8000-000000000010",
                "email": email,
                "status": "active",
                "project_id": "00000000-0000-4000-8000-000000000020",
                "email_confirmed": True,
                "user_metadata": {
                    "display_name": "Ada",
                    "roles": ["admin"],
                },
                "app_metadata": {"provider": "email"},
                "avatar_url": "https://example.com/avatar.png",
                "banned_until": None,
                "last_sign_in_at": "2026-08-31T12:00:00Z",
                "created_at": "2026-08-30T12:00:00+00:00",
                "updated_at": "2026-08-31T17:30:00+05:30",
            }
        }
    )


def _updated_user_profile() -> AuthUpdateUserResponse200:
    return AuthUpdateUserResponse200.from_dict(_user_profile().to_dict())


def _converted_user_profile() -> AuthConvertAnonymousResponse200:
    payload = _user_profile().to_dict()
    payload["user"]["email"] = "converted@example.com"
    payload["user"]["email_confirmed"] = False
    return AuthConvertAnonymousResponse200.from_dict(payload)


class StateTransport:
    def __init__(self) -> None:
        self.next_access_token = "access-1"
        self.signup_response = Response(
            201,
            {
                "confirmation_required": True,
                "message": "Check your email to confirm your account",
            },
        )
        self.signup_calls: list[dict[str, Any]] = []
        self.anonymous_signin_response = Response(
            201,
            {
                "access_token": "anonymous-access",
                "refresh_token": "anonymous-refresh",
                "user": {"id": "00000000-0000-4000-8000-000000000099"},
            },
        )
        self.anonymous_signin_calls: list[dict[str, Any]] = []
        self.on_anonymous_signin: Callable[[], None] | None = None
        self.anonymous_conversion_response = Response(200, _converted_user_profile())
        self.anonymous_conversion_calls: list[dict[str, Any]] = []
        self.on_anonymous_conversion: Callable[[], None] | None = None
        self.email_change_response = Response(
            200,
            {"message": "Confirmation email sent", "new_email": "new@example.com"},
        )
        self.email_change_calls: list[dict[str, Any]] = []
        self.on_email_change: Callable[[], None] | None = None
        self.forgot_password_response = Response(
            200,
            {"message": "If the email exists, a password reset link has been sent."},
        )
        self.forgot_password_calls: list[dict[str, Any]] = []
        self.reset_password_response = Response(
            200,
            {"message": "Password reset successful. Please sign in again."},
        )
        self.reset_password_calls: list[dict[str, Any]] = []
        self.confirm_email_response = Response(
            200,
            {"message": "Email confirmed successfully"},
        )
        self.confirm_email_calls: list[dict[str, Any]] = []
        self.resend_confirmation_response = Response(
            200,
            {"message": "If eligible, a confirmation email has been sent."},
        )
        self.resend_confirmation_calls: list[dict[str, Any]] = []
        self.user_response = Response(
            200,
            _user_profile(),
        )
        self.on_get_user: Callable[[], None] | None = None
        self.update_user_response = Response(200, _updated_user_profile())
        self.update_user_calls: list[dict[str, Any]] = []
        self.on_update_user: Callable[[], None] | None = None
        self.refresh_response = Response(
            200,
            {
                "access_token": "access-2",
                "refresh_token": "refresh-2",
                "user": {"id": "00000000-0000-4000-8000-000000000010"},
            },
        )
        self.on_refresh: Callable[[], None] | None = None
        self.logout_response = Response(204)
        self.on_logout: Callable[[], None] | None = None
        self.query_calls: list[dict[str, Any]] = []
        self.authorizations: list[tuple[str, str]] = []

    def auth_signin(self, **kwargs: Any) -> Response:
        self.authorizations.append(("auth", kwargs["authorization"]))
        return Response(
            200,
            {
                "access_token": self.next_access_token,
                "refresh_token": f"refresh-{self.next_access_token}",
                "user": {"id": "00000000-0000-4000-8000-000000000010"},
            },
        )

    def auth_signup(self, **kwargs: Any) -> Response:
        self.authorizations.append(("signup", kwargs["authorization"]))
        self.signup_calls.append(kwargs)
        return self.signup_response

    def auth_signup_anonymous(self, **kwargs: Any) -> Response:
        self.authorizations.append(("anonymous_signin", kwargs["authorization"]))
        self.anonymous_signin_calls.append(kwargs)
        if self.on_anonymous_signin is not None:
            self.on_anonymous_signin()
        return self.anonymous_signin_response

    def auth_convert_anonymous(self, **kwargs: Any) -> Response:
        self.authorizations.append(("anonymous_conversion", kwargs["authorization"]))
        self.anonymous_conversion_calls.append(kwargs)
        if self.on_anonymous_conversion is not None:
            self.on_anonymous_conversion()
        return self.anonymous_conversion_response

    def auth_request_email_change(self, **kwargs: Any) -> Response:
        self.authorizations.append(("email_change", kwargs["authorization"]))
        self.email_change_calls.append(kwargs)
        if self.on_email_change is not None:
            self.on_email_change()
        return self.email_change_response

    def auth_forgot_password(self, **kwargs: Any) -> Response:
        self.authorizations.append(("forgot_password", kwargs["authorization"]))
        self.forgot_password_calls.append(kwargs)
        return self.forgot_password_response

    def auth_reset_password(self, **kwargs: Any) -> Response:
        self.authorizations.append(("reset_password", kwargs["authorization"]))
        self.reset_password_calls.append(kwargs)
        return self.reset_password_response

    def auth_confirm_email(self, **kwargs: Any) -> Response:
        self.authorizations.append(("confirm_email", kwargs["authorization"]))
        self.confirm_email_calls.append(kwargs)
        return self.confirm_email_response

    def auth_resend_confirmation(self, **kwargs: Any) -> Response:
        self.authorizations.append(("resend_confirmation", kwargs["authorization"]))
        self.resend_confirmation_calls.append(kwargs)
        return self.resend_confirmation_response

    def auth_get_user(self, **kwargs: Any) -> Response:
        self.authorizations.append(("get_user", kwargs["authorization"]))
        if self.on_get_user is not None:
            self.on_get_user()
        return self.user_response

    def auth_update_user(self, **kwargs: Any) -> Response:
        self.authorizations.append(("update_user", kwargs["authorization"]))
        self.update_user_calls.append(kwargs)
        if self.on_update_user is not None:
            self.on_update_user()
        return self.update_user_response

    def auth_refresh(self, **kwargs: Any) -> Response:
        self.authorizations.append(("refresh", kwargs["authorization"]))
        if self.on_refresh is not None:
            self.on_refresh()
        return self.refresh_response

    def auth_logout(self, **kwargs: Any) -> Response:
        self.authorizations.append(("logout", kwargs["authorization"]))
        if self.on_logout is not None:
            self.on_logout()
        return self.logout_response

    def query_database_select(self, **kwargs: Any) -> Response:
        self.authorizations.append(("query", kwargs["authorization"]))
        self.query_calls.append(kwargs["body"])
        return Response(200, {"data": [kwargs["body"]], "count": 1})

    def upload_storage_object(self, **kwargs: Any) -> Response:
        self.authorizations.append(("upload", kwargs["authorization"]))
        return Response(201, {"name": kwargs["path"]})

    def download_storage_object(self, **kwargs: Any) -> Response:
        self.authorizations.append(("download", kwargs["authorization"]))
        return Response(200, content=b"bytes")

    def acquire_project_lock(self, **kwargs: Any) -> Response:
        self.authorizations.append(("acquire", kwargs["authorization"]))
        return Response(201, {"expires_at": None, "fencing_token": 1})

    def release_project_lock(self, **kwargs: Any) -> Response:
        self.authorizations.append(("release", kwargs["authorization"]))
        return Response(204)


def test_query_builder_chains_are_immutable() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    base = client.database("main").from_("items")
    selected = base.select("*")
    first = selected.eq("slug", "a")
    second = selected.eq("slug", "b")

    first.execute()
    second.execute()

    assert transport.query_calls == [
        {
            "table": "items",
            "filters": [{"column": "slug", "operator": "eq", "value": "a"}],
        },
        {
            "table": "items",
            "filters": [{"column": "slug", "operator": "eq", "value": "b"}],
        },
    ]


def test_each_request_reads_the_current_credentials() -> None:
    transport = StateTransport()
    client = VolcanoClient(
        anon_key="anon-1",
        service_key="service-1",
        _transport=transport,
    )
    client.auth.sign_in(email="user@example.com", password="secret")
    query = client.database("main").from_("items").select("*")
    bucket = client.storage.from_("assets")

    transport.next_access_token = "access-2"
    client._anon_key = "anon-2"
    client.auth.sign_in(email="user@example.com", password="secret")
    query.execute()
    bucket.upload("a.txt", b"bytes")
    bucket.download("a.txt")
    lease = client.locks.acquire("build", ttl=30)
    client._service_key = "service-2"
    client.locks.release("build", lease)

    assert transport.authorizations == [
        ("auth", "anon-1"),
        ("auth", "anon-2"),
        ("query", "access-2"),
        ("upload", "access-2"),
        ("download", "access-2"),
        ("acquire", "service-1"),
        ("release", "service-2"),
    ]


def test_auth_facade_reads_an_empty_session_without_transport() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    assert client.auth.get_session() is None
    assert transport.authorizations == []


def test_sign_up_returns_immutable_acknowledgement_without_session_change() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")

    result = client.auth.sign_up(
        email="new@example.com",
        password="secret",
        metadata={"display_name": "New User"},
    )

    assert result.confirmation_required is True
    assert result.message == "Check your email to confirm your account"
    assert client.auth.get_session() is established
    assert transport.signup_calls == [
        {
            "authorization": "anon",
            "email": "new@example.com",
            "password": "secret",
            "metadata": {"display_name": "New User"},
        }
    ]
    mutable_result: Any = result
    with pytest.raises(FrozenInstanceError):
        mutable_result.message = "changed"


def test_sign_up_uses_empty_metadata_without_creating_a_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    client.auth.sign_up(email="new@example.com", password="secret")

    assert client.auth.get_session() is None
    assert transport.signup_calls[0]["metadata"] == {}


def test_sign_up_raises_typed_errors_without_changing_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")
    transport.signup_response = Response(403, {"error": "Signups are disabled"})

    with pytest.raises(AuthenticationError, match="Signups are disabled"):
        client.auth.sign_up(email="new@example.com", password="secret")

    assert client.auth.get_session() is established


def test_sign_in_anonymously_stores_the_returned_session_and_metadata() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    session = client.auth.sign_in_anonymously(metadata={"device": "mobile"})

    assert session == Session(
        access_token="anonymous-access",
        refresh_token="anonymous-refresh",
        user_id="00000000-0000-4000-8000-000000000099",
    )
    assert client.auth.get_session() is session
    assert transport.anonymous_signin_calls == [
        {"authorization": "anon", "metadata": {"device": "mobile"}}
    ]


def test_sign_in_anonymously_does_not_replace_a_newer_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    replacement = Session(
        access_token="replacement-access",
        refresh_token="replacement-refresh",
        user_id="00000000-0000-4000-8000-000000000010",
    )

    def replace_session() -> None:
        client.auth.set_session(replacement)

    transport.on_anonymous_signin = replace_session

    with pytest.raises(SessionChangedError):
        client.auth.sign_in_anonymously()

    assert client.auth.get_session() == replacement


def test_sign_in_anonymously_preserves_session_when_disabled() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")
    transport.anonymous_signin_response = Response(
        403,
        {"error": "Anonymous sign-ins are disabled"},
    )

    with pytest.raises(AuthenticationError, match="Anonymous sign-ins are disabled"):
        client.auth.sign_in_anonymously()

    assert client.auth.get_session() is established


def test_convert_anonymous_returns_the_user_without_replacing_the_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in_anonymously()

    user = client.auth.convert_anonymous(
        email="converted@example.com",
        password="secret",
        metadata={"display_name": "Ada"},
    )

    assert user.email == "converted@example.com"
    assert user.email_confirmed is False
    assert client.auth.get_session() is established
    assert transport.anonymous_conversion_calls == [
        {
            "authorization": "anonymous-access",
            "email": "converted@example.com",
            "password": "secret",
            "metadata": {"display_name": "Ada"},
        }
    ]


def test_convert_anonymous_requires_a_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(AuthenticationError, match="No active session"):
        client.auth.convert_anonymous(email="converted@example.com", password="secret")

    assert transport.anonymous_conversion_calls == []


def test_convert_anonymous_does_not_return_a_stale_response() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in_anonymously()
    replacement = Session(
        access_token="replacement-access",
        refresh_token="replacement-refresh",
        user_id="replacement-user",
    )

    def replace_session() -> None:
        client.auth.set_session(replacement)

    transport.on_anonymous_conversion = replace_session

    with pytest.raises(SessionChangedError):
        client.auth.convert_anonymous(email="converted@example.com", password="secret")

    assert client.auth.get_session() == replacement


def test_request_email_change_returns_acknowledgement_without_session_change() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")

    result = client.auth.request_email_change(new_email="new@example.com")

    assert result.message == "Confirmation email sent"
    assert result.new_email == "new@example.com"
    assert client.auth.get_session() is established
    assert transport.email_change_calls == [
        {"authorization": "access-1", "new_email": "new@example.com"}
    ]


def test_request_email_change_accepts_optional_response_fields() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    transport.email_change_response = Response(200, {})

    result = client.auth.request_email_change(new_email="new@example.com")

    assert result.message is None
    assert result.new_email is None


def test_request_email_change_requires_a_current_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(AuthenticationError, match="No active session"):
        client.auth.request_email_change(new_email="new@example.com")

    assert transport.email_change_calls == []


def test_request_email_change_rejects_a_stale_response() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    replacement = Session(
        access_token="replacement-access",
        refresh_token="replacement-refresh",
        user_id="replacement-user",
    )

    def replace_session() -> None:
        client.auth.set_session(replacement)

    transport.on_email_change = replace_session

    with pytest.raises(SessionChangedError):
        client.auth.request_email_change(new_email="new@example.com")

    assert client.auth.get_session() == replacement


def test_get_user_returns_an_immutable_server_validated_profile() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")

    user = client.auth.get_user()

    assert user.id == "00000000-0000-4000-8000-000000000010"
    assert user.email == "user@example.com"
    assert user.status == "active"
    assert user.project_id == "00000000-0000-4000-8000-000000000020"
    assert user.email_confirmed is True
    assert user.user_metadata == {"display_name": "Ada", "roles": ("admin",)}
    assert user.app_metadata == {"provider": "email"}
    assert user.avatar_url == "https://example.com/avatar.png"
    assert user.banned_until is None
    assert user.last_sign_in_at == datetime.fromisoformat("2026-08-31T12:00:00Z")
    assert user.created_at == datetime.fromisoformat("2026-08-30T12:00:00+00:00")
    assert user.updated_at == datetime.fromisoformat("2026-08-31T17:30:00+05:30")
    assert transport.authorizations[-1] == ("get_user", "access-1")
    assert client.auth.get_session() is established
    mutable_user: Any = user
    mutable_metadata: Any = user.user_metadata
    mutable_app_metadata: Any = user.app_metadata
    with pytest.raises(FrozenInstanceError):
        mutable_user.email = "changed@example.com"
    with pytest.raises(TypeError):
        mutable_metadata["display_name"] = "Changed"
    with pytest.raises(TypeError):
        mutable_app_metadata["provider"] = "oauth"


def test_reset_password_for_email_returns_the_generic_acknowledgement() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")

    client.auth.reset_password_for_email(email="user@example.com")

    assert transport.forgot_password_calls == [
        {"authorization": "anon", "email": "user@example.com"}
    ]
    assert client.auth.get_session() is established


def test_reset_password_for_email_raises_typed_errors_without_session_change() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")
    transport.forgot_password_response = Response(
        403,
        {"error": "Password reset disabled"},
    )

    with pytest.raises(AuthenticationError, match="Password reset disabled"):
        client.auth.reset_password_for_email(email="user@example.com")

    assert client.auth.get_session() is established


def test_reset_password_for_email_accepts_a_message_less_acknowledgement() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    transport.forgot_password_response = Response(200, {})

    client.auth.reset_password_for_email(email="user@example.com")


def test_reset_password_uses_the_recovery_token_without_session_change() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="other@example.com", password="secret")

    client.auth.reset_password(token="recovery-token", new_password="new-secret")

    assert transport.reset_password_calls == [
        {
            "authorization": "anon",
            "token": "recovery-token",
            "new_password": "new-secret",
        }
    ]
    assert client.auth.get_session() is established


def test_reset_password_raises_a_typed_error_without_session_change() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="other@example.com", password="secret")
    transport.reset_password_response = Response(401)

    with pytest.raises(AuthenticationError):
        client.auth.reset_password(token="expired-token", new_password="new-secret")

    assert client.auth.get_session() is established


def test_confirm_email_uses_the_token_without_session_change() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="other@example.com", password="secret")

    client.auth.confirm_email(token="confirmation-token")

    assert transport.confirm_email_calls == [
        {"authorization": "anon", "token": "confirmation-token"}
    ]
    assert client.auth.get_session() is established


def test_confirm_email_raises_a_typed_error_without_session_change() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="other@example.com", password="secret")
    transport.confirm_email_response = Response(401)

    with pytest.raises(AuthenticationError):
        client.auth.confirm_email(token="expired-token")

    assert client.auth.get_session() is established


def test_resend_confirmation_is_enumeration_safe_without_session_change() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="other@example.com", password="secret")

    client.auth.resend_confirmation(email="user@example.com")

    assert transport.resend_confirmation_calls == [
        {"authorization": "anon", "email": "user@example.com"}
    ]
    assert client.auth.get_session() is established


def test_resend_confirmation_preserves_rate_limit_metadata() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="other@example.com", password="secret")
    transport.resend_confirmation_response = Response(
        429,
        {"error": "Too many requests"},
        headers={"Retry-After": "17"},
    )

    with pytest.raises(RateLimitedError) as caught:
        client.auth.resend_confirmation(email="user@example.com")

    assert caught.value.retry_after == 17
    assert client.auth.get_session() is established


def test_get_user_accepts_a_server_profile_without_an_email() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    transport.user_response = Response(200, _user_profile(email=""))

    user = client.auth.get_user()

    assert user.email == ""


def test_user_with_metadata_has_a_stable_hash() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    user = client.auth.get_user()

    assert {user} == {user}


def test_get_user_without_a_session_fails_before_transport() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(AuthenticationError, match="No active session"):
        client.auth.get_user()

    assert transport.authorizations == []


def test_get_user_authentication_failure_preserves_the_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")
    transport.user_response = Response(401, {"error": "expired"})

    with pytest.raises(AuthenticationError, match="expired"):
        client.auth.get_user()

    assert client.auth.get_session() is established


def test_get_user_rejects_a_profile_loaded_for_a_replaced_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    replacement = Session(
        access_token="replacement-access",
        refresh_token="replacement-refresh",
        user_id="replacement-user",
    )

    def replace_session() -> None:
        client.auth.set_session(replacement)

    transport.on_get_user = replace_session

    with pytest.raises(SessionChangedError):
        client.auth.get_user()

    assert client.auth.get_session() == replacement


def test_update_user_returns_the_updated_profile_without_replacing_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")

    user = client.auth.update_user(
        password="new-secret",
        metadata={"display_name": "Grace", "avatar": None},
    )

    assert user.id == established.user_id
    assert user.user_metadata == {"display_name": "Ada", "roles": ("admin",)}
    assert transport.update_user_calls == [
        {
            "authorization": "access-1",
            "password": "new-secret",
            "metadata": {"display_name": "Grace", "avatar": None},
        }
    ]
    assert client.auth.get_session() is established


def test_update_user_without_a_session_fails_before_transport() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(AuthenticationError, match="No active session"):
        client.auth.update_user(metadata={"display_name": "Grace"})

    assert transport.update_user_calls == []


def test_update_user_authentication_failure_preserves_the_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")
    transport.update_user_response = Response(401, {"error": "expired"})

    with pytest.raises(AuthenticationError, match="expired"):
        client.auth.update_user(password="new-secret")

    assert client.auth.get_session() is established


def test_update_user_rejects_a_profile_for_a_replaced_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    replacement = Session(
        access_token="replacement-access",
        refresh_token="replacement-refresh",
        user_id="replacement-user",
    )

    def replace_session() -> None:
        client.auth.set_session(replacement)

    transport.on_update_user = replace_session

    with pytest.raises(SessionChangedError):
        client.auth.update_user(metadata={"display_name": "Grace"})

    assert client.auth.get_session() == replacement


def test_auth_facade_reads_established_immutable_session_without_transport() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")
    calls_after_sign_in = list(transport.authorizations)

    current = client.auth.get_session()

    assert current is established
    assert current == Session(
        access_token="access-1",
        refresh_token="refresh-access-1",
        user_id="00000000-0000-4000-8000-000000000010",
    )
    assert transport.authorizations == calls_after_sign_in


def test_auth_facade_adopts_an_owned_session_without_transport() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    supplied = Session(
        access_token="adopted-access",
        refresh_token="adopted-refresh",
        user_id="adopted-user",
    )

    adopted = client.auth.set_session(supplied)

    assert adopted == supplied
    assert adopted is not supplied
    assert client.auth.get_session() is adopted
    assert transport.authorizations == []


def test_auth_facade_adoption_replaces_the_current_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    replacement = Session(
        access_token="replacement-access",
        refresh_token="replacement-refresh",
        user_id="replacement-user",
    )
    calls_after_sign_in = list(transport.authorizations)

    adopted = client.auth.set_session(replacement)

    assert client.auth.get_session() is adopted
    assert adopted == replacement
    assert transport.authorizations == calls_after_sign_in


@pytest.mark.parametrize(
    "invalid",
    [
        object(),
        Session(access_token=" ", refresh_token="refresh", user_id="user"),
        Session(access_token="access", refresh_token="\t", user_id="user"),
        Session(access_token="access", refresh_token="refresh", user_id="\n"),
    ],
)
def test_auth_facade_rejects_incomplete_adoption_without_mutation(invalid: Any) -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    previous = client.auth.sign_in(email="user@example.com", password="secret")
    calls_after_sign_in = list(transport.authorizations)

    with pytest.raises(ValueError, match="complete Session"):
        client.auth.set_session(invalid)

    assert client.auth.get_session() is previous
    assert transport.authorizations == calls_after_sign_in


def test_refresh_replaces_the_captured_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")

    refreshed = client.auth.refresh_session()

    assert refreshed == Session("access-2", "refresh-2", established.user_id)
    assert client.auth.get_session() is refreshed


def test_refresh_without_a_session_fails_without_transport() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(AuthenticationError, match="No active session"):
        client.auth.refresh_session()

    assert transport.authorizations == []


def test_refresh_authentication_failure_clears_only_the_captured_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")
    transport.refresh_response = Response(401, {"error": "expired"})

    with pytest.raises(AuthenticationError, match="expired"):
        client.auth.refresh_session()

    assert client.auth.get_session() is None
    assert established.refresh_token == "refresh-access-1"


def test_refresh_server_failure_preserves_the_captured_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")
    transport.refresh_response = Response(503, {"error": "unavailable"})

    with pytest.raises(ServerError, match="unavailable"):
        client.auth.refresh_session()

    assert client.auth.get_session() is established


def test_refresh_does_not_replace_a_session_established_during_the_request() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    replacement = Session(
        "replacement-access",
        "replacement-refresh",
        "replacement-user",
    )

    def replace_session() -> None:
        client.auth.set_session(replacement)

    transport.on_refresh = replace_session

    with pytest.raises(SessionChangedError):
        client.auth.refresh_session()

    assert client.auth.get_session() == replacement


def test_sign_out_revokes_and_clears_the_current_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")

    client.auth.sign_out()

    assert client.auth.get_session() is None
    assert transport.authorizations[-1] == ("logout", "anon")


def test_sign_out_without_a_session_succeeds_without_transport() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    client.auth.sign_out()
    assert transport.authorizations == []


def test_sign_out_server_failure_clears_then_raises() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    transport.logout_response = Response(503, {"error": "Logout unavailable"})

    with pytest.raises(ServerError, match="Logout unavailable"):
        client.auth.sign_out()

    assert client.auth.get_session() is None


def test_sign_out_does_not_clear_a_replacement_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    replacement = Session(
        "replacement-access", "replacement-refresh", "replacement-user"
    )

    def replace_session() -> None:
        client.auth.set_session(replacement)

    transport.on_logout = replace_session
    with pytest.raises(SessionChangedError):
        client.auth.sign_out()
    assert client.auth.get_session() == replacement
