from __future__ import annotations

from io import BytesIO
from typing import Annotated, TypeAlias

import httpx
from hypothesis import given, seed
from hypothesis import strategies as st
from property_support import PROPERTY_SEED
from storage_fixtures import upload_response

from volcano_sdk import Session, VolcanoClient
from volcano_sdk._transport import GeneratedTransport

BinaryPayload: TypeAlias = Annotated[bytes, st.binary(max_size=1024)]


@seed(PROPERTY_SEED)
@given(...)
def test_upload_preserves_remaining_binary_stream(payload: BinaryPayload) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return upload_response(len(payload))

    transport = GeneratedTransport(
        api_url="https://api.example.test", httpx_transport=httpx.MockTransport(handle)
    )
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.set_session(Session("access", "refresh", "user"))
    source = BytesIO(b"prefix" + payload)
    source.seek(6)
    client.storage.from_("assets").upload("payload.bin", source)
    assert len(requests) == 1
    assert b"\r\n\r\n" + payload + b"\r\n" in requests[0].content
    assert requests[0].headers["authorization"] == "Bearer access"
    assert source.tell() == 6 + len(payload)
    assert not source.closed


@seed(PROPERTY_SEED)
@given(...)
def test_download_preserves_arbitrary_bytes(payload: BinaryPayload) -> None:
    def handle(request: httpx.Request) -> httpx.Response:
        assert request.headers["authorization"] == "Bearer access"
        return httpx.Response(
            200, content=payload, headers={"Content-Type": "application/octet-stream"}
        )

    transport = GeneratedTransport(
        api_url="https://api.example.test", httpx_transport=httpx.MockTransport(handle)
    )
    client = VolcanoClient(anon_key="anon", _transport=transport)
    client.auth.set_session(Session("access", "refresh", "user"))
    assert client.storage.from_("assets").download("payload.bin") == payload
