from __future__ import annotations

import json
from typing import TYPE_CHECKING

import httpx
import pytest

from volcano_sdk import VolcanoClient
from volcano_sdk._transport import GeneratedTransport, _header
from volcano_sdk.errors import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
    RateLimitedError,
    ServerError,
    SessionChangedError,
    TransportError,
    ValidationError,
    VolcanoError,
)

if TYPE_CHECKING:
    from collections.abc import Callable


def client_for(handler: Callable[[httpx.Request], httpx.Response]) -> VolcanoClient:
    return VolcanoClient(
        anon_key="anon-key",
        _transport=GeneratedTransport(
            api_url="https://api.test.volcano.dev",
            httpx_transport=httpx.MockTransport(handler),
        ),
    )


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (400, ValidationError),
        (401, AuthenticationError),
        (403, AuthenticationError),
        (404, NotFoundError),
        (409, ConflictError),
        (418, VolcanoError),
        (422, ValidationError),
        (429, RateLimitedError),
        (451, VolcanoError),
        (500, ServerError),
        (503, ServerError),
    ],
)
def test_http_failures_map_to_stable_error_categories(
    status: int,
    expected: type[VolcanoError],
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            status,
            json={"error": "contract failure", "code": "contract_code"},
            headers={"Retry-After": "17"},
        )

    client = client_for(handle)

    with pytest.raises(expected) as caught:
        _ = client.auth.sign_in(email="user@example.com", password="wrong")

    assert str(caught.value) == "contract failure"
    assert type(caught.value) is expected
    assert caught.value.status == status
    assert caught.value.code == "contract_code"
    assert caught.value.retry_after == (17 if status == 429 else None)
    assert len(requests) == 1
    assert requests[0].method == "POST"
    assert requests[0].url == "https://api.test.volcano.dev/auth/signin"
    assert requests[0].headers["authorization"] == "Bearer anon-key"
    assert json.loads(requests[0].content) == {
        "email": "user@example.com",
        "password": "wrong",
    }
    assert client.auth.get_session() is None


@pytest.mark.parametrize(
    "retry_after", ["", "invalid", "1.5", "Wed, 21 Oct 2015 07:28:00 GMT"]
)
def test_invalid_retry_delay_preserves_the_rate_limit_error(retry_after: str) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            429,
            json={"error": "rate limited", "code": "rate_limit_exceeded"},
            headers={"Retry-After": retry_after},
        )

    client = client_for(handle)

    with pytest.raises(RateLimitedError, match="rate limited") as caught:
        _ = client.auth.sign_in(email="user@example.com", password="wrong")

    assert caught.value.status == 429
    assert caught.value.code == "rate_limit_exceeded"
    assert caught.value.retry_after is None
    assert len(requests) == 1
    assert client.auth.get_session() is None


@pytest.mark.parametrize(
    ("headers", "expected"),
    [
        (None, None),
        ({}, None),
        ({"Content-Type": "application/json"}, None),
        ({"rEtRy-AfTeR": "17"}, "17"),
        ({"Retry-After": ""}, ""),
    ],
)
def test_optional_response_headers_preserve_case_insensitive_values(
    headers: dict[str, str] | None, expected: str | None
) -> None:
    assert _header(headers, "retry-after") == expected


def test_network_failure_maps_to_transport_error() -> None:
    requests: list[httpx.Request] = []
    message = "connection failed"

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        raise httpx.ConnectError(message, request=request)

    client = client_for(handle)

    with pytest.raises(TransportError) as caught:
        _ = client.auth.sign_in(email="user@example.com", password="secret")

    assert caught.value.status is None
    assert caught.value.code is None
    assert caught.value.retry_after is None
    assert isinstance(caught.value.__cause__, httpx.ConnectError)
    assert str(caught.value.__cause__) == message
    assert len(requests) == 1
    assert caught.value.__cause__.request is requests[0]
    assert client.auth.get_session() is None


def test_session_changed_error_preserves_its_public_contract() -> None:
    error = SessionChangedError()

    assert str(error) == "Session changed during authentication operation"
    assert error.status == 409
    assert error.code == "auth_session_changed"
    assert error.retry_after is None
