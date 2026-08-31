"""Internal transport boundary around the generated OpenAPI client."""

from __future__ import annotations

import json
from dataclasses import dataclass
from io import BytesIO
from pathlib import PurePosixPath
from typing import TYPE_CHECKING, Any, Protocol, cast
from uuid import UUID, uuid4

import httpx

from ._generated.api.authentication import (
    auth_logout,
    auth_refresh,
    auth_signin,
    auth_signup,
)
from ._generated.api.database_queries import query_database_select
from ._generated.api.locks import acquire_project_lock, release_project_lock
from ._generated.api.storage_objects import (
    download_storage_object,
    upload_storage_object,
)
from ._generated.client import AuthenticatedClient
from ._generated.models.auth_logout_body import AuthLogoutBody
from ._generated.models.auth_refresh_body import AuthRefreshBody
from ._generated.models.auth_signin_body import AuthSigninBody
from ._generated.models.auth_signup_body import AuthSignupBody
from ._generated.models.auth_signup_body_user_metadata import (
    AuthSignupBodyUserMetadata,
)
from ._generated.models.database_select_request import DatabaseSelectRequest
from ._generated.models.project_lock_lease_request import ProjectLockLeaseRequest
from ._generated.models.upload_storage_object_files_body import (
    UploadStorageObjectFilesBody,
)
from ._generated.types import File
from .errors import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
    RateLimitedError,
    ServerError,
    TransportError,
    ValidationError,
    VolcanoError,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

HTTP_NOT_FOUND = 404
HTTP_CONFLICT = 409
HTTP_RATE_LIMITED = 429
HTTP_SERVER_ERROR_MIN = 500
HTTP_SERVER_ERROR_MAX = 599
ERROR_TYPES_BY_STATUS: dict[int, type[VolcanoError]] = {
    400: ValidationError,
    401: AuthenticationError,
    403: AuthenticationError,
    HTTP_NOT_FOUND: NotFoundError,
    HTTP_CONFLICT: ConflictError,
    422: ValidationError,
    HTTP_RATE_LIMITED: RateLimitedError,
}


class TransportResponse(Protocol):
    @property
    def status_code(self) -> int: ...

    @property
    def payload(self) -> Any: ...

    @property
    def content(self) -> bytes: ...

    @property
    def headers(self) -> Mapping[str, str] | None: ...


@dataclass(frozen=True, slots=True)
class _GeneratedTransportResponse:
    status_code: int
    payload: Any
    content: bytes
    headers: Mapping[str, str]


class AuthRefreshTransport(Protocol):
    def auth_refresh(
        self,
        *,
        authorization: str,
        refresh_token: str,
    ) -> TransportResponse: ...


class AuthLogoutTransport(Protocol):
    def auth_logout(
        self,
        *,
        authorization: str,
        refresh_token: str,
    ) -> TransportResponse: ...


class AuthSignUpTransport(Protocol):
    def auth_signup(
        self,
        *,
        authorization: str,
        email: str,
        password: str,
        metadata: dict[str, object],
    ) -> TransportResponse: ...


class Transport(Protocol):
    def auth_signin(
        self,
        *,
        authorization: str,
        email: str,
        password: str,
    ) -> TransportResponse: ...

    def query_database_select(
        self,
        *,
        authorization: str,
        database_name: str,
        body: dict[str, Any],
    ) -> TransportResponse: ...

    def upload_storage_object(
        self,
        *,
        authorization: str,
        bucket_name: str,
        path: str,
        data: bytes,
    ) -> TransportResponse: ...

    def download_storage_object(
        self,
        *,
        authorization: str,
        bucket_name: str,
        path: str,
    ) -> TransportResponse: ...

    def acquire_project_lock(
        self,
        *,
        authorization: str,
        key: str,
        ttl: int,
        token: str,
    ) -> TransportResponse: ...

    def release_project_lock(
        self,
        *,
        authorization: str,
        key: str,
        token: str,
    ) -> TransportResponse: ...


def invoke(operation: Callable[..., Any], **kwargs: Any) -> Any:
    try:
        return operation(**kwargs)
    except httpx.HTTPError as error:
        raise TransportError(str(error) or "Volcano transport failed") from error


def _header(headers: Mapping[str, str] | None, name: str) -> str | None:
    if headers is None:
        return None
    for key, value in headers.items():
        if key.lower() == name.lower():
            return value
    return None


def _error_type(status: int) -> type[VolcanoError]:
    error_type = ERROR_TYPES_BY_STATUS.get(status)
    if error_type is not None:
        return error_type
    if HTTP_SERVER_ERROR_MIN <= status <= HTTP_SERVER_ERROR_MAX:
        return ServerError
    return VolcanoError


def response_payload(response: Any, expected_status: int) -> Any:
    status = int(response.status_code)
    if status != expected_status:
        payload: Mapping[str, object]
        raw_payload = response.payload
        if isinstance(raw_payload, dict):
            payload = cast("Mapping[str, object]", raw_payload)
        else:
            payload = {}
        message = str(
            payload.get("error") or payload.get("message") or "Volcano request failed"
        )
        code_value = payload.get("code")
        code = str(code_value) if code_value is not None else None
        retry_after = None
        if status == HTTP_RATE_LIMITED:
            retry_after_value = _header(response.headers, "Retry-After")
            try:
                retry_after = (
                    int(retry_after_value) if retry_after_value is not None else None
                )
            except ValueError:
                retry_after = None
        raise _error_type(status)(
            message,
            status=status,
            code=code,
            retry_after=retry_after,
        )
    return response.payload


class GeneratedTransport:
    def __init__(
        self,
        *,
        api_url: str,
        timeout: float = 60.0,
        httpx_transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._api_url = api_url.rstrip("/")
        self._timeout = timeout
        self._httpx_transport = httpx_transport

    def _client(self, authorization: str) -> AuthenticatedClient:
        httpx_args: dict[str, Any] = {}
        if self._httpx_transport is not None:
            httpx_args["transport"] = self._httpx_transport
        return AuthenticatedClient(
            base_url=self._api_url,
            token=authorization,
            timeout=httpx.Timeout(self._timeout),
            httpx_args=httpx_args,
        )

    @staticmethod
    def _response(response: Any) -> TransportResponse:
        parsed = response.parsed
        if hasattr(parsed, "to_dict"):
            payload = parsed.to_dict()
        elif parsed is not None:
            payload = parsed
        else:
            try:
                payload = json.loads(response.content)
            except (json.JSONDecodeError, UnicodeDecodeError):
                payload = None
        return _GeneratedTransportResponse(
            status_code=int(response.status_code),
            payload=payload,
            content=response.content,
            headers=dict(response.headers),
        )

    def auth_signin(
        self,
        *,
        authorization: str,
        email: str,
        password: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = auth_signin.sync_detailed(
                client=client,
                body=AuthSigninBody(email=email, password=password),
            )
        return self._response(response)

    def auth_signup(
        self,
        *,
        authorization: str,
        email: str,
        password: str,
        metadata: dict[str, object],
    ) -> TransportResponse:
        body = AuthSignupBody(
            email=email,
            password=password,
            user_metadata=AuthSignupBodyUserMetadata.from_dict(metadata),
        )
        with self._client(authorization) as client:
            response = auth_signup.sync_detailed(client=client, body=body)
        return self._response(response)

    def auth_refresh(
        self,
        *,
        authorization: str,
        refresh_token: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = auth_refresh.sync_detailed(
                client=client,
                body=AuthRefreshBody(refresh_token=refresh_token),
            )
        return self._response(response)

    def auth_logout(
        self,
        *,
        authorization: str,
        refresh_token: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = auth_logout.sync_detailed(
                client=client,
                body=AuthLogoutBody(refresh_token=refresh_token),
            )
        return self._response(response)

    def query_database_select(
        self,
        *,
        authorization: str,
        database_name: str,
        body: dict[str, Any],
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = query_database_select.sync_detailed(
                database_name,
                client=client,
                body=DatabaseSelectRequest.from_dict(body),
            )
        return self._response(response)

    def upload_storage_object(
        self,
        *,
        authorization: str,
        bucket_name: str,
        path: str,
        data: bytes,
    ) -> TransportResponse:
        file_name = PurePosixPath(path).name or "file"
        body = UploadStorageObjectFilesBody(
            file=File(
                payload=BytesIO(data),
                file_name=file_name,
                mime_type="application/octet-stream",
            )
        )
        with self._client(authorization) as client:
            response = upload_storage_object.sync_detailed(
                bucket_name,
                path,
                client=client,
                body=body,
            )
        return self._response(response)

    def download_storage_object(
        self,
        *,
        authorization: str,
        bucket_name: str,
        path: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = download_storage_object.sync_detailed(
                bucket_name,
                path,
                client=client,
            )
        return self._response(response)

    def acquire_project_lock(
        self,
        *,
        authorization: str,
        key: str,
        ttl: int,
        token: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = acquire_project_lock.sync_detailed(
                key,
                client=client,
                body=ProjectLockLeaseRequest(ttl_seconds=ttl),
                x_volcano_lock_token=cast("UUID", token),
                x_volcano_request_id=cast("UUID", str(uuid4())),
            )
        return self._response(response)

    def release_project_lock(
        self,
        *,
        authorization: str,
        key: str,
        token: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = release_project_lock.sync_detailed(
                key,
                client=client,
                x_volcano_lock_token=cast("UUID", token),
                x_volcano_request_id=cast("UUID", str(uuid4())),
            )
        return self._response(response)
