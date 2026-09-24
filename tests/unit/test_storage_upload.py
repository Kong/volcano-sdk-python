from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO

import httpx
import pytest
from fixtures.invalid_arguments import non_string_content_type
from storage_fixtures import upload_response
from typing_extensions import override

from volcano_sdk import Session, VolcanoClient
from volcano_sdk._transport import GeneratedTransport, TransportResponse


@dataclass(frozen=True)
class UploadResponse:
    payload: object
    status_code: int = 201
    content: bytes = b""
    headers: dict[str, str] | None = None


class UploadPayloadTransport(GeneratedTransport):
    def __init__(self, payload: object) -> None:
        super().__init__(api_url="https://api.test.volcano.dev")
        self.payload: object = payload

    @override
    def upload_storage_object(
        self,
        *,
        authorization: str,
        bucket_name: str,
        path: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> TransportResponse:
        del authorization, bucket_name, path, data, content_type
        return UploadResponse(self.payload)


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
    _ = client.auth.set_session(Session("access", "refresh", "user"))
    source = BytesIO(b"skip-hello\x00\xff")
    _ = source.seek(5)

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
    "content_type", ["", " ", "text/plain\r\nX-Bad: yes", "x\x00y"]
)
def test_upload_rejects_invalid_content_type_before_reading(content_type: str) -> None:
    client = VolcanoClient(api_url="http://127.0.0.1:1", anon_key="anon")
    _ = client.auth.set_session(Session("access", "refresh", "user"))
    source = BytesIO(b"unchanged")

    with pytest.raises(ValueError, match="content_type"):
        _ = client.storage.from_("assets").upload(
            "payload.bin", source, content_type=content_type
        )

    assert source.tell() == 0


def test_upload_rejects_non_string_content_type_before_reading() -> None:
    client = VolcanoClient(api_url="http://127.0.0.1:1", anon_key="anon")
    _ = client.auth.set_session(Session("access", "refresh", "user"))
    source = BytesIO(b"unchanged")

    with pytest.raises(ValueError, match="content_type"):
        non_string_content_type(client.storage.from_("assets"), source)

    assert source.tell() == 0


def test_upload_requires_a_session_before_consuming_a_stream() -> None:
    client = VolcanoClient(anon_key="anon")
    source = BytesIO(b"private")

    with pytest.raises(RuntimeError, match="active session"):
        _ = client.storage.from_("assets").upload("payload.bin", source)

    assert source.tell() == 0
    assert not source.closed


@pytest.mark.parametrize("payload", [[], {1: "unexpected"}])
def test_upload_rejects_malformed_success_payload(payload: object) -> None:
    client = VolcanoClient(anon_key="anon", _transport=UploadPayloadTransport(payload))
    _ = client.auth.set_session(Session("access", "refresh", "user"))

    with pytest.raises(TypeError, match="Expected a storage upload response object"):
        _ = client.storage.from_("assets").upload("payload.bin", b"payload")
