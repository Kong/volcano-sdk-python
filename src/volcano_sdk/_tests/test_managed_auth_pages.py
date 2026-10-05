from uuid import UUID

import httpx
import pytest

from volcano_sdk._generated.api.auth_configuration import render_auth_page_preview
from volcano_sdk._generated.client import Client


@pytest.mark.parametrize(
    ("status", "content_type", "body"),
    [
        (200, "text/html", "<!doctype html><title>Preview</title>"),
        (404, "text/plain", "Preview ticket is invalid or expired"),
        (500, "text/plain", "Preview could not be rendered"),
    ],
)
def test_preview_transport_preserves_status_and_content_type(
    status: int,
    content_type: str,
    body: str,
) -> None:
    def respond(request: httpx.Request) -> httpx.Response:
        assert request.url.params["ticket"] == "preview-ticket"
        return httpx.Response(status, text=body, headers={"Content-Type": content_type})

    with httpx.Client(
        base_url="https://api.example.com",
        transport=httpx.MockTransport(respond),
    ) as http:
        client = Client(base_url="https://api.example.com").set_httpx_client(http)
        result = render_auth_page_preview.sync_detailed(
            UUID("00000000-0000-4000-8000-000000000001"),
            "login",
            client=client,
            ticket="preview-ticket",
        )

    assert result.status_code == status
    assert result.headers["content-type"].startswith(content_type)
    assert result.parsed == body
