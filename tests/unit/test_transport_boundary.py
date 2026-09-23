"""Generated request fields are validated before crossing into HTTPX."""

from __future__ import annotations

import httpx
import pytest
from typing_extensions import override

from volcano_sdk._generated.client import AuthenticatedClient
from volcano_sdk._transport import _generated_request, _json_object


def _client() -> AuthenticatedClient:
    def respond(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"url": str(request.url)})

    return AuthenticatedClient(
        base_url="https://api.test.volcano.dev",
        token="access-token",
        httpx_args={"transport": httpx.MockTransport(respond)},
    )


@pytest.mark.parametrize(
    ("kwargs", "field"),
    [
        ({"url": "/test"}, "method"),
        ({"method": "get"}, "url"),
        ({"method": "get", "url": "/test", "headers": 1}, "headers"),
        ({"method": "get", "url": "/test", "headers": {1: "value"}}, "headers"),
        ({"method": "get", "url": "/test", "headers": {"key": 1}}, "headers"),
        ({"method": "get", "url": "/test", "params": 1}, "params"),
        ({"method": "get", "url": "/test", "params": {1: "value"}}, "params"),
        ({"method": "get", "url": "/test", "params": {"key": []}}, "params"),
        ({"method": "get", "url": "/test", "unsupported": True}, "unsupported field"),
    ],
)
def test_generated_request_rejects_invalid_fields(
    kwargs: dict[str, object], field: str
) -> None:
    with _client() as client, pytest.raises(TypeError, match=field):
        _ = _generated_request(client, kwargs)


def test_generated_request_preserves_valid_fields() -> None:
    with _client() as client:
        response = _generated_request(
            client,
            {
                "method": "post",
                "url": "/test",
                "headers": {"X-Test": "value"},
                "params": {"page": 2, "cursor": None, "enabled": True},
                "json": {"value": 1},
            },
        )

    assert response.request.headers["x-test"] == "value"
    assert response.request.url.params["page"] == "2"
    assert response.request.url.params["enabled"] == "true"
    assert response.request.url.params["cursor"] == ""
    assert response.request.content == b'{"value":1}'


class _InvalidKeyResponse(httpx.Response):
    @override
    def json(self, **kwargs: object) -> object:
        return {1: "value"}


def test_json_object_rejects_non_string_keys() -> None:
    response = _InvalidKeyResponse(200)
    with pytest.raises(TypeError, match="response body key"):
        _ = _json_object(response)
