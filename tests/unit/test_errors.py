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

UNEXPECTED_TRANSPORT_CALL = "unexpected transport operation"


@dataclass(frozen=True)
class ErrorResponse:
    status_code: int
    payload: dict[str, Any]
    content: bytes = b""
    headers: dict[str, str] | None = None


class ErrorTransport:
    def __init__(self, failure: ErrorResponse | Exception) -> None:
        self.failure = failure

    def auth_signin(
        self,
        *,
        authorization: str,
        email: str,
        password: str,
    ) -> ErrorResponse:
        del authorization, email, password
        if isinstance(self.failure, Exception):
            raise self.failure
        return self.failure

    def query_database_select(
        self,
        *,
        authorization: str,
        database_name: str,
        body: dict[str, Any],
    ) -> ErrorResponse:
        del authorization, database_name, body
        raise AssertionError(UNEXPECTED_TRANSPORT_CALL)

    def query_database_insert(
        self,
        *,
        authorization: str,
        database_name: str,
        body: dict[str, Any],
    ) -> ErrorResponse:
        del authorization, database_name, body
        raise AssertionError(UNEXPECTED_TRANSPORT_CALL)

    def query_database_update(
        self,
        *,
        authorization: str,
        database_name: str,
        body: dict[str, Any],
    ) -> ErrorResponse:
        del authorization, database_name, body
        raise AssertionError(UNEXPECTED_TRANSPORT_CALL)

    def upload_storage_object(
        self,
        *,
        authorization: str,
        bucket_name: str,
        path: str,
        data: bytes,
    ) -> ErrorResponse:
        del authorization, bucket_name, path, data
        raise AssertionError(UNEXPECTED_TRANSPORT_CALL)

    def download_storage_object(
        self,
        *,
        authorization: str,
        bucket_name: str,
        path: str,
    ) -> ErrorResponse:
        del authorization, bucket_name, path
        raise AssertionError(UNEXPECTED_TRANSPORT_CALL)

    def acquire_project_lock(
        self,
        *,
        authorization: str,
        key: str,
        ttl: int,
        token: str,
    ) -> ErrorResponse:
        del authorization, key, ttl, token
        raise AssertionError(UNEXPECTED_TRANSPORT_CALL)

    def release_project_lock(
        self,
        *,
        authorization: str,
        key: str,
        token: str,
    ) -> ErrorResponse:
        del authorization, key, token
        raise AssertionError(UNEXPECTED_TRANSPORT_CALL)


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
        _transport=ErrorTransport(
            httpx.ConnectError("connection failed", request=request)
        ),
    )

    with pytest.raises(TransportError) as caught:
        client.auth.sign_in(email="user@example.com", password="secret")

    assert caught.value.status is None
    assert caught.value.code is None
    assert caught.value.retry_after is None
    assert isinstance(caught.value.__cause__, httpx.ConnectError)
