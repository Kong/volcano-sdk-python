from __future__ import annotations

import json

import httpx
import pytest

from volcano_sdk import AuthenticationError
from volcano_sdk._generated.models.auth_get_user_response_200 import (
    AuthGetUserResponse200,
)
from volcano_sdk._generated.models.auth_update_user_response_200 import (
    AuthUpdateUserResponse200,
)
from volcano_sdk._generated.types import Unset
from volcano_sdk._transport import GeneratedTransport


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
        if request.method == "GET" and path == "/storage/assets/a.txt":
            return httpx.Response(200, content=b"hello")
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
    assert acquire.payload["fencing_token"] == 7
    assert release.status_code == 204
    assert [request.method for request in requests] == [
        "POST",
        "POST",
        "POST",
        "POST",
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
    assert json.loads(requests[5].content) == {"ttl_seconds": 30}
    assert requests[5].headers["x-volcano-lock-token"] == (
        "00000000-0000-4000-8000-000000000001"
    )
    assert requests[6].headers["x-volcano-lock-token"] == (
        "00000000-0000-4000-8000-000000000001"
    )
