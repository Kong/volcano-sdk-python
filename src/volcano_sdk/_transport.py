from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from io import BytesIO
from pathlib import PurePosixPath
from typing import Any, Protocol, cast
from uuid import UUID, uuid4

import httpx

from ._generated.api.authentication import auth_signin
from ._generated.api.database_queries import query_database_select
from ._generated.api.locks import acquire_project_lock, release_project_lock
from ._generated.api.storage_objects import (
    download_storage_object,
    upload_storage_object,
)
from ._generated.client import AuthenticatedClient
from ._generated.models.auth_signin_body import AuthSigninBody
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


@dataclass(frozen=True, slots=True)
class TransportResponse:
    status_code: int
    payload: Any
    content: bytes
    headers: Mapping[str, str]


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


def response_payload(response: Any, expected_status: int) -> Any:
    status = int(response.status_code)
    if status != expected_status:
        payload = response.payload if isinstance(response.payload, dict) else {}
        message = str(payload.get("error") or payload.get("message") or "Volcano request failed")
        code_value = payload.get("code")
        code = str(code_value) if code_value is not None else None
        retry_after = None
        if status == 429:
            retry_after_value = _header(response.headers, "Retry-After")
            try:
                retry_after = int(retry_after_value) if retry_after_value is not None else None
            except ValueError:
                retry_after = None
        error_type: type[VolcanoError]
        if status in (401, 403):
            error_type = AuthenticationError
        elif status in (400, 422):
            error_type = ValidationError
        elif status == 404:
            error_type = NotFoundError
        elif status == 409:
            error_type = ConflictError
        elif status == 429:
            error_type = RateLimitedError
        elif 500 <= status <= 599:
            error_type = ServerError
        else:
            error_type = VolcanoError
        raise error_type(
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
        return TransportResponse(
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
                x_volcano_lock_token=cast(UUID, token),
                x_volcano_request_id=cast(UUID, str(uuid4())),
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
                x_volcano_lock_token=cast(UUID, token),
                x_volcano_request_id=cast(UUID, str(uuid4())),
            )
        return self._response(response)
