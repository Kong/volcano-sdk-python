from __future__ import annotations

import json

import httpx
import pytest

from volcano_sdk import AuthenticationError, User, VolcanoClient
from volcano_sdk._transport import GeneratedTransport, TransportResponse


def _recording_transport() -> tuple[GeneratedTransport, list[httpx.Request]]:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(418)

    return (
        GeneratedTransport(
            api_url="https://api.test.volcano.dev",
            httpx_transport=httpx.MockTransport(handle),
        ),
        requests,
    )


def test_generated_transport_normalizes_malformed_signup_payloads() -> None:
    def handle(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(201, json={"message": "created"})

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )
    client = VolcanoClient(anon_key="anon-key", _transport=transport)

    with pytest.raises(AuthenticationError, match="Invalid authentication response"):
        client.auth.sign_up(email="user@example.com", password="secret")


def _auth_response() -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "access_token": "access-token",
            "refresh_token": "refresh-token",
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


def _upload_response() -> httpx.Response:
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


def _successful_response(request: httpx.Request) -> httpx.Response:
    response_by_operation = {
        ("POST", "/auth/signin"): _auth_response(),
        ("POST", "/databases/main/query/select"): httpx.Response(
            200, json={"data": [{"slug": "a"}], "count": 1}
        ),
        ("POST", "/storage/assets/a.txt"): _upload_response(),
        ("GET", "/storage/assets/a.txt"): httpx.Response(200, content=b"hello"),
        ("POST", "/locks/build/lease"): httpx.Response(
            201,
            json={
                "key": "build",
                "expires_at": "2026-08-26T12:00:30Z",
                "fencing_token": 7,
            },
        ),
        ("DELETE", "/locks/build/lease"): httpx.Response(204),
    }
    response = response_by_operation.get((request.method, request.url.path))
    if response is None:
        message = f"unexpected request: {request.method} {request.url.path}"
        raise AssertionError(message)
    return response


def _successful_transport() -> tuple[GeneratedTransport, list[httpx.Request]]:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return _successful_response(request)

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )
    return transport, requests


def _call_six_operations(
    transport: GeneratedTransport,
) -> tuple[TransportResponse, ...]:
    auth = transport.auth_signin(
        authorization="anon-key",
        email="user@example.com",
        password="secret",
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
    return auth, query, upload, download, acquire, release


def _assert_request_metadata(requests: list[httpx.Request]) -> None:
    assert [request.method for request in requests] == [
        "POST",
        "POST",
        "POST",
        "GET",
        "POST",
        "DELETE",
    ]
    assert [request.headers["authorization"] for request in requests] == [
        "Bearer anon-key",
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
        "table": "items",
        "select": ["*"],
        "filters": [{"column": "slug", "operator": "eq", "value": "a"}],
    }
    assert b"hello" in requests[2].content
    assert json.loads(requests[4].content) == {"ttl_seconds": 30}
    assert requests[4].headers["x-volcano-lock-token"] == (
        "00000000-0000-4000-8000-000000000001"
    )
    assert requests[5].headers["x-volcano-lock-token"] == (
        "00000000-0000-4000-8000-000000000001"
    )


def test_generated_transport_calls_the_six_openapi_operations() -> None:
    transport, requests = _successful_transport()
    auth, query, upload, download, acquire, release = _call_six_operations(transport)

    assert auth.payload["user"]["id"] == "00000000-0000-4000-8000-000000000010"
    assert query.payload == {"data": [{"slug": "a"}], "count": 1}
    assert upload.payload["name"] == "a.txt"
    assert download.content == b"hello"
    assert acquire.payload["fencing_token"] == 7
    assert release.status_code == 204
    _assert_request_metadata(requests)


def test_generated_transport_calls_session_core_operations() -> None:
    transport, requests = _recording_transport()

    transport.auth_signup(
        authorization="anon-key",
        email="user@example.com",
        password="signup-password",
        user_metadata={"display_name": "User"},
    )
    transport.auth_signin(
        authorization="anon-key",
        email="user@example.com",
        password="signin-password",
    )
    transport.auth_refresh(
        authorization="anon-key",
        refresh_token="refresh-token",
    )
    transport.auth_logout(
        authorization="anon-key",
        refresh_token="refresh-token",
    )
    transport.auth_get_user(authorization="access-token")
    transport.auth_update_user(
        authorization="access-token",
        password="new-password",
        user_metadata={"display_name": "Updated"},
    )

    assert [(request.method, request.url.path) for request in requests] == [
        ("POST", "/auth/signup"),
        ("POST", "/auth/signin"),
        ("POST", "/auth/refresh"),
        ("POST", "/auth/logout"),
        ("GET", "/auth/user"),
        ("PUT", "/auth/user"),
    ]
    assert [request.headers["authorization"] for request in requests] == [
        "Bearer anon-key",
        "Bearer anon-key",
        "Bearer anon-key",
        "Bearer anon-key",
        "Bearer access-token",
        "Bearer access-token",
    ]
    bodies = [
        json.loads(request.content) if request.content else None for request in requests
    ]
    assert bodies == [
        {
            "email": "user@example.com",
            "password": "signup-password",
            "user_metadata": {"display_name": "User"},
        },
        {"email": "user@example.com", "password": "signin-password"},
        {"refresh_token": "refresh-token"},
        {"refresh_token": "refresh-token"},
        None,
        {
            "password": "new-password",
            "user_metadata": {"display_name": "Updated"},
        },
    ]


def test_generated_transport_thaws_frozen_user_metadata() -> None:
    transport, requests = _recording_transport()
    user = User(
        id="user-123",
        email="user@example.com",
        user_metadata={"nested": [{"value": "kept"}]},
    )

    transport.auth_update_user(
        authorization="access-token",
        user_metadata=user.user_metadata,
    )

    assert json.loads(requests[0].content) == {
        "user_metadata": {"nested": [{"value": "kept"}]}
    }


def test_generated_transport_calls_account_operations() -> None:
    transport, requests = _recording_transport()

    transport.auth_signup_anonymous(
        authorization="anon-key",
        user_metadata={"display_name": "Guest"},
    )
    transport.auth_convert_anonymous(
        authorization="access-token",
        email="user@example.com",
        password="secret",
        user_metadata={"plan": "developer"},
    )
    transport.auth_confirm_email(
        authorization="anon-key",
        token="confirmation-token",
    )
    transport.auth_resend_confirmation(
        authorization="anon-key",
        email="user@example.com",
    )
    transport.auth_forgot_password(
        authorization="anon-key",
        email="user@example.com",
    )
    transport.auth_reset_password(
        authorization="anon-key",
        token="recovery-token",
        new_password="new-password",
    )
    transport.auth_request_email_change(
        authorization="access-token",
        new_email="new@example.com",
    )
    transport.auth_confirm_email_change(
        authorization="access-token",
        email_change_token="email-change-token",
    )
    transport.auth_cancel_email_change(authorization="access-token")

    assert [(request.method, request.url.path) for request in requests] == [
        ("POST", "/auth/signup-anonymous"),
        ("POST", "/auth/user/convert-anonymous"),
        ("POST", "/auth/confirm"),
        ("POST", "/auth/resend-confirmation"),
        ("POST", "/auth/forgot-password"),
        ("POST", "/auth/reset-password"),
        ("POST", "/auth/user/change-email"),
        ("POST", "/auth/user/confirm-email-change"),
        ("DELETE", "/auth/user/cancel-email-change"),
    ]
    assert [request.headers["authorization"] for request in requests] == [
        "Bearer anon-key",
        "Bearer access-token",
        "Bearer anon-key",
        "Bearer anon-key",
        "Bearer anon-key",
        "Bearer anon-key",
        "Bearer access-token",
        "Bearer access-token",
        "Bearer access-token",
    ]
    bodies = [
        json.loads(request.content) if request.content else None for request in requests
    ]
    assert bodies == [
        {"user_metadata": {"display_name": "Guest"}},
        {
            "email": "user@example.com",
            "password": "secret",
            "user_metadata": {"plan": "developer"},
        },
        {"token": "confirmation-token"},
        {"email": "user@example.com"},
        {"email": "user@example.com"},
        {"token": "recovery-token", "new_password": "new-password"},
        {"new_email": "new@example.com"},
        {"email_change_token": "email-change-token"},
        None,
    ]


def test_generated_transport_calls_oauth_operations() -> None:
    transport, requests = _recording_transport()

    transport.auth_oauth_authorize(
        authorization="anon-key",
        provider="github",
        redirect_url="https://app.example/callback",
        state="oauth-state",
    )
    transport.auth_oauth_exchange(
        authorization="anon-key",
        code="oauth-code",
        redirect_url="https://app.example/callback",
    )
    transport.auth_link_oauth_provider(
        authorization="access-token",
        provider="google",
        redirect_url="https://app.example/link-callback",
        state="link-state",
    )
    transport.auth_unlink_oauth_provider(
        authorization="access-token",
        provider="google",
    )
    transport.auth_list_oauth_providers(authorization="access-token")
    transport.refresh_oauth_provider_token(
        authorization="access-token",
        provider="github",
    )
    transport.get_oauth_provider_token(
        authorization="access-token",
        provider="github",
    )
    transport.call_oauth_provider_api(
        authorization="access-token",
        provider="github",
        endpoint="/user/repos",
        method="POST",
        body={"visibility": "private"},
    )

    assert [(request.method, request.url.path) for request in requests] == [
        ("GET", "/auth/oauth/github/authorize"),
        ("POST", "/auth/oauth/exchange"),
        ("POST", "/auth/oauth/google/link"),
        ("DELETE", "/auth/oauth/google/unlink"),
        ("GET", "/auth/oauth/providers"),
        ("POST", "/auth/oauth/github/refresh-token"),
        ("GET", "/auth/oauth/github/token"),
        ("POST", "/auth/oauth/github/call-api"),
    ]
    assert [request.headers["authorization"] for request in requests] == [
        "Bearer anon-key",
        "Bearer anon-key",
        "Bearer access-token",
        "Bearer access-token",
        "Bearer access-token",
        "Bearer access-token",
        "Bearer access-token",
        "Bearer access-token",
    ]
    assert dict(requests[0].url.params) == {
        "anon_key": "anon-key",
        "redirect_url": "https://app.example/callback",
        "client_state": "oauth-state",
        "response_mode": "code",
    }
    assert json.loads(requests[1].content) == {
        "code": "oauth-code",
        "redirect_url": "https://app.example/callback",
    }
    assert dict(requests[2].url.params) == {
        "redirect_url": "https://app.example/link-callback",
        "client_state": "link-state",
        "response_mode": "code",
    }
    assert json.loads(requests[7].content) == {
        "endpoint": "/user/repos",
        "method": "POST",
        "body": {"visibility": "private"},
    }


def test_generated_transport_preserves_provider_api_array_responses() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json=[{"id": 1}, {"id": 2}])

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    response = transport.call_oauth_provider_api(
        authorization="access-token",
        provider="github",
        endpoint="/user/repos",
    )

    assert response.payload == [{"id": 1}, {"id": 2}]
    assert len(requests) == 1
    assert requests[0].headers["authorization"] == "Bearer access-token"


def test_generated_transport_thaws_provider_api_request_metadata() -> None:
    transport, requests = _recording_transport()
    user = User(
        id="user-123",
        email="user@example.com",
        user_metadata={"nested": [{"enabled": True}]},
    )

    transport.call_oauth_provider_api(
        authorization="access-token",
        provider="github",
        endpoint="/user",
        method="POST",
        body={"metadata": user.user_metadata},
    )

    assert json.loads(requests[0].content)["body"] == {
        "metadata": {"nested": [{"enabled": True}]}
    }


def test_generated_transport_calls_device_session_operations() -> None:
    transport, requests = _recording_transport()

    transport.auth_get_my_sessions(
        authorization="access-token",
        limit=10,
        sort="created_at",
        status="active",
        cursor="next-page",
        offset=20,
    )
    transport.auth_delete_my_session(
        authorization="access-token",
        session_id="00000000-0000-4000-8000-000000000040",
    )
    transport.auth_delete_all_my_sessions(authorization="access-token")

    assert [(request.method, request.url.path) for request in requests] == [
        ("GET", "/auth/user/sessions"),
        (
            "DELETE",
            "/auth/user/sessions/00000000-0000-4000-8000-000000000040",
        ),
        ("DELETE", "/auth/user/sessions"),
    ]
    assert dict(requests[0].url.params) == {
        "limit": "10",
        "sort": "created_at",
        "status": "active",
        "cursor": "next-page",
        "offset": "20",
    }
    assert [request.headers["authorization"] for request in requests] == [
        "Bearer access-token",
        "Bearer access-token",
        "Bearer access-token",
    ]
