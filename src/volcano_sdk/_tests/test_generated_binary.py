"""Verify generated binary response adapters against real HTTPX responses."""

from uuid import UUID

import httpx
import pytest

from volcano_sdk._generated.api.projects import get_project_logo
from volcano_sdk._generated.api.storage_objects import download_public_file
from volcano_sdk._generated.client import Client
from volcano_sdk._generated.types import File


@pytest.mark.parametrize(
    "content_type",
    ["image/png", "image/jpeg", "image/gif", "image/webp", "image/svg+xml"],
)
def test_generated_logo_response_preserves_bytes(content_type: str) -> None:
    payload = b"\x00\xff\x80binary response"
    transport = httpx.MockTransport(
        lambda _request: httpx.Response(
            200, content=payload, headers={"Content-Type": content_type}
        )
    )
    with Client(
        base_url="https://api.test",
        httpx_args={"transport": transport},
        raise_on_unexpected_status=True,
    ) as client:
        response = get_project_logo.sync_detailed(UUID(int=1), client=client)

    assert response.content == payload
    assert response.headers["Content-Type"] == content_type
    assert isinstance(response.parsed, File)
    assert response.parsed.payload.read() == payload


@pytest.mark.parametrize(
    "content_type", ["application/octet-stream", "application/zip", "image/png"]
)
def test_generated_public_download_preserves_bytes(content_type: str) -> None:
    payload = b"\x00\xff\x80binary response"
    transport = httpx.MockTransport(
        lambda _request: httpx.Response(
            200, content=payload, headers={"Content-Type": content_type}
        )
    )
    with Client(
        base_url="https://api.test",
        httpx_args={"transport": transport},
        raise_on_unexpected_status=True,
    ) as client:
        response = download_public_file.sync_detailed(
            UUID(int=1), "assets", "file.bin", client=client
        )

    assert response.content == payload
    assert response.headers["Content-Type"] == content_type
    assert isinstance(response.parsed, File)
    assert response.parsed.payload.read() == payload
