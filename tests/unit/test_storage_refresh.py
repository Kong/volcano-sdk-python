from __future__ import annotations

from io import BytesIO
from typing import TYPE_CHECKING

import httpx
import pytest

from volcano_sdk import (
    AuthenticationError,
    Session,
    SessionChangedError,
    TransportError,
    VolcanoClient,
    VolcanoError,
)
from volcano_sdk._transport import GeneratedTransport

if TYPE_CHECKING:
    from collections.abc import Callable

OPERATIONS = (
    "upload",
    "download",
    "range",
    "list",
    "remove",
    "move",
    "copy",
    "visibility",
    "create",
    "part",
    "complete",
    "status",
    "abort",
)
USER_ID = "00000000-0000-4000-8000-000000000001"


def make_client(handler: Callable[[httpx.Request], httpx.Response]) -> VolcanoClient:
    client = VolcanoClient(
        anon_key="anon",
        _transport=GeneratedTransport(
            api_url="https://api.test.volcano.dev",
            httpx_transport=httpx.MockTransport(handler),
        ),
    )
    client.auth.set_session(Session("old-access", "old-refresh", USER_ID))
    return client


def storage_operation(client: VolcanoClient, operation: str) -> object:
    bucket = client.storage.from_("assets")
    operations: dict[str, Callable[[], object]] = {
        "upload": lambda: bucket.upload("file.bin", BytesIO(b"hello\x00\xff")),
        "download": lambda: bucket.download("file.bin"),
        "range": lambda: bucket.download("file.bin", byte_range="bytes=1-3"),
        "list": lambda: bucket.list("file", limit=2, cursor="next"),
        "remove": lambda: bucket.remove("file.bin"),
        "move": lambda: bucket.move("file.bin", "moved.bin"),
        "copy": lambda: bucket.copy("file.bin", "copy.bin"),
        "visibility": lambda: bucket.update_visibility("file.bin", is_public=True),
        "create": lambda: bucket.create_upload_session("file.bin", total_size=7),
        "part": lambda: bucket.upload_part(
            "file.bin", session_id="upload", part_number=1, data=b"hello\x00\xff"
        ),
        "complete": lambda: bucket.complete_upload_session(
            "file.bin", session_id="upload"
        ),
        "status": lambda: bucket.get_upload_session("file.bin", session_id="upload"),
        "abort": lambda: bucket.abort_upload_session("file.bin", session_id="upload"),
    }
    return operations[operation]()


def refresh_response() -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "access_token": "new-access",
            "refresh_token": "new-refresh",
            "token_type": "bearer",
            "expires_in": 3600,
            "user": {"id": USER_ID, "email": "user@example.com", "status": "active"},
        },
    )


def success_response(operation: str) -> httpx.Response:
    obj = {
        "id": "00000000-0000-4000-8000-000000000020",
        "bucket_id": "00000000-0000-4000-8000-000000000030",
        "name": "file.bin",
        "size": 7,
        "mime_type": "application/octet-stream",
        "is_public": True,
        "created_at": "2026-09-17T00:00:00Z",
        "updated_at": "2026-09-17T00:00:00Z",
    }
    payload: object = obj
    if operation in {"create", "status"}:
        payload = {
            "session_id": "upload",
            "part_size": 7,
            "total_parts": 1,
            "expires_at": "2026-09-18T00:00:00Z",
            "created_at": "2026-09-17T00:00:00Z",
            "status": "uploading",
            "path": "file.bin",
            "content_type": "application/octet-stream",
            "total_size": 7,
            "parts_uploaded": 0,
            "bytes_uploaded": 0,
            "parts": [],
        }
    elif operation == "part":
        payload = {"part_number": 1, "etag": "part-1", "size": 7}
    elif operation == "complete":
        payload = {"object": obj}
    elif operation == "list":
        payload = {"objects": [obj], "next_cursor": ""}
    elif operation in {"remove", "abort"}:
        payload = {"message": "deleted"}
    if operation in {"download", "range"}:
        return httpx.Response(206 if operation == "range" else 200, content=b"ell")
    return httpx.Response(
        201 if operation in {"upload", "create", "copy"} else 200, json=payload
    )


@pytest.mark.parametrize("operation", OPERATIONS)
@pytest.mark.parametrize("rejection", [b'{"error":"expired"}', b"", b"not json"])
def test_storage_refreshes_once_and_replays_the_request(
    operation: str, rejection: bytes
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/refresh":
            return refresh_response()
        if request.headers["authorization"] == "Bearer old-access":
            return httpx.Response(401, content=rejection)
        return success_response(operation)

    client = make_client(handle)
    storage_operation(client, operation)

    assert [request.headers["authorization"] for request in requests] == [
        "Bearer old-access",
        "Bearer anon",
        "Bearer new-access",
    ]
    assert requests[0].url == requests[2].url
    assert requests[0].method == requests[2].method
    if operation == "upload":
        # Multipart boundaries can differ; the consumed stream's bytes must not.
        assert b"\r\n\r\nhello\x00\xff\r\n" in requests[0].content
        assert b"\r\n\r\nhello\x00\xff\r\n" in requests[2].content
    else:
        assert requests[0].content == requests[2].content
    assert client.current_session is not None
    assert client.current_session.user_id == USER_ID


@pytest.mark.parametrize("operation", OPERATIONS)
@pytest.mark.parametrize("refresh_status", [200, 401, 503])
def test_storage_bounds_retries_and_preserves_original_failure(
    operation: str, refresh_status: int
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/refresh":
            return (
                refresh_response()
                if refresh_status == 200
                else httpx.Response(refresh_status, json={"error": "refresh failed"})
            )
        return httpx.Response(401, json={"error": "storage denied"})

    client = make_client(handle)
    with pytest.raises(AuthenticationError, match="storage denied"):
        storage_operation(client, operation)
    assert len(requests) == (3 if refresh_status == 200 else 2)
    assert (client.current_session is None) == (refresh_status == 401)


@pytest.mark.parametrize("operation", OPERATIONS)
def test_storage_never_retries_under_a_replacement_session(operation: str) -> None:
    requests: list[httpx.Request] = []
    replacement = Session("replacement", "replacement-refresh", "other")

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/refresh":
            client.auth.set_session(replacement)
            return refresh_response()
        return httpx.Response(401, json={"error": "expired"})

    client = make_client(handle)
    with pytest.raises(SessionChangedError):
        storage_operation(client, operation)
    assert client.current_session == replacement
    assert len(requests) == 2


@pytest.mark.parametrize("operation", OPERATIONS)
@pytest.mark.parametrize("status", [403, 503])
def test_storage_does_not_refresh_other_http_failures(
    operation: str, status: int
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(status, json={"error": "storage unavailable"})

    with pytest.raises(VolcanoError, match="storage unavailable") as caught:
        storage_operation(make_client(handle), operation)
    assert caught.value.status == status
    assert len(requests) == 1


@pytest.mark.parametrize("operation", OPERATIONS)
def test_storage_does_not_retry_transport_failures(operation: str) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        message = "response lost"
        raise httpx.ReadTimeout(message, request=request)

    with pytest.raises(TransportError):
        storage_operation(make_client(handle), operation)
    assert len(requests) == 1


def test_remove_refreshes_only_the_rejected_path_and_reuses_rotated_credentials() -> (
    None
):
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/auth/refresh":
            return refresh_response()
        if (
            request.url.path.endswith("/second")
            and request.headers["authorization"] == "Bearer old-access"
        ):
            return httpx.Response(401, json={"error": "expired"})
        return success_response("remove")

    client = make_client(handle)
    assert client.storage.from_("assets").remove(["first", "second", "third"]) == (
        "first",
        "second",
        "third",
    )
    assert [
        (request.url.path, request.headers["authorization"]) for request in requests
    ] == [
        ("/storage/assets/first", "Bearer old-access"),
        ("/storage/assets/second", "Bearer old-access"),
        ("/auth/refresh", "Bearer anon"),
        ("/storage/assets/second", "Bearer new-access"),
        ("/storage/assets/third", "Bearer new-access"),
    ]


def test_remove_stops_when_a_different_session_is_adopted_between_paths() -> None:
    requests: list[httpx.Request] = []
    replacement = Session("replacement", "replacement-refresh", "other")

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        client.auth.set_session(replacement)
        return success_response("remove")

    client = make_client(handle)
    with pytest.raises(SessionChangedError):
        client.storage.from_("assets").remove(["first", "second"])
    assert client.current_session == replacement
    assert len(requests) == 1
