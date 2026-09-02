from __future__ import annotations

import json
from types import MappingProxyType

import httpx
import pytest

from volcano_sdk import AuthenticationError, RateLimitedError, VolcanoError
from volcano_sdk._generated.models.auth_convert_anonymous_response_200 import (
    AuthConvertAnonymousResponse200,
)
from volcano_sdk._generated.models.auth_get_user_response_200 import (
    AuthGetUserResponse200,
)
from volcano_sdk._generated.models.auth_update_user_response_200 import (
    AuthUpdateUserResponse200,
)
from volcano_sdk._generated.types import Unset
from volcano_sdk._transport import (
    GeneratedTransport,
    StorageUploadPartRequest,
    StorageUploadSessionReference,
    StorageUploadSessionRequest,
    response_payload,
)


def test_generated_transport_builds_an_oauth_authorization_url() -> None:
    transport = GeneratedTransport(api_url="https://api.test.volcano.dev")

    result = transport.auth_oauth_authorization_url(
        anon_key="anon key",
        provider="github",
        redirect_url="https://app.example/callback?next=/repos",
        client_state="state-value",
    )

    url = httpx.URL(result)
    assert url.scheme == "https"
    assert url.host == "api.test.volcano.dev"
    assert url.path == "/auth/oauth/github/authorize"
    assert dict(url.params) == {
        "anon_key": "anon key",
        "redirect_url": "https://app.example/callback?next=/repos",
        "client_state": "state-value",
        "response_mode": "code",
    }


def test_generated_transport_exchanges_an_oauth_code() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "access_token": "oauth-access",
                "refresh_token": "oauth-refresh",
                "token_type": "bearer",
                "expires_in": 3600,
                "user": {
                    "id": "00000000-0000-4000-8000-000000000010",
                    "email": "user@example.com",
                    "status": "active",
                },
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_oauth_exchange(
        authorization="anon-key",
        code="oauth-code",
        redirect_url="https://app.example/callback",
    )

    assert response.status_code == 200
    assert requests[0].url.path == "/auth/oauth/exchange"
    assert requests[0].headers["authorization"] == "Bearer anon-key"
    assert json.loads(requests[0].content) == {
        "code": "oauth-code",
        "redirect_url": "https://app.example/callback",
    }


def test_generated_transport_signs_up_with_the_anon_key_and_metadata() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            201,
            json={
                "confirmation_required": True,
                "message": "Check your email to confirm your account",
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_signup(
        authorization="anon-key",
        email="user@example.com",
        password="secret",
        metadata={"display_name": "New User"},
    )

    assert response.status_code == 201
    assert response.payload == {
        "confirmation_required": True,
        "message": "Check your email to confirm your account",
    }
    assert requests[0].method == "POST"
    assert requests[0].url.path == "/auth/signup"
    assert requests[0].headers["authorization"] == "Bearer anon-key"
    assert json.loads(requests[0].content) == {
        "email": "user@example.com",
        "password": "secret",
        "user_metadata": {"display_name": "New User"},
    }


def test_generated_transport_signs_in_anonymously_with_metadata() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            201,
            json={
                "access_token": "anonymous-access",
                "refresh_token": "anonymous-refresh",
                "user": {"id": "00000000-0000-4000-8000-000000000099"},
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_signup_anonymous(
        authorization="anon-key",
        metadata={"device": "mobile"},
    )

    assert response.status_code == 201
    assert requests[0].method == "POST"
    assert requests[0].url.path == "/auth/signup-anonymous"
    assert requests[0].headers["authorization"] == "Bearer anon-key"
    assert json.loads(requests[0].content) == {"user_metadata": {"device": "mobile"}}


def test_generated_transport_converts_an_anonymous_user() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "user": {
                    "id": "00000000-0000-4000-8000-000000000099",
                    "email": "converted@example.com",
                    "status": "active",
                }
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_convert_anonymous(
        authorization="anonymous-access",
        email="converted@example.com",
        password="secret",
        metadata={"display_name": "Ada"},
    )

    assert response.status_code == 200
    assert isinstance(response.payload, AuthConvertAnonymousResponse200)
    assert requests[0].method == "POST"
    assert requests[0].url.path == "/auth/user/convert-anonymous"
    assert requests[0].headers["authorization"] == "Bearer anonymous-access"
    assert json.loads(requests[0].content) == {
        "email": "converted@example.com",
        "password": "secret",
        "user_metadata": {"display_name": "Ada"},
    }


def test_generated_transport_requests_an_email_change() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={})

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_request_email_change(
        authorization="access-token",
        new_email="new@example.com",
    )

    assert response.status_code == 200
    assert requests[0].method == "POST"
    assert requests[0].url.path == "/auth/user/change-email"
    assert requests[0].headers["authorization"] == "Bearer access-token"
    assert json.loads(requests[0].content) == {"new_email": "new@example.com"}


def test_generated_transport_cancels_an_email_change() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, content=b"")

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_cancel_email_change(authorization="access-token")

    assert response.status_code == 200
    assert requests[0].method == "DELETE"
    assert requests[0].url.path == "/auth/user/cancel-email-change"
    assert requests[0].headers["authorization"] == "Bearer access-token"


def test_generated_transport_confirms_an_email_change() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "user": {
                    "id": "00000000-0000-4000-8000-000000000010",
                    "email": "new@example.com",
                    "status": "active",
                }
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_confirm_email_change(
        authorization="access-token",
        token="change-token",
    )

    assert response.status_code == 200
    assert requests[0].method == "POST"
    assert requests[0].url.path == "/auth/user/confirm-email-change"
    assert requests[0].headers["authorization"] == "Bearer access-token"
    assert json.loads(requests[0].content) == {"email_change_token": "change-token"}


def test_generated_transport_lists_sessions_with_offset_pagination() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "sessions": [
                    {
                        "id": "00000000-0000-4000-8000-000000000099",
                        "user_id": "00000000-0000-4000-8000-000000000010",
                        "provider": "email",
                        "expires_at": "2026-09-02T12:00:00Z",
                        "is_active": True,
                        "is_current": True,
                    }
                ],
                "total": 21,
                "page": 2,
                "limit": 10,
                "total_pages": 3,
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_get_my_sessions(
        authorization="access-token",
        page=2,
        limit=10,
    )

    assert response.status_code == 200
    assert requests[0].method == "GET"
    assert requests[0].url.path == "/auth/user/sessions"
    assert dict(requests[0].url.params) == {
        "page": "2",
        "limit": "10",
        "sort": "last_activity",
    }
    assert requests[0].headers["authorization"] == "Bearer access-token"


def test_generated_transport_rejects_a_malformed_session_page() -> None:
    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(
            lambda _request: httpx.Response(200, content=b"not-json")
        ),
    )

    with pytest.raises(VolcanoError, match="Expected a complete session page"):
        transport.auth_get_my_sessions(
            authorization="access-token",
            page=1,
            limit=20,
        )


def test_generated_transport_preserves_a_malformed_session_auth_error() -> None:
    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(
            lambda _request: httpx.Response(401, content=b"not-json")
        ),
    )

    response = transport.auth_get_my_sessions(
        authorization="access-token",
        page=1,
        limit=20,
    )

    with pytest.raises(AuthenticationError) as caught:
        response_payload(response, 200)

    assert caught.value.status == 401


def test_generated_transport_lists_linked_oauth_providers() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "providers": [
                    {
                        "provider": "google",
                        "linked_at": "2026-08-30T12:00:00Z",
                        "updated_at": "2026-09-01T12:00:00Z",
                    }
                ]
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_list_oauth_providers(authorization="access-token")

    assert response.status_code == 200
    assert requests[0].method == "GET"
    assert requests[0].url.path == "/auth/oauth/providers"
    assert requests[0].headers["authorization"] == "Bearer access-token"


def test_generated_transport_rejects_malformed_linked_oauth_providers() -> None:
    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(
            lambda _request: httpx.Response(200, content=b"not-json")
        ),
    )

    with pytest.raises(VolcanoError, match="Expected complete linked OAuth providers"):
        transport.auth_list_oauth_providers(authorization="access-token")


def test_generated_transport_preserves_a_malformed_oauth_auth_error() -> None:
    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(
            lambda _request: httpx.Response(401, content=b"not-json")
        ),
    )

    response = transport.auth_list_oauth_providers(authorization="access-token")

    with pytest.raises(AuthenticationError) as caught:
        response_payload(response, 200)

    assert caught.value.status == 401


def test_generated_transport_starts_linking_an_oauth_provider() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={"authorization_url": "https://accounts.example/link"},
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_link_oauth_provider(
        authorization="access-token",
        provider="github",
    )

    assert response.status_code == 200
    assert requests[0].method == "POST"
    assert requests[0].url.path == "/auth/oauth/github/link"
    assert requests[0].headers["authorization"] == "Bearer access-token"


def test_generated_transport_rejects_a_malformed_oauth_link_response() -> None:
    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(
            lambda _request: httpx.Response(200, content=b"not-json")
        ),
    )

    with pytest.raises(VolcanoError, match="Expected an OAuth authorization URL"):
        transport.auth_link_oauth_provider(
            authorization="access-token",
            provider="google",
        )


def test_generated_transport_preserves_a_malformed_oauth_link_auth_error() -> None:
    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(
            lambda _request: httpx.Response(401, content=b"not-json")
        ),
    )

    response = transport.auth_link_oauth_provider(
        authorization="access-token",
        provider="google",
    )

    with pytest.raises(AuthenticationError) as caught:
        response_payload(response, 200)

    assert caught.value.status == 401


def test_generated_transport_unlinks_an_oauth_provider() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(204)

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_unlink_oauth_provider(
        authorization="access-token",
        provider="github",
    )

    assert response.status_code == 204
    assert requests[0].method == "DELETE"
    assert requests[0].url.path == "/auth/oauth/github/unlink"
    assert requests[0].headers["authorization"] == "Bearer access-token"


def test_generated_transport_gets_oauth_provider_token_status() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "message": "Provider token is valid",
                "provider": "google",
                "expires_in": 3600,
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_get_oauth_provider_token(
        authorization="access-token",
        provider="google",
    )

    assert response.status_code == 200
    assert requests[0].method == "GET"
    assert requests[0].url.path == "/auth/oauth/google/token"
    assert requests[0].headers["authorization"] == "Bearer access-token"


def test_generated_transport_refreshes_an_oauth_provider_token() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "message": "Provider token refreshed successfully",
                "provider": "google",
                "expires_in": 3600,
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_refresh_oauth_provider_token(
        authorization="access-token",
        provider="google",
    )

    assert response.status_code == 200
    assert requests[0].method == "POST"
    assert requests[0].url.path == "/auth/oauth/google/refresh-token"
    assert requests[0].headers["authorization"] == "Bearer access-token"


def test_generated_transport_calls_an_oauth_provider_api() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "provider": "github",
                "endpoint": "/user/repos",
                "status_code": 200,
                "data": [{"name": "volcano"}],
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_call_oauth_api(
        authorization="access-token",
        provider="github",
        endpoint="/user/repos",
        method="POST",
        body={"visibility": "private"},
    )

    assert response.status_code == 200
    assert requests[0].method == "POST"
    assert requests[0].url.path == "/auth/oauth/github/call-api"
    assert requests[0].headers["authorization"] == "Bearer access-token"
    assert json.loads(requests[0].content) == {
        "endpoint": "/user/repos",
        "method": "POST",
        "body": {"visibility": "private"},
    }


def test_generated_transport_normalizes_immutable_oauth_api_body() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "provider": "github",
                "endpoint": "/user/repos",
                "status_code": 200,
                "data": {},
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    transport.auth_call_oauth_api(
        authorization="access-token",
        provider="github",
        endpoint="/user/repos",
        method="POST",
        body=MappingProxyType({"filters": MappingProxyType({"visibility": "private"})}),
    )

    assert json.loads(requests[0].content) == {
        "endpoint": "/user/repos",
        "method": "POST",
        "body": {"filters": {"visibility": "private"}},
    }


def test_generated_transport_deletes_all_other_sessions() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(204)

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_delete_all_my_sessions(authorization="access-token")

    assert response.status_code == 204
    assert requests[0].method == "DELETE"
    assert requests[0].url.path == "/auth/user/sessions"
    assert requests[0].headers["authorization"] == "Bearer access-token"


def test_generated_transport_deletes_one_session() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(204)

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_delete_my_session(
        authorization="access-token",
        session_id="00000000-0000-4000-8000-000000000099",
    )

    assert response.status_code == 204
    assert requests[0].method == "DELETE"
    assert (
        requests[0].url.path
        == "/auth/user/sessions/00000000-0000-4000-8000-000000000099"
    )
    assert requests[0].headers["authorization"] == "Bearer access-token"


def test_generated_transport_requests_a_password_reset_with_the_anon_key() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "message": "If the email exists, a password reset link has been sent."
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_forgot_password(
        authorization="anon-key",
        email="user@example.com",
    )

    assert response.status_code == 200
    assert response.payload == {
        "message": "If the email exists, a password reset link has been sent."
    }
    assert requests[0].method == "POST"
    assert requests[0].url.path == "/auth/forgot-password"
    assert requests[0].headers["authorization"] == "Bearer anon-key"
    assert json.loads(requests[0].content) == {"email": "user@example.com"}


def test_generated_transport_accepts_a_malformed_password_reset_success_body() -> None:
    def handle(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            content=b"not-json",
            headers={"Content-Type": "application/json"},
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_forgot_password(
        authorization="anon-key",
        email="user@example.com",
    )

    assert response.status_code == 200
    assert response.payload is None


def test_generated_transport_preserves_a_malformed_rate_limit_response() -> None:
    def handle(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            429,
            content=b"not-json",
            headers={"Content-Type": "application/json", "Retry-After": "17"},
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_forgot_password(
        authorization="anon-key",
        email="user@example.com",
    )

    with pytest.raises(RateLimitedError) as caught:
        response_payload(response, 200)

    assert caught.value.status == 429
    assert caught.value.retry_after == 17


def test_generated_transport_resets_a_password_with_the_anon_key() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"message": "Password reset successful"})

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_reset_password(
        authorization="anon-key",
        token="recovery-token",
        new_password="new-secret",
    )

    assert response.status_code == 200
    assert requests[0].method == "POST"
    assert requests[0].url.path == "/auth/reset-password"
    assert requests[0].headers["authorization"] == "Bearer anon-key"
    assert json.loads(requests[0].content) == {
        "token": "recovery-token",
        "new_password": "new-secret",
    }


def test_generated_transport_confirms_an_email_with_the_anon_key() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"message": "Email confirmed successfully"})

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_confirm_email(
        authorization="anon-key",
        token="confirmation-token",
    )

    assert response.status_code == 200
    assert requests[0].method == "POST"
    assert requests[0].url.path == "/auth/confirm"
    assert requests[0].headers["authorization"] == "Bearer anon-key"
    assert json.loads(requests[0].content) == {"token": "confirmation-token"}


def test_generated_transport_resends_confirmation_with_the_anon_key() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={})

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_resend_confirmation(
        authorization="anon-key",
        email="user@example.com",
    )

    assert response.status_code == 200
    assert requests[0].method == "POST"
    assert requests[0].url.path == "/auth/resend-confirmation"
    assert requests[0].headers["authorization"] == "Bearer anon-key"
    assert json.loads(requests[0].content) == {"email": "user@example.com"}


def test_generated_transport_gets_the_current_user_with_the_access_token() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "user": {
                    "id": "00000000-0000-4000-8000-000000000010",
                    "email": "user@example.com",
                    "status": "active",
                    "email_confirmed": True,
                    "user_metadata": {"display_name": "Ada"},
                    "created_at": "2026-08-26T12:00:00Z",
                    "updated_at": "2026-08-26T12:00:00Z",
                }
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_get_user(authorization="access-token")

    assert response.status_code == 200
    assert isinstance(response.payload, AuthGetUserResponse200)
    assert not isinstance(response.payload.user, Unset)
    assert response.payload.user.email == "user@example.com"
    assert requests[0].method == "GET"
    assert requests[0].url.path == "/auth/user"
    assert requests[0].headers["authorization"] == "Bearer access-token"


def test_generated_transport_normalizes_malformed_current_user_json() -> None:
    def handle(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            content=b"not-json",
            headers={"Content-Type": "text/html"},
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    with pytest.raises(AuthenticationError, match="Expected a complete user profile"):
        transport.auth_get_user(authorization="access-token")


def test_generated_transport_updates_the_current_user() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "user": {
                    "id": "00000000-0000-4000-8000-000000000010",
                    "email": "user@example.com",
                    "status": "active",
                    "user_metadata": {"display_name": "Grace"},
                }
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_update_user(
        authorization="access-token",
        password="new-secret",
        metadata={"display_name": "Grace", "avatar": None},
    )

    assert response.status_code == 200
    assert isinstance(response.payload, AuthUpdateUserResponse200)
    assert not isinstance(response.payload.user, Unset)
    assert response.payload.user.email == "user@example.com"
    assert requests[0].method == "PUT"
    assert requests[0].url.path == "/auth/user"
    assert requests[0].headers["authorization"] == "Bearer access-token"
    assert json.loads(requests[0].content) == {
        "password": "new-secret",
        "user_metadata": {"display_name": "Grace", "avatar": None},
    }


def test_generated_transport_omits_absent_update_fields() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "user": {
                    "id": "00000000-0000-4000-8000-000000000010",
                    "email": "user@example.com",
                    "status": "active",
                }
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    transport.auth_update_user(
        authorization="access-token",
        password=None,
        metadata=None,
    )

    assert json.loads(requests[0].content) == {}


def test_generated_transport_logs_out_with_the_anon_key_and_refresh_token() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(204)

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.auth_logout(
        authorization="anon-key",
        refresh_token="refresh-1",
    )

    assert response.status_code == 204
    assert requests[0].method == "POST"
    assert requests[0].url.path == "/auth/logout"
    assert requests[0].headers["authorization"] == "Bearer anon-key"
    assert json.loads(requests[0].content) == {"refresh_token": "refresh-1"}


def test_generated_transport_inserts_a_database_row() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={"data": [{"id": "item-1", "name": "Volcano"}], "count": 1},
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.query_database_insert(
        authorization="access-token",
        database_name="main",
        body={"table": "items", "values": {"name": "Volcano"}},
    )

    assert response.payload == {
        "data": [{"id": "item-1", "name": "Volcano"}],
        "count": 1,
    }
    assert requests[0].method == "POST"
    assert requests[0].url.path == "/databases/main/query/insert"
    assert requests[0].headers["authorization"] == "Bearer access-token"
    assert json.loads(requests[0].content) == {
        "table": "items",
        "values": {"name": "Volcano"},
    }


def test_generated_transport_updates_filtered_database_rows() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={"data": [{"id": "item-1", "status": "published"}], "count": 1},
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.query_database_update(
        authorization="access-token",
        database_name="main",
        body={
            "table": "items",
            "values": {"status": "published"},
            "filters": [{"column": "id", "operator": "eq", "value": "item-1"}],
        },
    )

    assert response.payload == {
        "data": [{"id": "item-1", "status": "published"}],
        "count": 1,
    }
    assert requests[0].method == "POST"
    assert requests[0].url.path == "/databases/main/query/update"
    assert requests[0].headers["authorization"] == "Bearer access-token"
    assert json.loads(requests[0].content) == {
        "table": "items",
        "values": {"status": "published"},
        "filters": [{"column": "id", "operator": "eq", "value": "item-1"}],
    }


def test_generated_transport_deletes_filtered_database_rows() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"data": [{"id": "item-1"}], "count": 1})

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.query_database_delete(
        authorization="access-token",
        database_name="main",
        body={
            "table": "items",
            "filters": [{"column": "id", "operator": "eq", "value": "item-1"}],
        },
    )

    assert response.payload == {"data": [{"id": "item-1"}], "count": 1}
    assert requests[0].method == "POST"
    assert requests[0].url.path == "/databases/main/query/delete"
    assert requests[0].headers["authorization"] == "Bearer access-token"
    assert json.loads(requests[0].content) == {
        "table": "items",
        "filters": [{"column": "id", "operator": "eq", "value": "item-1"}],
    }


def test_generated_transport_calls_the_seven_openapi_operations() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        path = request.url.path
        if path in {"/auth/signin", "/auth/refresh"}:
            refreshing = path == "/auth/refresh"
            return httpx.Response(
                200,
                json={
                    "access_token": (
                        "refreshed-access-token" if refreshing else "access-token"
                    ),
                    "refresh_token": (
                        "refreshed-refresh-token" if refreshing else "refresh-token"
                    ),
                    "user": {
                        "id": "00000000-0000-4000-8000-000000000010",
                        "email": "user@example.com",
                        "status": "active",
                        "email_confirmed": True,
                        "created_at": "2026-08-26T12:00:00Z",
                        "updated_at": "2026-08-26T12:00:00Z",
                    },
                    "expires_in": 3600,
                    "token_type": "bearer",
                },
            )
        if path == "/databases/main/query/select":
            return httpx.Response(200, json={"data": [{"slug": "a"}], "count": 1})
        if request.method == "POST" and path == "/storage/assets/a.txt":
            return httpx.Response(
                201,
                json={
                    "id": "00000000-0000-4000-8000-000000000020",
                    "bucket_id": "00000000-0000-4000-8000-000000000030",
                    "name": "a.txt",
                    "is_public": False,
                    "size": 5,
                    "mime_type": "application/octet-stream",
                    "metadata": {},
                    "owner_id": "00000000-0000-4000-8000-000000000010",
                    "created_at": "2026-08-26T12:00:00Z",
                    "updated_at": "2026-08-26T12:00:00Z",
                },
            )
        if request.method == "GET" and path in {
            "/storage/assets/a.txt",
            "/storage/assets",
        }:
            if path == "/storage/assets/a.txt":
                response = httpx.Response(200, content=b"hello")
            else:
                assert dict(request.url.params) == {
                    "prefix": "avatars",
                    "limit": "25",
                    "cursor": "cursor-1",
                }
                response = httpx.Response(
                    200,
                    json={"objects": [], "next_cursor": "cursor-2"},
                )
            return response
        if request.method == "POST" and path == "/locks/build/lease":
            return httpx.Response(
                201,
                json={
                    "key": "build",
                    "expires_at": "2026-08-26T12:00:30Z",
                    "fencing_token": 7,
                },
            )
        if request.method == "DELETE" and path == "/locks/build/lease":
            return httpx.Response(204)
        message = f"unexpected request: {request.method} {path}"
        raise AssertionError(message)

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    auth = transport.auth_signin(
        authorization="anon-key",
        email="user@example.com",
        password="secret",
    )
    refresh = transport.auth_refresh(
        authorization="anon-key",
        refresh_token="refresh-token",
    )
    query = transport.query_database_select(
        authorization="access-token",
        database_name="main",
        body={
            "table": "items",
            "select": ["*"],
            "filters": [{"column": "slug", "operator": "eq", "value": "a"}],
        },
    )
    upload = transport.upload_storage_object(
        authorization="access-token",
        bucket_name="assets",
        path="a.txt",
        data=b"hello",
    )
    download = transport.download_storage_object(
        authorization="access-token",
        bucket_name="assets",
        path="a.txt",
        byte_range="bytes=0-4",
    )
    listed = transport.list_storage_objects(
        authorization="access-token",
        bucket_name="assets",
        prefix="avatars",
        limit=25,
        cursor="cursor-1",
    )
    acquire = transport.acquire_project_lock(
        authorization="service-key",
        key="build",
        ttl=30,
        token="00000000-0000-4000-8000-000000000001",
    )
    release = transport.release_project_lock(
        authorization="service-key",
        key="build",
        token="00000000-0000-4000-8000-000000000001",
    )

    assert auth.payload["user"]["id"] == "00000000-0000-4000-8000-000000000010"
    assert refresh.payload["access_token"] == "refreshed-access-token"
    assert query.payload == {"data": [{"slug": "a"}], "count": 1}
    assert upload.payload["name"] == "a.txt"
    assert download.content == b"hello"
    assert listed.payload == {"objects": [], "next_cursor": "cursor-2"}
    assert acquire.payload["fencing_token"] == 7
    assert release.status_code == 204
    assert [request.method for request in requests] == [
        "POST",
        "POST",
        "POST",
        "POST",
        "GET",
        "GET",
        "POST",
        "DELETE",
    ]
    assert [request.headers["authorization"] for request in requests] == [
        "Bearer anon-key",
        "Bearer anon-key",
        "Bearer access-token",
        "Bearer access-token",
        "Bearer access-token",
        "Bearer access-token",
        "Bearer service-key",
        "Bearer service-key",
    ]
    assert json.loads(requests[0].content) == {
        "email": "user@example.com",
        "password": "secret",
    }
    assert json.loads(requests[1].content) == {
        "refresh_token": "refresh-token",
    }
    assert json.loads(requests[2].content) == {
        "table": "items",
        "select": ["*"],
        "filters": [{"column": "slug", "operator": "eq", "value": "a"}],
    }
    assert b"hello" in requests[3].content
    assert requests[4].headers["range"] == "bytes=0-4"
    assert json.loads(requests[6].content) == {"ttl_seconds": 30}
    assert requests[6].headers["x-volcano-lock-token"] == (
        "00000000-0000-4000-8000-000000000001"
    )
    assert requests[7].headers["x-volcano-lock-token"] == (
        "00000000-0000-4000-8000-000000000001"
    )


def test_generated_transport_deletes_a_storage_object() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200)

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.delete_storage_object(
        authorization="access-token",
        bucket_name="assets",
        path="archive/a.txt",
    )

    assert response.status_code == 200
    assert len(requests) == 1
    assert requests[0].method == "DELETE"
    assert requests[0].url.path == "/storage/assets/archive/a.txt"
    assert requests[0].headers["authorization"] == "Bearer access-token"


def test_generated_transport_creates_an_upload_session_with_json() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            201,
            json={
                "session_id": "session-123",
                "part_size": 8_388_608,
                "total_parts": 3,
                "expires_at": "2026-09-09T12:00:00Z",
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.create_upload_session(
        authorization="access-token",
        bucket_name="assets",
        request=StorageUploadSessionRequest(
            path="videos/demo clip.mp4",
            content_type="video/mp4",
            total_size=20_000_000,
            part_size=8_388_608,
        ),
    )

    assert response.status_code == 201
    assert response.payload["session_id"] == "session-123"
    assert len(requests) == 1
    assert requests[0].url.path == "/storage/assets/videos/demo clip.mp4"
    assert requests[0].headers["authorization"] == "Bearer access-token"
    assert requests[0].headers["content-type"] == "application/json"
    assert json.loads(requests[0].content) == {
        "object_path": "videos/demo clip.mp4",
        "content_type": "video/mp4",
        "total_size": 20_000_000,
        "part_size": 8_388_608,
    }


def test_generated_transport_uploads_a_binary_part() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={"part_number": 2, "etag": "etag-part-2", "size": 6},
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.upload_part(
        authorization="access-token",
        bucket_name="assets",
        request=StorageUploadPartRequest(
            path="videos/demo clip.mp4",
            session_id="session-123",
            part_number=2,
            data=b"chunk\x00",
        ),
    )

    assert response.payload == {
        "part_number": 2,
        "etag": "etag-part-2",
        "size": 6,
    }
    assert len(requests) == 1
    assert requests[0].method == "PUT"
    assert requests[0].url.path == "/storage/assets/videos/demo clip.mp4"
    assert requests[0].headers["authorization"] == "Bearer access-token"
    assert requests[0].headers["content-type"] == "application/octet-stream"
    assert requests[0].headers["x-upload-session"] == "session-123"
    assert requests[0].headers["x-part-number"] == "2"
    assert requests[0].content == b"chunk\x00"


def test_generated_transport_completes_an_upload_session() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "object": {
                    "id": "00000000-0000-4000-8000-000000000020",
                    "bucket_id": "00000000-0000-4000-8000-000000000030",
                    "name": "videos/demo clip.mp4",
                    "size": 20_000_000,
                    "mime_type": "video/mp4",
                    "is_public": False,
                }
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.complete_upload_session(
        authorization="access-token",
        bucket_name="assets",
        request=StorageUploadSessionReference(
            path="videos/demo clip.mp4",
            session_id="session-123",
        ),
    )

    assert response.payload["object"]["name"] == "videos/demo clip.mp4"
    assert len(requests) == 1
    assert requests[0].method == "POST"
    assert requests[0].url.path == "/storage/assets/videos/demo clip.mp4"
    assert requests[0].headers["authorization"] == "Bearer access-token"
    assert requests[0].headers["x-upload-session"] == "session-123"
    assert requests[0].headers["x-upload-complete"] == "true"


def test_generated_transport_gets_upload_session_status_as_json() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            headers={"Content-Type": "application/json"},
            json={
                "session_id": "session-123",
                "status": "uploading",
                "path": "videos/demo clip.mp4",
                "content_type": "video/mp4",
                "total_size": 20_000_000,
                "part_size": 8_388_608,
                "total_parts": 3,
                "parts_uploaded": 1,
                "bytes_uploaded": 8_388_608,
                "parts": [],
                "expires_at": "2026-09-09T12:00:00Z",
                "created_at": "2026-09-02T12:00:00Z",
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.get_upload_session(
        authorization="access-token",
        bucket_name="assets",
        request=StorageUploadSessionReference(
            path="videos/demo clip.mp4",
            session_id="session-123",
        ),
    )

    assert response.payload["session_id"] == "session-123"
    assert len(requests) == 1
    assert requests[0].method == "GET"
    assert requests[0].url.path == "/storage/assets/videos/demo clip.mp4"
    assert requests[0].headers["authorization"] == "Bearer access-token"
    assert requests[0].headers["x-upload-session"] == "session-123"


def test_generated_transport_aborts_an_upload_session() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"message": "upload session aborted"})

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.abort_upload_session(
        authorization="access-token",
        bucket_name="assets",
        request=StorageUploadSessionReference(
            path="videos/demo clip.mp4",
            session_id="session-123",
        ),
    )

    assert response.status_code == 200
    assert len(requests) == 1
    assert requests[0].method == "DELETE"
    assert requests[0].url.path == "/storage/assets/videos/demo clip.mp4"
    assert requests[0].headers["authorization"] == "Bearer access-token"
    assert requests[0].headers["x-upload-session"] == "session-123"


def test_generated_transport_gets_project_lock_state() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "held": True,
                "expires_at": "2026-08-26T12:00:30Z",
                "fencing_token": 7,
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.get_project_lock(
        authorization="service-key",
        key="build:queue",
    )

    assert response.payload["held"] is True
    assert len(requests) == 1
    assert requests[0].method == "GET"
    assert requests[0].url.path == "/locks/build:queue"
    assert requests[0].headers["authorization"] == "Bearer service-key"
    assert requests[0].headers["x-volcano-request-id"]


def test_generated_transport_moves_a_storage_object() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "id": "00000000-0000-4000-8000-000000000020",
                "bucket_id": "00000000-0000-4000-8000-000000000030",
                "name": "published/a.txt",
                "size": 5,
                "mime_type": "text/plain",
                "is_public": False,
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.move_storage_object(
        authorization="access-token",
        bucket_name="assets",
        from_path="drafts/a.txt",
        to_path="published/a.txt",
    )

    assert response.status_code == 200
    assert len(requests) == 1
    assert requests[0].url.path == "/storage/assets/move"
    assert json.loads(requests[0].content) == {
        "from": "drafts/a.txt",
        "to": "published/a.txt",
    }


def test_generated_transport_copies_a_storage_object() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            201,
            json={
                "id": "00000000-0000-4000-8000-000000000021",
                "bucket_id": "00000000-0000-4000-8000-000000000030",
                "name": "drafts/a.txt",
                "size": 5,
                "mime_type": "text/plain",
                "is_public": False,
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )
    response = transport.copy_storage_object(
        authorization="access-token",
        bucket_name="assets",
        from_path="templates/a.txt",
        to_path="drafts/a.txt",
    )

    assert response.status_code == 201
    assert requests[0].url.path == "/storage/assets/copy"
    assert json.loads(requests[0].content) == {
        "from": "templates/a.txt",
        "to": "drafts/a.txt",
    }


def test_generated_transport_updates_storage_object_visibility() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "id": "00000000-0000-4000-8000-000000000020",
                "bucket_id": "00000000-0000-4000-8000-000000000030",
                "name": "avatars/a.png",
                "size": 5,
                "mime_type": "image/png",
                "is_public": True,
                "public_url": "https://api.test.volcano.dev/public/project/assets/avatars/a.png",
            },
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.update_storage_object_visibility(
        authorization="access-token",
        bucket_name="assets",
        path="avatars/a.png",
        is_public=True,
    )

    assert response.status_code == 200
    assert requests[0].method == "PATCH"
    assert requests[0].url.path == "/storage/assets/avatars/a.png/visibility"
    assert json.loads(requests[0].content) == {"is_public": True}
