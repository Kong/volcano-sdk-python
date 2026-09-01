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
    auth_confirm_email_change,
    auth_convert_anonymous,
    auth_get_user,
    auth_logout,
    auth_refresh,
    auth_signin,
    auth_signup,
    auth_update_user,
)
from ._generated.api.authentication.auth_cancel_email_change import (
    _get_kwargs as cancel_email_change_kwargs,
)
from ._generated.api.authentication.auth_confirm_email import (
    _get_kwargs as confirm_email_kwargs,
)
from ._generated.api.authentication.auth_delete_all_my_sessions import (
    _get_kwargs as delete_all_my_sessions_kwargs,
)
from ._generated.api.authentication.auth_delete_my_session import (
    _get_kwargs as delete_my_session_kwargs,
)
from ._generated.api.authentication.auth_forgot_password import (
    _get_kwargs as forgot_password_kwargs,
)
from ._generated.api.authentication.auth_get_my_sessions import (
    _get_kwargs as get_my_sessions_kwargs,
)
from ._generated.api.authentication.auth_request_email_change import (
    _get_kwargs as request_email_change_kwargs,
)
from ._generated.api.authentication.auth_resend_confirmation import (
    _get_kwargs as resend_confirmation_kwargs,
)
from ._generated.api.authentication.auth_reset_password import (
    _get_kwargs as reset_password_kwargs,
)
from ._generated.api.authentication.auth_signup_anonymous import (
    _get_kwargs as signup_anonymous_kwargs,
)
from ._generated.api.database_queries import query_database_select
from ._generated.api.locks import acquire_project_lock, release_project_lock
from ._generated.api.storage_objects import (
    download_storage_object,
    upload_storage_object,
)
from ._generated.client import AuthenticatedClient
from ._generated.models.auth_confirm_email_body import AuthConfirmEmailBody
from ._generated.models.auth_confirm_email_change_body import AuthConfirmEmailChangeBody
from ._generated.models.auth_convert_anonymous_body import AuthConvertAnonymousBody
from ._generated.models.auth_convert_anonymous_body_user_metadata import (
    AuthConvertAnonymousBodyUserMetadata,
)
from ._generated.models.auth_forgot_password_body import AuthForgotPasswordBody
from ._generated.models.auth_get_my_sessions_response_200 import (
    AuthGetMySessionsResponse200,
)
from ._generated.models.auth_logout_body import AuthLogoutBody
from ._generated.models.auth_refresh_body import AuthRefreshBody
from ._generated.models.auth_request_email_change_body import AuthRequestEmailChangeBody
from ._generated.models.auth_resend_confirmation_body import AuthResendConfirmationBody
from ._generated.models.auth_reset_password_body import AuthResetPasswordBody
from ._generated.models.auth_signin_body import AuthSigninBody
from ._generated.models.auth_signup_anonymous_body import AuthSignupAnonymousBody
from ._generated.models.auth_signup_anonymous_body_user_metadata import (
    AuthSignupAnonymousBodyUserMetadata,
)
from ._generated.models.auth_signup_body import AuthSignupBody
from ._generated.models.auth_signup_body_user_metadata import (
    AuthSignupBodyUserMetadata,
)
from ._generated.models.auth_update_user_body import AuthUpdateUserBody
from ._generated.models.auth_update_user_body_user_metadata import (
    AuthUpdateUserBodyUserMetadata,
)
from ._generated.models.database_select_request import DatabaseSelectRequest
from ._generated.models.project_lock_lease_request import ProjectLockLeaseRequest
from ._generated.models.upload_storage_object_files_body import (
    UploadStorageObjectFilesBody,
)
from ._generated.types import UNSET, File
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
HTTP_OK = 200
HTTP_SERVER_ERROR_MIN = 500
HTTP_SERVER_ERROR_MAX = 599
_MALFORMED_USER_PROFILE = "Expected a complete user profile"
_MALFORMED_SESSION_PAGE = "Expected a complete session page"
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


class AuthSignUpAnonymousTransport(Protocol):
    def auth_signup_anonymous(
        self,
        *,
        authorization: str,
        metadata: dict[str, object],
    ) -> TransportResponse: ...


class AuthConvertAnonymousTransport(Protocol):
    def auth_convert_anonymous(
        self,
        *,
        authorization: str,
        email: str,
        password: str,
        metadata: dict[str, object],
    ) -> TransportResponse: ...


class AuthForgotPasswordTransport(Protocol):
    def auth_forgot_password(
        self,
        *,
        authorization: str,
        email: str,
    ) -> TransportResponse: ...


class AuthConfirmEmailTransport(Protocol):
    def auth_confirm_email(
        self,
        *,
        authorization: str,
        token: str,
    ) -> TransportResponse: ...


class AuthResetPasswordTransport(Protocol):
    def auth_reset_password(
        self,
        *,
        authorization: str,
        token: str,
        new_password: str,
    ) -> TransportResponse: ...


class AuthResendConfirmationTransport(Protocol):
    def auth_resend_confirmation(
        self,
        *,
        authorization: str,
        email: str,
    ) -> TransportResponse: ...


class AuthRequestEmailChangeTransport(Protocol):
    def auth_request_email_change(
        self,
        *,
        authorization: str,
        new_email: str,
    ) -> TransportResponse: ...


class AuthCancelEmailChangeTransport(Protocol):
    def auth_cancel_email_change(
        self,
        *,
        authorization: str,
    ) -> TransportResponse: ...


class AuthConfirmEmailChangeTransport(Protocol):
    def auth_confirm_email_change(
        self,
        *,
        authorization: str,
        token: str,
    ) -> TransportResponse: ...


class AuthDeleteAllMySessionsTransport(Protocol):
    def auth_delete_all_my_sessions(
        self,
        *,
        authorization: str,
    ) -> TransportResponse: ...


class AuthDeleteMySessionTransport(Protocol):
    def auth_delete_my_session(
        self,
        *,
        authorization: str,
        session_id: str,
    ) -> TransportResponse: ...


class AuthGetMySessionsTransport(Protocol):
    def auth_get_my_sessions(
        self,
        *,
        authorization: str,
        page: int,
        limit: int,
    ) -> TransportResponse: ...


class AuthGetUserTransport(Protocol):
    def auth_get_user(self, *, authorization: str) -> TransportResponse: ...


class AuthUpdateUserTransport(Protocol):
    def auth_update_user(
        self,
        *,
        authorization: str,
        password: str | None,
        metadata: dict[str, object] | None,
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

    @staticmethod
    def _raw_response(response: httpx.Response) -> TransportResponse:
        try:
            payload = json.loads(response.content)
        except (json.JSONDecodeError, UnicodeDecodeError):
            payload = None
        return _GeneratedTransportResponse(
            status_code=response.status_code,
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

    def auth_signup_anonymous(
        self,
        *,
        authorization: str,
        metadata: dict[str, object],
    ) -> TransportResponse:
        body = AuthSignupAnonymousBody(
            user_metadata=AuthSignupAnonymousBodyUserMetadata.from_dict(metadata)
        )
        with self._client(authorization) as client:
            response = client.get_httpx_client().request(
                **signup_anonymous_kwargs(body=body)
            )
        return self._raw_response(response)

    def auth_convert_anonymous(
        self,
        *,
        authorization: str,
        email: str,
        password: str,
        metadata: dict[str, object],
    ) -> TransportResponse:
        body = AuthConvertAnonymousBody(
            email=email,
            password=password,
            user_metadata=AuthConvertAnonymousBodyUserMetadata.from_dict(metadata),
        )
        try:
            with self._client(authorization) as client:
                response = auth_convert_anonymous.sync_detailed(
                    client=client,
                    body=body,
                )
        except (
            AttributeError,
            KeyError,
            TypeError,
            UnicodeDecodeError,
            ValueError,
        ) as error:
            raise AuthenticationError(_MALFORMED_USER_PROFILE) from error
        if int(response.status_code) != HTTP_OK:
            return self._response(response)
        return _GeneratedTransportResponse(
            status_code=int(response.status_code),
            payload=response.parsed,
            content=response.content,
            headers=dict(response.headers),
        )

    def auth_forgot_password(
        self,
        *,
        authorization: str,
        email: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = client.get_httpx_client().request(
                **forgot_password_kwargs(body=AuthForgotPasswordBody(email=email))
            )
        return self._raw_response(response)

    def auth_confirm_email(
        self,
        *,
        authorization: str,
        token: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = client.get_httpx_client().request(
                **confirm_email_kwargs(body=AuthConfirmEmailBody(token=token))
            )
        return self._raw_response(response)

    def auth_reset_password(
        self,
        *,
        authorization: str,
        token: str,
        new_password: str,
    ) -> TransportResponse:
        body = AuthResetPasswordBody(token=token, new_password=new_password)
        with self._client(authorization) as client:
            response = client.get_httpx_client().request(
                **reset_password_kwargs(body=body)
            )
        return self._raw_response(response)

    def auth_resend_confirmation(
        self,
        *,
        authorization: str,
        email: str,
    ) -> TransportResponse:
        body = AuthResendConfirmationBody(email=email)
        with self._client(authorization) as client:
            response = client.get_httpx_client().request(
                **resend_confirmation_kwargs(body=body)
            )
        return self._raw_response(response)

    def auth_request_email_change(
        self,
        *,
        authorization: str,
        new_email: str,
    ) -> TransportResponse:
        body = AuthRequestEmailChangeBody(new_email=new_email)
        with self._client(authorization) as client:
            response = client.get_httpx_client().request(
                **request_email_change_kwargs(body=body)
            )
        return self._raw_response(response)

    def auth_cancel_email_change(self, *, authorization: str) -> TransportResponse:
        with self._client(authorization) as client:
            response = client.get_httpx_client().request(**cancel_email_change_kwargs())
        return self._raw_response(response)

    def auth_confirm_email_change(
        self,
        *,
        authorization: str,
        token: str,
    ) -> TransportResponse:
        body = AuthConfirmEmailChangeBody(email_change_token=token)
        try:
            with self._client(authorization) as client:
                response = auth_confirm_email_change.sync_detailed(
                    client=client,
                    body=body,
                )
        except (
            AttributeError,
            KeyError,
            TypeError,
            UnicodeDecodeError,
            ValueError,
        ) as error:
            raise AuthenticationError(_MALFORMED_USER_PROFILE) from error
        if int(response.status_code) != HTTP_OK:
            return self._response(response)
        return _GeneratedTransportResponse(
            status_code=int(response.status_code),
            payload=response.parsed,
            content=response.content,
            headers=dict(response.headers),
        )

    def auth_delete_all_my_sessions(
        self,
        *,
        authorization: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = client.get_httpx_client().request(
                **delete_all_my_sessions_kwargs()
            )
        return self._raw_response(response)

    def auth_delete_my_session(
        self,
        *,
        authorization: str,
        session_id: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = client.get_httpx_client().request(
                **delete_my_session_kwargs(session_id=cast("UUID", session_id))
            )
        return self._raw_response(response)

    def auth_get_my_sessions(
        self,
        *,
        authorization: str,
        page: int,
        limit: int,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = client.get_httpx_client().request(
                **get_my_sessions_kwargs(page=page, limit=limit)
            )
        if response.status_code != HTTP_OK:
            return self._raw_response(response)
        try:
            payload = AuthGetMySessionsResponse200.from_dict(response.json())
        except (
            AttributeError,
            KeyError,
            TypeError,
            UnicodeDecodeError,
            ValueError,
        ) as error:
            raise VolcanoError(_MALFORMED_SESSION_PAGE) from error
        return _GeneratedTransportResponse(
            status_code=response.status_code,
            payload=payload,
            content=response.content,
            headers=dict(response.headers),
        )

    def auth_get_user(self, *, authorization: str) -> TransportResponse:
        try:
            with self._client(authorization) as client:
                response = auth_get_user.sync_detailed(client=client)
        except (
            AttributeError,
            KeyError,
            TypeError,
            UnicodeDecodeError,
            ValueError,
        ) as error:
            raise AuthenticationError(_MALFORMED_USER_PROFILE) from error
        if int(response.status_code) != HTTP_OK:
            return self._response(response)
        return _GeneratedTransportResponse(
            status_code=int(response.status_code),
            payload=response.parsed,
            content=response.content,
            headers=dict(response.headers),
        )

    def auth_update_user(
        self,
        *,
        authorization: str,
        password: str | None,
        metadata: dict[str, object] | None,
    ) -> TransportResponse:
        body = AuthUpdateUserBody(
            password=UNSET if password is None else password,
            user_metadata=(
                UNSET
                if metadata is None
                else AuthUpdateUserBodyUserMetadata.from_dict(metadata)
            ),
        )
        try:
            with self._client(authorization) as client:
                response = auth_update_user.sync_detailed(client=client, body=body)
        except (
            AttributeError,
            KeyError,
            TypeError,
            UnicodeDecodeError,
            ValueError,
        ) as error:
            raise AuthenticationError(_MALFORMED_USER_PROFILE) from error
        if int(response.status_code) != HTTP_OK:
            return self._response(response)
        return _GeneratedTransportResponse(
            status_code=int(response.status_code),
            payload=response.parsed,
            content=response.content,
            headers=dict(response.headers),
        )

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
