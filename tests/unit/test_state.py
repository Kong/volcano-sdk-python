from __future__ import annotations

import json
from base64 import urlsafe_b64encode
from dataclasses import FrozenInstanceError, dataclass
from datetime import datetime
from threading import Event, Thread
from typing import TYPE_CHECKING, Any, cast

import httpx
import pytest

from volcano_sdk import (
    AuthenticationError,
    AuthSession,
    AuthSubscription,
    LinkedOAuthProvider,
    OAuthProviderTokenStatus,
    RateLimitedError,
    ServerError,
    Session,
    SessionChangedError,
    SessionPage,
    TransportError,
    VolcanoClient,
    VolcanoError,
)
from volcano_sdk._generated.models.auth_confirm_email_change_response_200 import (
    AuthConfirmEmailChangeResponse200,
)
from volcano_sdk._generated.models.auth_convert_anonymous_response_200 import (
    AuthConvertAnonymousResponse200,
)
from volcano_sdk._generated.models.auth_get_my_sessions_response_200 import (
    AuthGetMySessionsResponse200,
)
from volcano_sdk._generated.models.auth_get_user_response_200 import (
    AuthGetUserResponse200,
)
from volcano_sdk._generated.models.auth_link_o_auth_provider_response_200 import (
    AuthLinkOAuthProviderResponse200,
)
from volcano_sdk._generated.models.auth_list_o_auth_providers_response_200 import (
    AuthListOAuthProvidersResponse200,
)
from volcano_sdk._generated.models.auth_update_user_response_200 import (
    AuthUpdateUserResponse200,
)
from volcano_sdk._generated.models.call_o_auth_provider_api_response_200 import (
    CallOAuthProviderAPIResponse200,
)
from volcano_sdk._generated.models.get_o_auth_provider_token_response_200 import (
    GetOAuthProviderTokenResponse200,
)
from volcano_sdk._generated.models.refresh_o_auth_provider_token_response_200 import (
    RefreshOAuthProviderTokenResponse200,
)

if TYPE_CHECKING:
    from collections.abc import Callable

_CONNECTION_LOST = "connection lost"
_SUBSCRIBER_FAILED = "subscriber failed"


class _SubscriberAbortError(BaseException):
    pass


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


def _confirmed_email_change_profile() -> AuthConfirmEmailChangeResponse200:
    return AuthConfirmEmailChangeResponse200.from_dict(
        _user_profile(email="new@example.com").to_dict()
    )


def _access_token_with_session_id(session_id: str) -> str:
    payload = urlsafe_b64encode(json.dumps({"session_id": session_id}).encode()).rstrip(
        b"="
    )
    return f"header.{payload.decode()}.signature"


def _sessions_page() -> AuthGetMySessionsResponse200:
    return AuthGetMySessionsResponse200.from_dict(
        {
            "sessions": [
                {
                    "id": "00000000-0000-4000-8000-000000000099",
                    "user_id": "00000000-0000-4000-8000-000000000010",
                    "provider": "email",
                    "user_agent": "Volcano Test",
                    "ip_address": "192.0.2.10",
                    "last_ip_address": "192.0.2.11",
                    "expires_at": "2026-09-02T12:00:00Z",
                    "last_activity_at": "2026-09-01T12:00:00Z",
                    "session_started_at": "2026-08-31T12:00:00Z",
                    "is_active": True,
                    "is_current": True,
                    "created_at": "2026-08-31T12:00:00Z",
                    "updated_at": "2026-09-01T12:00:00Z",
                }
            ],
            "total": 21,
            "page": 2,
            "limit": 10,
            "total_pages": 3,
        }
    )


def _linked_oauth_providers() -> AuthListOAuthProvidersResponse200:
    return AuthListOAuthProvidersResponse200.from_dict(
        {
            "providers": [
                {
                    "provider": "google",
                    "linked_at": "2026-08-30T12:00:00Z",
                    "updated_at": "2026-09-01T12:00:00Z",
                }
            ]
        }
    )


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
        self.cancel_email_change_response = Response(200, {})
        self.cancel_email_change_calls: list[dict[str, Any]] = []
        self.on_cancel_email_change: Callable[[], None] | None = None
        self.confirm_email_change_response = Response(
            200,
            _confirmed_email_change_profile(),
        )
        self.confirm_email_change_calls: list[dict[str, Any]] = []
        self.on_confirm_email_change: Callable[[], None] | None = None
        self.delete_other_sessions_response = Response(204)
        self.delete_other_sessions_calls: list[dict[str, Any]] = []
        self.on_delete_other_sessions: Callable[[], None] | None = None
        self.delete_session_response = Response(204)
        self.delete_session_calls: list[dict[str, Any]] = []
        self.on_delete_session: Callable[[], None] | None = None
        self.list_sessions_response = Response(200, _sessions_page())
        self.list_sessions_calls: list[dict[str, Any]] = []
        self.on_list_sessions: Callable[[], None] | None = None
        self._configure_oauth()
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

    def _configure_oauth(self) -> None:
        self.oauth_authorization_url = "https://api.example/auth/oauth/github/authorize"
        self.oauth_authorization_url_calls: list[dict[str, Any]] = []
        self.oauth_exchange_response = Response(
            200,
            {
                "access_token": "oauth-access",
                "refresh_token": "oauth-refresh",
                "user": {"id": "00000000-0000-4000-8000-000000000010"},
            },
        )
        self.oauth_exchange_calls: list[dict[str, Any]] = []
        self.on_oauth_exchange: Callable[[], None] | None = None
        self.list_oauth_providers_response = Response(200, _linked_oauth_providers())
        self.list_oauth_providers_calls: list[dict[str, Any]] = []
        self.on_list_oauth_providers: Callable[[], None] | None = None
        self.link_oauth_provider_response = Response(
            200,
            AuthLinkOAuthProviderResponse200.from_dict(
                {"authorization_url": "https://accounts.example/link"}
            ),
        )
        self.link_oauth_provider_calls: list[dict[str, Any]] = []
        self.on_link_oauth_provider: Callable[[], None] | None = None
        self.unlink_oauth_provider_response = Response(204)
        self.unlink_oauth_provider_calls: list[dict[str, Any]] = []
        self.on_unlink_oauth_provider: Callable[[], None] | None = None
        self.oauth_provider_token_status_response = Response(
            200,
            GetOAuthProviderTokenResponse200.from_dict(
                {
                    "message": "Provider token is valid",
                    "provider": "google",
                    "expires_in": 3600,
                }
            ),
        )
        self.oauth_provider_token_status_calls: list[dict[str, Any]] = []
        self.on_oauth_provider_token_status: Callable[[], None] | None = None
        self.refresh_oauth_provider_token_response = Response(
            200,
            RefreshOAuthProviderTokenResponse200.from_dict(
                {
                    "message": "Provider token refreshed successfully",
                    "provider": "google",
                    "expires_in": 3600,
                }
            ),
        )
        self.refresh_oauth_provider_token_calls: list[dict[str, Any]] = []
        self.on_refresh_oauth_provider_token: Callable[[], None] | None = None
        self.call_oauth_api_response = Response(
            200,
            CallOAuthProviderAPIResponse200.from_dict(
                {
                    "provider": "github",
                    "endpoint": "/user/repos",
                    "status_code": 200,
                    "data": [{"name": "volcano"}],
                }
            ),
        )
        self.call_oauth_api_calls: list[dict[str, Any]] = []
        self.on_call_oauth_api: Callable[[], None] | None = None

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

    def auth_cancel_email_change(self, **kwargs: Any) -> Response:
        self.authorizations.append(("cancel_email_change", kwargs["authorization"]))
        self.cancel_email_change_calls.append(kwargs)
        if self.on_cancel_email_change is not None:
            self.on_cancel_email_change()
        return self.cancel_email_change_response

    def auth_confirm_email_change(self, **kwargs: Any) -> Response:
        self.authorizations.append(("confirm_email_change", kwargs["authorization"]))
        self.confirm_email_change_calls.append(kwargs)
        if self.on_confirm_email_change is not None:
            self.on_confirm_email_change()
        return self.confirm_email_change_response

    def auth_delete_all_my_sessions(self, **kwargs: Any) -> Response:
        self.authorizations.append(("delete_other_sessions", kwargs["authorization"]))
        self.delete_other_sessions_calls.append(kwargs)
        if self.on_delete_other_sessions is not None:
            self.on_delete_other_sessions()
        return self.delete_other_sessions_response

    def auth_delete_my_session(self, **kwargs: Any) -> Response:
        self.authorizations.append(("delete_session", kwargs["authorization"]))
        self.delete_session_calls.append(kwargs)
        if self.on_delete_session is not None:
            self.on_delete_session()
        return self.delete_session_response

    def auth_get_my_sessions(self, **kwargs: Any) -> Response:
        self.authorizations.append(("list_sessions", kwargs["authorization"]))
        self.list_sessions_calls.append(kwargs)
        if self.on_list_sessions is not None:
            self.on_list_sessions()
        return self.list_sessions_response

    def auth_list_oauth_providers(self, **kwargs: Any) -> Response:
        self.authorizations.append(("list_oauth_providers", kwargs["authorization"]))
        self.list_oauth_providers_calls.append(kwargs)
        if self.on_list_oauth_providers is not None:
            self.on_list_oauth_providers()
        return self.list_oauth_providers_response

    def auth_oauth_authorization_url(self, **kwargs: Any) -> str:
        self.oauth_authorization_url_calls.append(kwargs)
        return self.oauth_authorization_url

    def auth_oauth_exchange(self, **kwargs: Any) -> Response:
        self.oauth_exchange_calls.append(kwargs)
        if self.on_oauth_exchange is not None:
            self.on_oauth_exchange()
        return self.oauth_exchange_response

    def auth_link_oauth_provider(self, **kwargs: Any) -> Response:
        self.authorizations.append(("link_oauth_provider", kwargs["authorization"]))
        self.link_oauth_provider_calls.append(kwargs)
        if self.on_link_oauth_provider is not None:
            self.on_link_oauth_provider()
        return self.link_oauth_provider_response

    def auth_unlink_oauth_provider(self, **kwargs: Any) -> Response:
        self.authorizations.append(("unlink_oauth_provider", kwargs["authorization"]))
        self.unlink_oauth_provider_calls.append(kwargs)
        if self.on_unlink_oauth_provider is not None:
            self.on_unlink_oauth_provider()
        return self.unlink_oauth_provider_response

    def auth_get_oauth_provider_token(self, **kwargs: Any) -> Response:
        self.authorizations.append(("oauth_token_status", kwargs["authorization"]))
        self.oauth_provider_token_status_calls.append(kwargs)
        if self.on_oauth_provider_token_status is not None:
            self.on_oauth_provider_token_status()
        return self.oauth_provider_token_status_response

    def auth_refresh_oauth_provider_token(self, **kwargs: Any) -> Response:
        self.authorizations.append(("refresh_oauth_token", kwargs["authorization"]))
        self.refresh_oauth_provider_token_calls.append(kwargs)
        if self.on_refresh_oauth_provider_token is not None:
            self.on_refresh_oauth_provider_token()
        return self.refresh_oauth_provider_token_response

    def auth_call_oauth_api(self, **kwargs: Any) -> Response:
        self.authorizations.append(("call_oauth_api", kwargs["authorization"]))
        self.call_oauth_api_calls.append(kwargs)
        if self.on_call_oauth_api is not None:
            self.on_call_oauth_api()
        return self.call_oauth_api_response

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


def test_auth_state_subscription_reports_session_transitions() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    events: list[tuple[str, Session | None]] = []

    subscription = client.auth.on_auth_state_change(
        lambda event, session: events.append((event, session))
    )
    signed_in = client.auth.sign_in(email="user@example.com", password="secret")
    refreshed = client.auth.refresh_session()
    client.auth.sign_out()

    assert isinstance(subscription, AuthSubscription)
    assert events == [
        ("INITIAL_SESSION", None),
        ("SIGNED_IN", signed_in),
        ("TOKEN_REFRESHED", refreshed),
        ("SIGNED_OUT", None),
    ]


def test_auth_state_subscription_unsubscribes_idempotently() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    events: list[tuple[str, Session | None]] = []
    subscription = client.auth.on_auth_state_change(
        lambda event, session: events.append((event, session))
    )

    subscription.unsubscribe()
    subscription.unsubscribe()
    client.auth.sign_in(email="user@example.com", password="secret")

    assert events == [("INITIAL_SESSION", None)]


def test_auth_state_subscription_handles_preserve_identity() -> None:
    client = VolcanoClient(anon_key="anon", _transport=StateTransport())

    first = client.auth.on_auth_state_change(lambda _event, _session: None)
    second = client.auth.on_auth_state_change(lambda _event, _session: None)

    assert first != second
    assert len({first, second}) == 2


def test_auth_state_subscription_requires_a_callable() -> None:
    client = VolcanoClient(anon_key="anon", _transport=StateTransport())

    with pytest.raises(TypeError, match="callback must be callable"):
        client.auth.on_auth_state_change(cast("Any", None))


def test_auth_state_callback_failure_does_not_interrupt_other_subscribers() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    received: list[tuple[str, Session | None]] = []

    def fail(_event: str, _session: Session | None) -> None:
        raise RuntimeError(_SUBSCRIBER_FAILED)

    client.auth.on_auth_state_change(fail)
    client.auth.on_auth_state_change(
        lambda event, session: received.append((event, session))
    )

    signed_in = client.auth.sign_in(email="user@example.com", password="secret")

    assert received == [
        ("INITIAL_SESSION", None),
        ("SIGNED_IN", signed_in),
    ]


def test_auth_state_callbacks_preserve_order_during_reentrant_changes() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    received: list[tuple[str, Session | None]] = []

    def sign_out_after_sign_in(event: str, _session: Session | None) -> None:
        if event == "SIGNED_IN":
            client.auth.sign_out()

    client.auth.on_auth_state_change(sign_out_after_sign_in)
    client.auth.on_auth_state_change(
        lambda event, session: received.append((event, session))
    )
    received.clear()

    signed_in = client.auth.sign_in(email="user@example.com", password="secret")

    assert received == [
        ("SIGNED_IN", signed_in),
        ("SIGNED_OUT", None),
    ]


def test_auth_state_unsubscribe_skips_queued_reentrant_changes() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    received: list[str] = []

    def sign_out_after_sign_in(event: str, _session: Session | None) -> None:
        if event == "SIGNED_IN":
            client.auth.sign_out()

    client.auth.on_auth_state_change(sign_out_after_sign_in)
    subscription: AuthSubscription

    def unsubscribe_after_sign_in(event: str, _session: Session | None) -> None:
        received.append(event)
        if event == "SIGNED_IN":
            subscription.unsubscribe()

    subscription = client.auth.on_auth_state_change(unsubscribe_after_sign_in)
    received.clear()

    client.auth.sign_in(email="user@example.com", password="secret")

    assert received == ["SIGNED_IN"]


def test_auth_state_dispatch_recovers_after_a_base_exception() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    received: list[str] = []

    def interrupt_after_sign_in(event: str, _session: Session | None) -> None:
        if event == "SIGNED_IN":
            raise KeyboardInterrupt

    interrupting = client.auth.on_auth_state_change(interrupt_after_sign_in)
    client.auth.on_auth_state_change(lambda event, _session: received.append(event))
    received.clear()

    with pytest.raises(KeyboardInterrupt):
        client.auth.sign_in(email="user@example.com", password="secret")

    interrupting.unsubscribe()
    client.auth.sign_out()

    assert received == ["SIGNED_IN", "SIGNED_OUT"]


def test_auth_state_subscription_rolls_back_when_initial_delivery_aborts() -> None:
    client = VolcanoClient(anon_key="anon", _transport=StateTransport())
    received: list[str] = []
    observed: list[str] = []

    def interrupt(event: str, _session: Session | None) -> None:
        received.append(event)
        raise _SubscriberAbortError

    with pytest.raises(_SubscriberAbortError):
        client.auth.on_auth_state_change(interrupt)

    client.auth.on_auth_state_change(lambda event, _session: observed.append(event))
    client.auth.sign_in(email="user@example.com", password="secret")

    assert received == ["INITIAL_SESSION"]
    assert observed == ["INITIAL_SESSION", "SIGNED_IN"]


def test_auth_state_dispatch_preserves_concurrent_notifications_on_abort() -> None:
    client = VolcanoClient(anon_key="anon", _transport=StateTransport())
    entered = Event()
    release = Event()
    received: list[str] = []

    def interrupt(event: str, _session: Session | None) -> None:
        if event == "SIGNED_IN":
            entered.set()
            assert release.wait(timeout=1)
            raise _SubscriberAbortError

    client.auth.on_auth_state_change(interrupt)
    client.auth.on_auth_state_change(lambda event, _session: received.append(event))
    received.clear()

    def sign_out() -> None:
        assert entered.wait(timeout=1)
        client.auth.sign_out()
        release.set()

    sign_out_thread = Thread(target=sign_out)
    sign_out_thread.start()
    with pytest.raises(_SubscriberAbortError):
        client.auth.sign_in(email="user@example.com", password="secret")
    sign_out_thread.join(timeout=1)

    assert not sign_out_thread.is_alive()
    assert received == ["SIGNED_IN", "SIGNED_OUT"]


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


def test_request_email_change_rejects_a_non_object_response() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    transport.email_change_response = Response(200, [])

    with pytest.raises(TypeError, match="valid email-change acknowledgement"):
        client.auth.request_email_change(new_email="new@example.com")


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


def test_cancel_email_change_preserves_the_current_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")

    client.auth.cancel_email_change()

    assert client.auth.get_session() is established
    assert transport.cancel_email_change_calls == [{"authorization": "access-1"}]


def test_cancel_email_change_requires_a_current_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(AuthenticationError, match="No active session"):
        client.auth.cancel_email_change()

    assert transport.cancel_email_change_calls == []


def test_cancel_email_change_rejects_a_stale_response() -> None:
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

    transport.on_cancel_email_change = replace_session

    with pytest.raises(SessionChangedError):
        client.auth.cancel_email_change()

    assert client.auth.get_session() == replacement


def test_confirm_email_change_returns_user_without_replacing_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")

    user = client.auth.confirm_email_change(token="change-token")

    assert user.email == "new@example.com"
    assert client.auth.get_session() is established
    assert transport.confirm_email_change_calls == [
        {"authorization": "access-1", "token": "change-token"}
    ]


def test_confirm_email_change_requires_a_current_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(AuthenticationError, match="No active session"):
        client.auth.confirm_email_change(token="change-token")

    assert transport.confirm_email_change_calls == []


def test_confirm_email_change_rejects_a_missing_user() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    transport.confirm_email_change_response = Response(
        200,
        AuthConfirmEmailChangeResponse200(),
    )

    with pytest.raises(AuthenticationError, match="complete user profile"):
        client.auth.confirm_email_change(token="change-token")


def test_confirm_email_change_rejects_a_stale_response() -> None:
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

    transport.on_confirm_email_change = replace_session

    with pytest.raises(SessionChangedError):
        client.auth.confirm_email_change(token="change-token")

    assert client.auth.get_session() == replacement


def test_list_sessions_returns_an_immutable_offset_page() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")

    result = client.auth.list_sessions(page=2, limit=10)

    assert result == SessionPage(
        sessions=(
            AuthSession(
                id="00000000-0000-4000-8000-000000000099",
                user_id="00000000-0000-4000-8000-000000000010",
                provider="email",
                expires_at=datetime.fromisoformat("2026-09-02T12:00:00+00:00"),
                is_active=True,
                is_current=True,
                user_agent="Volcano Test",
                ip_address="192.0.2.10",
                last_ip_address="192.0.2.11",
                last_activity_at=datetime.fromisoformat("2026-09-01T12:00:00+00:00"),
                session_started_at=datetime.fromisoformat("2026-08-31T12:00:00+00:00"),
                created_at=datetime.fromisoformat("2026-08-31T12:00:00+00:00"),
                updated_at=datetime.fromisoformat("2026-09-01T12:00:00+00:00"),
            ),
        ),
        total=21,
        page=2,
        limit=10,
        total_pages=3,
    )
    assert client.auth.get_session() is established
    assert transport.list_sessions_calls == [
        {"authorization": "access-1", "page": 2, "limit": 10}
    ]
    with pytest.raises(FrozenInstanceError):
        result.page = 3  # type: ignore[misc]


def test_list_sessions_requires_a_current_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(AuthenticationError, match="No active session"):
        client.auth.list_sessions()

    assert transport.list_sessions_calls == []


def test_list_sessions_rejects_non_integer_pagination_values() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    payload = _sessions_page().to_dict()
    payload["total"] = "21"
    transport.list_sessions_response = Response(
        200,
        AuthGetMySessionsResponse200.from_dict(payload),
    )

    with pytest.raises(VolcanoError, match="Expected a complete session page"):
        client.auth.list_sessions()


@pytest.mark.parametrize(
    ("field", "value"),
    [("is_active", "false"), ("user_agent", 42)],
)
def test_list_sessions_rejects_invalid_session_scalars(
    field: str,
    value: object,
) -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    payload = _sessions_page().to_dict()
    payload["sessions"][0][field] = value
    transport.list_sessions_response = Response(
        200,
        AuthGetMySessionsResponse200.from_dict(payload),
    )

    with pytest.raises(VolcanoError, match="Expected a complete session page"):
        client.auth.list_sessions()


def test_list_sessions_rejects_a_stale_response() -> None:
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

    transport.on_list_sessions = replace_session

    with pytest.raises(SessionChangedError):
        client.auth.list_sessions()

    assert client.auth.get_session() == replacement


def test_list_linked_oauth_providers_returns_immutable_values() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")

    result = client.auth.list_linked_oauth_providers()

    assert result == (
        LinkedOAuthProvider(
            provider="google",
            linked_at=datetime.fromisoformat("2026-08-30T12:00:00+00:00"),
            updated_at=datetime.fromisoformat("2026-09-01T12:00:00+00:00"),
        ),
    )
    assert client.auth.get_session() is established
    assert transport.list_oauth_providers_calls == [{"authorization": "access-1"}]
    with pytest.raises(FrozenInstanceError):
        result[0].provider = "github"  # type: ignore[misc]


def test_list_linked_oauth_providers_requires_a_current_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(AuthenticationError, match="No active session"):
        client.auth.list_linked_oauth_providers()

    assert transport.list_oauth_providers_calls == []


def test_list_linked_oauth_providers_rejects_an_incomplete_item() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    transport.list_oauth_providers_response = Response(
        200,
        AuthListOAuthProvidersResponse200.from_dict(
            {"providers": [{"provider": "google"}]}
        ),
    )

    with pytest.raises(VolcanoError, match="Expected complete linked OAuth providers"):
        client.auth.list_linked_oauth_providers()


def test_list_linked_oauth_providers_accepts_a_future_provider_name() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    transport.list_oauth_providers_response = Response(
        200,
        AuthListOAuthProvidersResponse200.from_dict(
            {
                "providers": [
                    {
                        "provider": "future-provider",
                        "linked_at": "2026-08-30T12:00:00Z",
                        "updated_at": "2026-09-01T12:00:00Z",
                    }
                ]
            }
        ),
    )

    result = client.auth.list_linked_oauth_providers()

    assert result[0].provider == "future-provider"


def test_list_linked_oauth_providers_rejects_a_stale_response() -> None:
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

    transport.on_list_oauth_providers = replace_session

    with pytest.raises(SessionChangedError):
        client.auth.list_linked_oauth_providers()

    assert client.auth.get_session() == replacement


def test_link_oauth_provider_returns_an_authorization_url() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")

    result = client.auth.link_oauth_provider(provider="github")

    assert result == "https://accounts.example/link"
    assert client.auth.get_session() is established
    assert transport.link_oauth_provider_calls == [
        {"authorization": "access-1", "provider": "github"}
    ]


@pytest.mark.parametrize(
    "action",
    [
        "login",
        "signup",
        "forgot-password",
    ],
)
def test_get_hosted_auth_url_builds_the_canonical_action_url(
    action: str,
) -> None:
    client = VolcanoClient(
        api_url="https://api.example.com/root/",
        anon_key="anon key",
        _transport=StateTransport(),
    )

    result = client.auth.get_hosted_auth_url(
        project_id="project/id",
        action=cast("Any", action),
        state="state value",
    )

    assert result == (
        "https://api.example.com/root/projects/project%2Fid/auth/hosted"
        f"?action={action}&anon_key=anon+key&state=state+value"
    )
    assert client.auth.get_session() is None


@pytest.mark.parametrize(
    ("argument", "value"),
    [
        ("project_id", " "),
        ("state", ""),
    ],
)
def test_get_hosted_auth_url_rejects_empty_parameters(
    argument: str,
    value: str,
) -> None:
    client = VolcanoClient(anon_key="anon", _transport=StateTransport())
    options = {
        "project_id": "project-id",
        "action": "login",
        "state": "state-value",
        argument: value,
    }

    with pytest.raises(ValueError, match="Hosted auth parameters must be non-empty"):
        client.auth.get_hosted_auth_url(**cast("Any", options))


def test_get_hosted_auth_url_rejects_an_unknown_action() -> None:
    client = VolcanoClient(anon_key="anon", _transport=StateTransport())

    with pytest.raises(ValueError, match="Unsupported hosted auth action"):
        client.auth.get_hosted_auth_url(
            project_id="project-id",
            action=cast("Any", "device"),
            state="state-value",
        )


def test_adopt_hosted_auth_session_validates_state_and_stores_an_owned_copy() -> None:
    client = VolcanoClient(anon_key="anon", _transport=StateTransport())
    supplied = Session(
        access_token="hosted-access",
        refresh_token="hosted-refresh",
        user_id="hosted-user",
    )

    adopted = client.auth.adopt_hosted_auth_session(
        supplied,
        state="returned-state",
        expected_state="returned-state",
    )

    assert adopted == supplied
    assert adopted is not supplied
    assert client.auth.get_session() is adopted


def test_hosted_auth_state_mismatch_preserves_current_session() -> None:
    client = VolcanoClient(anon_key="anon", _transport=StateTransport())
    established = client.auth.set_session(
        Session(access_token="access", refresh_token="refresh", user_id="user")
    )
    returned = Session(
        access_token="attacker-access",
        refresh_token="attacker-refresh",
        user_id="attacker-user",
    )

    with pytest.raises(ValueError, match="Hosted auth state mismatch"):
        client.auth.adopt_hosted_auth_session(
            returned,
            state="attacker-state",
            expected_state="expected-state",
        )

    assert client.auth.get_session() is established


@pytest.mark.parametrize("argument", ["state", "expected_state"])
def test_adopt_hosted_auth_session_rejects_empty_state(argument: str) -> None:
    client = VolcanoClient(anon_key="anon", _transport=StateTransport())
    options = {"state": "state-value", "expected_state": "state-value", argument: " "}

    with pytest.raises(ValueError, match="Hosted auth parameters must be non-empty"):
        client.auth.adopt_hosted_auth_session(
            Session(access_token="access", refresh_token="refresh", user_id="user"),
            **cast("Any", options),
        )

    assert client.auth.get_session() is None


def test_sign_in_with_oauth_returns_an_authorization_url_without_a_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    result = client.auth.sign_in_with_oauth(
        provider="github",
        redirect_to="https://app.example/callback",
        state="state-value",
    )

    assert result == "https://api.example/auth/oauth/github/authorize"
    assert client.auth.get_session() is None
    assert transport.oauth_authorization_url_calls == [
        {
            "anon_key": "anon",
            "provider": "github",
            "redirect_url": "https://app.example/callback",
            "client_state": "state-value",
        }
    ]


def test_sign_in_with_oauth_rejects_an_unknown_provider() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(ValueError, match="Unsupported OAuth provider"):
        client.auth.sign_in_with_oauth(
            provider="invalid",  # type: ignore[arg-type]
            redirect_to="https://app.example/callback",
            state="state-value",
        )

    assert transport.oauth_authorization_url_calls == []


def test_exchange_oauth_code_stores_the_session_after_state_validation() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    result = client.auth.exchange_oauth_code(
        code="oauth-code",
        redirect_to="https://app.example/callback",
        state="state-value",
        expected_state="state-value",
    )

    assert result == Session(
        access_token="oauth-access",
        refresh_token="oauth-refresh",
        user_id="00000000-0000-4000-8000-000000000010",
    )
    assert client.auth.get_session() is result
    assert transport.oauth_exchange_calls == [
        {
            "authorization": "anon",
            "code": "oauth-code",
            "redirect_url": "https://app.example/callback",
        }
    ]


def test_exchange_oauth_code_rejects_a_state_mismatch_without_a_request() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(ValueError, match="OAuth state mismatch"):
        client.auth.exchange_oauth_code(
            code="oauth-code",
            redirect_to="https://app.example/callback",
            state="attacker-state",
            expected_state="expected-state",
        )

    assert transport.oauth_exchange_calls == []


def test_exchange_oauth_code_accepts_matching_unicode_state() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    result = client.auth.exchange_oauth_code(
        code="oauth-code",
        redirect_to="https://app.example/callback",
        state="état",
        expected_state="état",
    )

    assert client.auth.get_session() is result


def test_exchange_oauth_code_does_not_replace_a_concurrent_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    replacement = Session(
        access_token="replacement-access",
        refresh_token="replacement-refresh",
        user_id="replacement-user",
    )

    def replace_session() -> None:
        client.auth.set_session(replacement)

    transport.on_oauth_exchange = replace_session

    with pytest.raises(SessionChangedError):
        client.auth.exchange_oauth_code(
            code="oauth-code",
            redirect_to="https://app.example/callback",
            state="state-value",
            expected_state="state-value",
        )

    assert client.auth.get_session() == replacement


def test_link_oauth_provider_rejects_an_unknown_provider() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(ValueError, match="Unsupported OAuth provider"):
        client.auth.link_oauth_provider(provider="invalid")  # type: ignore[arg-type]

    assert transport.link_oauth_provider_calls == []


def test_link_oauth_provider_requires_a_current_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(AuthenticationError, match="No active session"):
        client.auth.link_oauth_provider(provider="google")

    assert transport.link_oauth_provider_calls == []


def test_link_oauth_provider_rejects_an_incomplete_response() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    transport.link_oauth_provider_response = Response(
        200,
        AuthLinkOAuthProviderResponse200(),
    )

    with pytest.raises(VolcanoError, match="Expected an OAuth authorization URL"):
        client.auth.link_oauth_provider(provider="google")


def test_link_oauth_provider_rejects_a_stale_response() -> None:
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

    transport.on_link_oauth_provider = replace_session

    with pytest.raises(SessionChangedError):
        client.auth.link_oauth_provider(provider="google")

    assert client.auth.get_session() == replacement


def test_unlink_oauth_provider_preserves_the_current_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")

    client.auth.unlink_oauth_provider(provider="github")

    assert client.auth.get_session() is established
    assert transport.unlink_oauth_provider_calls == [
        {"authorization": "access-1", "provider": "github"}
    ]


def test_unlink_oauth_provider_rejects_an_unknown_provider() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(ValueError, match="Unsupported OAuth provider"):
        client.auth.unlink_oauth_provider(provider="invalid")  # type: ignore[arg-type]

    assert transport.unlink_oauth_provider_calls == []


def test_unlink_oauth_provider_requires_a_current_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(AuthenticationError, match="No active session"):
        client.auth.unlink_oauth_provider(provider="google")

    assert transport.unlink_oauth_provider_calls == []


def test_unlink_oauth_provider_rejects_a_stale_response() -> None:
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

    transport.on_unlink_oauth_provider = replace_session

    with pytest.raises(SessionChangedError):
        client.auth.unlink_oauth_provider(provider="google")

    assert client.auth.get_session() == replacement


def test_get_oauth_provider_token_returns_immutable_status() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")

    result = client.auth.get_oauth_provider_token(provider="google")

    assert result == OAuthProviderTokenStatus(
        message="Provider token is valid",
        provider="google",
        expires_in=3600,
    )
    assert client.auth.get_session() is established
    assert transport.oauth_provider_token_status_calls == [
        {"authorization": "access-1", "provider": "google"}
    ]
    with pytest.raises(FrozenInstanceError):
        result.provider = "github"  # type: ignore[misc]


def test_get_oauth_provider_token_rejects_an_unknown_provider() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(ValueError, match="Unsupported OAuth provider"):
        client.auth.get_oauth_provider_token(provider="invalid")  # type: ignore[arg-type]

    assert transport.oauth_provider_token_status_calls == []


def test_get_oauth_provider_token_requires_a_current_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(AuthenticationError, match="No active session"):
        client.auth.get_oauth_provider_token(provider="google")

    assert transport.oauth_provider_token_status_calls == []


@pytest.mark.parametrize(
    "payload",
    [
        {"provider": "google", "expires_in": 3600},
        {"message": "Provider token is valid", "expires_in": 3600},
        {"message": "Provider token is valid", "provider": "google"},
        {
            "message": "Provider token is valid",
            "provider": "google",
            "expires_in": True,
        },
    ],
)
def test_get_oauth_provider_token_rejects_incomplete_status(
    payload: dict[str, object],
) -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    transport.oauth_provider_token_status_response = Response(
        200,
        GetOAuthProviderTokenResponse200.from_dict(payload),
    )

    with pytest.raises(
        VolcanoError, match="Expected complete OAuth provider token status"
    ):
        client.auth.get_oauth_provider_token(provider="google")


def test_get_oauth_provider_token_accepts_a_future_provider_name() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    transport.oauth_provider_token_status_response = Response(
        200,
        GetOAuthProviderTokenResponse200.from_dict(
            {
                "message": "Provider token is valid",
                "provider": "future-provider",
                "expires_in": 3600,
            }
        ),
    )

    result = client.auth.get_oauth_provider_token(provider="google")

    assert result.provider == "future-provider"


def test_get_oauth_provider_token_rejects_a_stale_response() -> None:
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

    transport.on_oauth_provider_token_status = replace_session

    with pytest.raises(SessionChangedError):
        client.auth.get_oauth_provider_token(provider="google")

    assert client.auth.get_session() == replacement


def test_refresh_oauth_provider_token_returns_immutable_status() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")

    result = client.auth.refresh_oauth_provider_token(provider="google")

    assert result == OAuthProviderTokenStatus(
        message="Provider token refreshed successfully",
        provider="google",
        expires_in=3600,
    )
    assert client.auth.get_session() is established
    assert transport.refresh_oauth_provider_token_calls == [
        {"authorization": "access-1", "provider": "google"}
    ]
    with pytest.raises(FrozenInstanceError):
        result.provider = "github"  # type: ignore[misc]


def test_refresh_oauth_provider_token_rejects_an_unknown_provider() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(ValueError, match="Unsupported OAuth provider"):
        client.auth.refresh_oauth_provider_token(provider="invalid")  # type: ignore[arg-type]

    assert transport.refresh_oauth_provider_token_calls == []


def test_refresh_oauth_provider_token_requires_a_current_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(AuthenticationError, match="No active session"):
        client.auth.refresh_oauth_provider_token(provider="google")

    assert transport.refresh_oauth_provider_token_calls == []


def test_refresh_oauth_provider_token_rejects_incomplete_status() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.sign_in(email="user@example.com", password="secret")
    transport.refresh_oauth_provider_token_response = Response(
        200,
        RefreshOAuthProviderTokenResponse200.from_dict(
            {"provider": "google", "expires_in": 3600}
        ),
    )

    with pytest.raises(
        VolcanoError, match="Expected complete OAuth provider token status"
    ):
        client.auth.refresh_oauth_provider_token(provider="google")


def test_refresh_oauth_provider_token_rejects_a_stale_response() -> None:
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

    transport.on_refresh_oauth_provider_token = replace_session

    with pytest.raises(SessionChangedError):
        client.auth.refresh_oauth_provider_token(provider="google")

    assert client.auth.get_session() == replacement


def test_call_oauth_api_returns_immutable_provider_data() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")

    result = client.auth.call_oauth_api(
        provider="github",
        endpoint="/user/repos",
        method="POST",
        body={"visibility": "private"},
    )

    assert result == ({"name": "volcano"},)
    assert client.auth.get_session() is established
    assert transport.call_oauth_api_calls == [
        {
            "authorization": "access-1",
            "provider": "github",
            "endpoint": "/user/repos",
            "method": "POST",
            "body": {"visibility": "private"},
        }
    ]
    repos = cast("tuple[dict[str, object], ...]", result)
    with pytest.raises(TypeError):
        repos[0]["name"] = "changed"


def test_call_oauth_api_rejects_an_unknown_provider() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(ValueError, match="Unsupported OAuth provider"):
        client.auth.call_oauth_api(
            provider="invalid",  # type: ignore[arg-type]
            endpoint="/user",
        )

    assert transport.call_oauth_api_calls == []


def test_call_oauth_api_rejects_an_unsupported_method() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(ValueError, match="Unsupported OAuth provider API method"):
        client.auth.call_oauth_api(
            provider="github",
            endpoint="/user",
            method="DELETE",  # type: ignore[arg-type]
        )

    assert transport.call_oauth_api_calls == []


def test_call_oauth_api_requires_a_current_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(AuthenticationError, match="No active session"):
        client.auth.call_oauth_api(provider="github", endpoint="/user")

    assert transport.call_oauth_api_calls == []


def test_call_oauth_api_rejects_a_stale_response() -> None:
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

    transport.on_call_oauth_api = replace_session

    with pytest.raises(SessionChangedError):
        client.auth.call_oauth_api(provider="github", endpoint="/user")

    assert client.auth.get_session() == replacement


def test_delete_all_other_sessions_preserves_the_current_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")

    client.auth.delete_all_other_sessions()

    assert client.auth.get_session() is established
    assert transport.delete_other_sessions_calls == [{"authorization": "access-1"}]


def test_delete_all_other_sessions_requires_a_current_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(AuthenticationError, match="No active session"):
        client.auth.delete_all_other_sessions()

    assert transport.delete_other_sessions_calls == []


def test_delete_all_other_sessions_rejects_a_stale_response() -> None:
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

    transport.on_delete_other_sessions = replace_session

    with pytest.raises(SessionChangedError):
        client.auth.delete_all_other_sessions()

    assert client.auth.get_session() == replacement


def test_delete_session_preserves_the_current_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    established = client.auth.sign_in(email="user@example.com", password="secret")

    client.auth.delete_session(session_id="00000000-0000-4000-8000-000000000099")

    assert client.auth.get_session() is established
    assert transport.delete_session_calls == [
        {
            "authorization": "access-1",
            "session_id": "00000000-0000-4000-8000-000000000099",
        }
    ]


def test_delete_session_requires_a_current_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)

    with pytest.raises(AuthenticationError, match="No active session"):
        client.auth.delete_session(session_id="00000000-0000-4000-8000-000000000099")

    assert transport.delete_session_calls == []


def test_delete_session_rejects_a_stale_response() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    session_id = "00000000-0000-4000-8000-000000000099"
    client.auth.set_session(
        Session(
            access_token=_access_token_with_session_id(session_id),
            refresh_token="original-refresh",
            user_id="original-user",
        )
    )
    replacement = Session(
        access_token="replacement-access",
        refresh_token="replacement-refresh",
        user_id="replacement-user",
    )

    def replace_session() -> None:
        client.auth.set_session(replacement)

    transport.on_delete_session = replace_session

    with pytest.raises(SessionChangedError):
        client.auth.delete_session(session_id=session_id)

    assert client.auth.get_session() == replacement


def test_delete_session_clears_the_deleted_current_session() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    session_id = "00000000-0000-4000-8000-0000000000ab"
    client.auth.set_session(
        Session(
            access_token=_access_token_with_session_id(session_id),
            refresh_token="current-refresh",
            user_id="current-user",
        )
    )

    client.auth.delete_session(session_id=session_id.upper())

    assert client.auth.get_session() is None


def test_delete_session_clears_current_state_when_the_response_is_lost() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    session_id = "00000000-0000-4000-8000-000000000099"
    client.auth.set_session(
        Session(
            access_token=_access_token_with_session_id(session_id),
            refresh_token="current-refresh",
            user_id="current-user",
        )
    )

    def lose_response() -> None:
        raise httpx.ReadError(_CONNECTION_LOST)

    transport.on_delete_session = lose_response

    with pytest.raises(TransportError, match="connection lost"):
        client.auth.delete_session(session_id=session_id)

    assert client.auth.get_session() is None


def test_delete_session_preserves_current_state_when_the_server_rejects_it() -> None:
    transport = StateTransport()
    client = VolcanoClient(anon_key="anon", _transport=transport)
    session_id = "00000000-0000-4000-8000-000000000099"
    current = Session(
        access_token=_access_token_with_session_id(session_id),
        refresh_token="current-refresh",
        user_id="current-user",
    )
    client.auth.set_session(current)
    stored = client.auth.get_session()
    transport.delete_session_response = Response(401, {"error": "expired"})

    with pytest.raises(AuthenticationError, match="expired"):
        client.auth.delete_session(session_id=session_id)

    assert client.auth.get_session() is stored


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
