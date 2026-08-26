from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx
import pytest

from volcano_sdk import VolcanoClient
from volcano_sdk.errors import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
    RateLimitedError,
    ServerError,
    TransportError,
    ValidationError,
    VolcanoError,
)


@dataclass(frozen=True)
class ErrorResponse:
    status_code: int
    payload: dict[str, Any]
    content: bytes = b""
    headers: dict[str, str] | None = None


class ErrorTransport:
    def __init__(self, failure: ErrorResponse | Exception) -> None:
        self.failure = failure

    def auth_signin(self, **kwargs: Any) -> ErrorResponse:
        del kwargs
        if isinstance(self.failure, Exception):
            raise self.failure
        return self.failure


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (400, ValidationError),
        (401, AuthenticationError),
        (403, AuthenticationError),
        (404, NotFoundError),
        (409, ConflictError),
        (429, RateLimitedError),
        (500, ServerError),
        (503, ServerError),
    ],
)
def test_http_failures_map_to_stable_error_categories(
    status: int,
    expected: type[VolcanoError],
) -> None:
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=ErrorTransport(
            ErrorResponse(
                status,
                {"error": "contract failure", "code": "contract_code"},
                headers={"Retry-After": "17"},
            )
        ),
    )

    with pytest.raises(expected) as caught:
        client.auth.sign_in(email="user@example.com", password="wrong")

    assert str(caught.value) == "contract failure"
    assert caught.value.status == status
    assert caught.value.code == "contract_code"
    assert caught.value.retry_after == (17 if status == 429 else None)


def test_network_failure_maps_to_transport_error() -> None:
    request = httpx.Request("POST", "https://api.test.volcano.dev/auth/signin")
    client = VolcanoClient(
        anon_key="anon-key",
        _transport=ErrorTransport(httpx.ConnectError("connection failed", request=request)),
    )

    with pytest.raises(TransportError) as caught:
        client.auth.sign_in(email="user@example.com", password="secret")

    assert caught.value.status is None
    assert caught.value.code is None
    assert caught.value.retry_after is None
    assert isinstance(caught.value.__cause__, httpx.ConnectError)
