from __future__ import annotations

from io import BytesIO
from typing import Any

import httpx
import pytest

from volcano_sdk import Session, VolcanoClient
from volcano_sdk._transport import GeneratedTransport


def upload_response() -> httpx.Response:
    return httpx.Response(
        201,
        json={
            "id": "00000000-0000-4000-8000-000000000020",
            "bucket_id": "00000000-0000-4000-8000-000000000030",
            "name": "payload.bin",
            "is_public": False,
            "size": 7,
            "mime_type": "application/octet-stream",
            "metadata": {},
            "owner_id": "00000000-0000-4000-8000-000000000010",
            "created_at": "2026-09-08T12:00:00Z",
            "updated_at": "2026-09-08T12:00:00Z",
        },
    )


@pytest.mark.parametrize(
    "content_type", [None, "image/png", "text/plain; charset=utf-8"]
)
def test_upload_sends_the_file_content_type(content_type: str | None) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return upload_response()

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.set_session(Session("access", "refresh", "user"))
    source = BytesIO(b"skip-hello\x00\xff")
    source.seek(5)

    options = {} if content_type is None else {"content_type": content_type}
    result = client.storage.from_("assets").upload("payload.bin", source, **options)

    request = requests[0]
    expected_type = content_type or "application/octet-stream"
    assert request.headers["content-type"].startswith("multipart/form-data; boundary=")
    assert f"Content-Type: {expected_type}\r\n".encode() in request.content
    assert b'name="file"; filename="payload.bin"' in request.content
    assert b"\r\n\r\nhello\x00\xff\r\n" in request.content
    assert not source.closed
    assert result["name"] == "payload.bin"


@pytest.mark.parametrize(
    "content_type", ["", " ", "text/plain\r\nX-Bad: yes", "x\x00y", 1]
)
def test_upload_rejects_invalid_content_type_before_reading(content_type: Any) -> None:
    client = VolcanoClient(api_url="http://127.0.0.1:1", anon_key="anon")
    client.auth.set_session(Session("access", "refresh", "user"))
    source = BytesIO(b"unchanged")

    with pytest.raises(ValueError, match="content_type"):
        client.storage.from_("assets").upload(
            "payload.bin", source, content_type=content_type
        )

    assert source.tell() == 0
