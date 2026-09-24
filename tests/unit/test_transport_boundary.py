"""Generated request fields are validated before crossing into HTTPX."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

import httpx
import pytest
from typing_extensions import override

from volcano_sdk import ServerError, VolcanoError
from volcano_sdk._generated.client import AuthenticatedClient
from volcano_sdk._transport import (
    GeneratedTransport,
    _generated_request,
    _GeneratedTransportResponse,
    _json_object,
    response_payload,
)


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
    with _client() as client, pytest.raises(TypeError) as caught:
        _ = _generated_request(client, kwargs)
    assert str(caught.value) == f"Invalid generated request field: {field}"


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


def test_generated_request_accepts_read_only_header_and_query_mappings() -> None:
    with _client() as client:
        response = _generated_request(
            client,
            {
                "method": "get",
                "url": "/test",
                "headers": MappingProxyType({"X-Test": "value"}),
                "params": MappingProxyType({"page": 2}),
            },
        )

    assert response.request.headers["x-test"] == "value"
    assert response.request.url.params["page"] == "2"


class _InvalidKeyResponse(httpx.Response):
    @override
    def json(self, **kwargs: object) -> object:
        return {1: "value"}


def test_json_object_rejects_non_string_keys() -> None:
    response = _InvalidKeyResponse(200)
    with pytest.raises(TypeError) as caught:
        _ = _json_object(response)
    assert str(caught.value) == "Invalid generated request field: response body key"


def test_json_object_rejects_a_non_object_response() -> None:
    with pytest.raises(TypeError) as caught:
        _ = _json_object(httpx.Response(200, json=["item"]))
    assert str(caught.value) == "Invalid generated request field: response body"


@pytest.mark.parametrize(
    ("payload", "message", "code"),
    [
        ({"error": "specific", "message": "fallback"}, "specific", None),
        ({"message": "message only"}, "message only", None),
        ({}, "Volcano request failed", None),
        ({"code": 42}, "Volcano request failed", "42"),
    ],
)
def test_response_payload_keeps_error_message_precedence_and_code(
    payload: dict[str, object], message: str, code: str | None
) -> None:
    response = _GeneratedTransportResponse(422, payload, b"", {})
    with pytest.raises(VolcanoError) as caught:
        _ = response_payload(response, 200)
    assert str(caught.value) == message
    assert caught.value.code == code


def test_response_payload_classifies_the_last_server_error_status() -> None:
    response = _GeneratedTransportResponse(599, {}, b"", {})
    with pytest.raises(ServerError) as caught:
        _ = response_payload(response, 200)
    assert caught.value.status == 599


@dataclass(frozen=True)
class _ParsedResponse:
    status_code: int
    parsed: object
    content: bytes
    headers: dict[str, str]


def test_generated_transport_preserves_a_parsed_scalar() -> None:
    response = _ParsedResponse(200, "created", b"{}", {})

    result = GeneratedTransport._response(response)

    assert result.payload == "created"


def test_generated_transport_returns_none_for_invalid_fallback_json() -> None:
    response = _ParsedResponse(200, None, b"not json", {})

    result = GeneratedTransport._response(response)

    assert result.payload is None
