from __future__ import annotations

import json

import httpx

from volcano_sdk._transport import GeneratedTransport


def test_generated_transport_calls_the_six_openapi_operations() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        path = request.url.path
        if path == "/auth/signin":
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
        raise AssertionError(f"unexpected request: {request.method} {path}")

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

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

    assert auth.payload["user"]["id"] == "00000000-0000-4000-8000-000000000010"
    assert query.payload == {"data": [{"slug": "a"}], "count": 1}
    assert upload.payload["name"] == "a.txt"
    assert download.content == b"hello"
    assert acquire.payload["fencing_token"] == 7
    assert release.status_code == 204
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
