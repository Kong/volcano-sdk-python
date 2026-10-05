"""Typed request and response capabilities for transport adapters."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    ParamSpec,
    Protocol,
    TypeVar,
    runtime_checkable,
)

from .errors import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
    RateLimitedError,
    ValidationError,
    VolcanoError,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

    from ._generated.models.auth_link_o_auth_provider_provider import (
        AuthLinkOAuthProviderProvider,
    )
    from ._generated.models.auth_o_auth_authorize_provider import (
        AuthOAuthAuthorizeProvider,
    )
    from ._generated.models.auth_unlink_o_auth_provider_provider import (
        AuthUnlinkOAuthProviderProvider,
    )
    from ._generated.models.call_o_auth_provider_api_provider import (
        CallOAuthProviderAPIProvider,
    )
    from ._generated.models.get_o_auth_provider_token_provider import (
        GetOAuthProviderTokenProvider,
    )
    from ._generated.models.refresh_o_auth_provider_token_provider import (
        RefreshOAuthProviderTokenProvider,
    )
    from .models import DurableExecutionStatus, JSONValue


HTTP_CREATED = 201


HTTP_UNAUTHORIZED = 401


HTTP_NOT_FOUND = 404


HTTP_CONFLICT = 409


HTTP_RATE_LIMITED = 429


HTTP_OK = 200


HTTP_SERVER_ERROR_MIN = 500


HTTP_SERVER_ERROR_MAX = 599


RETRY_AFTER_HEADER = "Retry-After"


URL_TRAILING_SLASHES = "/"


MALFORMED_USER_PROFILE = "Expected a complete user profile"


MALFORMED_SESSION_PAGE = "Expected a complete session page"


MALFORMED_LINKED_OAUTH_PROVIDERS = "Expected complete linked OAuth providers"


MALFORMED_OAUTH_LINK = "Expected an OAuth authorization URL"


MALFORMED_OAUTH_STATUS = "Expected complete OAuth provider token status"


MALFORMED_OAUTH_API_RESPONSE = "Expected OAuth provider API response data"


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
    def payload(self) -> object: ...

    @property
    def content(self) -> bytes: ...

    @property
    def headers(self) -> Mapping[str, str] | None: ...


class RawHTTPResponse(Protocol):
    @property
    def status_code(self) -> int: ...

    @property
    def content(self) -> bytes: ...

    @property
    def headers(self) -> Mapping[str, str]: ...


class ParsedHTTPResponse(RawHTTPResponse, Protocol):
    @property
    def parsed(self) -> object: ...


class JSONResponse(Protocol):
    def json(self) -> object: ...


class JSONDecoder(Protocol):
    def __call__(self, document: bytes, /) -> object: ...


decode_json: JSONDecoder = json.loads


@runtime_checkable
class ModelPayload(Protocol):
    def to_dict(self) -> Mapping[str, object]: ...


@dataclass(frozen=True, slots=True)
class DurableExecutionListRequest:
    """Filters and paging for a durable execution listing."""

    status: DurableExecutionStatus | None = None
    page: int | None = None
    limit: int | None = None


@dataclass(frozen=True, slots=True)
class StorageUploadSessionRequest:
    """Values needed to create a resumable storage upload session."""

    path: str
    content_type: str
    total_size: int
    part_size: int | None


@dataclass(frozen=True, slots=True)
class StorageUploadPartRequest:
    """Values needed to upload one resumable storage part."""

    path: str
    session_id: str
    part_number: int
    data: bytes


@dataclass(frozen=True, slots=True)
class StorageUploadSessionReference:
    """Values identifying one resumable storage upload session."""

    path: str
    session_id: str


@dataclass(frozen=True, slots=True)
class GeneratedTransportResponse:
    status_code: int
    payload: object
    content: bytes
    headers: Mapping[str, str]


@runtime_checkable
class AuthRefreshTransport(Protocol):
    def auth_refresh(
        self,
        *,
        authorization: str,
        refresh_token: str,
    ) -> TransportResponse: ...


@runtime_checkable
class AuthLogoutTransport(Protocol):
    def auth_logout(
        self,
        *,
        authorization: str,
        refresh_token: str,
    ) -> TransportResponse: ...


@runtime_checkable
class AuthSignUpTransport(Protocol):
    def auth_signup(
        self,
        *,
        authorization: str,
        email: str,
        password: str,
        metadata: dict[str, object],
    ) -> TransportResponse: ...


@runtime_checkable
class AuthSignUpAnonymousTransport(Protocol):
    def auth_signup_anonymous(
        self,
        *,
        authorization: str,
        metadata: dict[str, object],
    ) -> TransportResponse: ...


@runtime_checkable
class AuthConvertAnonymousTransport(Protocol):
    def auth_convert_anonymous(
        self,
        *,
        authorization: str,
        email: str,
        password: str,
        metadata: dict[str, object],
    ) -> TransportResponse: ...


@runtime_checkable
class AuthForgotPasswordTransport(Protocol):
    def auth_forgot_password(
        self,
        *,
        authorization: str,
        email: str,
    ) -> TransportResponse: ...


@runtime_checkable
class AuthConfirmEmailTransport(Protocol):
    def auth_confirm_email(
        self,
        *,
        authorization: str,
        token: str,
    ) -> TransportResponse: ...


@runtime_checkable
class AuthResetPasswordTransport(Protocol):
    def auth_reset_password(
        self,
        *,
        authorization: str,
        token: str,
        new_password: str,
    ) -> TransportResponse: ...


@runtime_checkable
class AuthResendConfirmationTransport(Protocol):
    def auth_resend_confirmation(
        self,
        *,
        authorization: str,
        email: str,
    ) -> TransportResponse: ...


@runtime_checkable
class AuthRequestEmailChangeTransport(Protocol):
    def auth_request_email_change(
        self,
        *,
        authorization: str,
        new_email: str,
    ) -> TransportResponse: ...


@runtime_checkable
class AuthCancelEmailChangeTransport(Protocol):
    def auth_cancel_email_change(
        self,
        *,
        authorization: str,
    ) -> TransportResponse: ...


@runtime_checkable
class AuthConfirmEmailChangeTransport(Protocol):
    def auth_confirm_email_change(
        self,
        *,
        authorization: str,
        token: str,
    ) -> TransportResponse: ...


@runtime_checkable
class AuthDeleteAllMySessionsTransport(Protocol):
    def auth_delete_all_my_sessions(
        self,
        *,
        authorization: str,
    ) -> TransportResponse: ...


@runtime_checkable
class AuthDeleteMySessionTransport(Protocol):
    def auth_delete_my_session(
        self,
        *,
        authorization: str,
        session_id: str,
    ) -> TransportResponse: ...


@runtime_checkable
class AuthGetMySessionsTransport(Protocol):
    def auth_get_my_sessions(
        self,
        *,
        authorization: str,
        page: int,
        limit: int,
    ) -> TransportResponse: ...


@runtime_checkable
class AuthListOAuthProvidersTransport(Protocol):
    def auth_list_oauth_providers(
        self,
        *,
        authorization: str,
    ) -> TransportResponse: ...


@runtime_checkable
class AuthOAuthAuthorizationURLTransport(Protocol):
    def auth_oauth_authorization_url(
        self,
        *,
        anon_key: str,
        provider: AuthOAuthAuthorizeProvider,
        redirect_url: str,
        client_state: str,
    ) -> str: ...


@runtime_checkable
class AuthOAuthExchangeTransport(Protocol):
    def auth_oauth_exchange(
        self,
        *,
        authorization: str,
        code: str,
        redirect_url: str,
    ) -> TransportResponse: ...


@runtime_checkable
class AuthLinkOAuthProviderTransport(Protocol):
    def auth_link_oauth_provider(
        self,
        *,
        authorization: str,
        provider: AuthLinkOAuthProviderProvider,
    ) -> TransportResponse: ...


@runtime_checkable
class AuthUnlinkOAuthProviderTransport(Protocol):
    def auth_unlink_oauth_provider(
        self,
        *,
        authorization: str,
        provider: AuthUnlinkOAuthProviderProvider,
    ) -> TransportResponse: ...


@runtime_checkable
class AuthGetOAuthProviderTokenTransport(Protocol):
    def auth_get_oauth_provider_token(
        self,
        *,
        authorization: str,
        provider: GetOAuthProviderTokenProvider,
    ) -> TransportResponse: ...


@runtime_checkable
class AuthRefreshOAuthProviderTokenTransport(Protocol):
    def auth_refresh_oauth_provider_token(
        self,
        *,
        authorization: str,
        provider: RefreshOAuthProviderTokenProvider,
    ) -> TransportResponse: ...


@runtime_checkable
class AuthCallOAuthAPITransport(Protocol):
    def auth_call_oauth_api(
        self,
        *,
        authorization: str,
        provider: CallOAuthProviderAPIProvider,
        endpoint: str,
        method: str,
        body: Mapping[str, JSONValue] | None,
    ) -> TransportResponse: ...


@runtime_checkable
class AuthGetUserTransport(Protocol):
    def auth_get_user(self, *, authorization: str) -> TransportResponse: ...


@runtime_checkable
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
        body: dict[str, object],
    ) -> TransportResponse: ...

    def query_database_insert(
        self,
        *,
        authorization: str,
        database_name: str,
        body: dict[str, object],
    ) -> TransportResponse: ...

    def query_database_update(
        self,
        *,
        authorization: str,
        database_name: str,
        body: dict[str, object],
    ) -> TransportResponse: ...

    def query_database_delete(
        self,
        *,
        authorization: str,
        database_name: str,
        body: dict[str, object],
    ) -> TransportResponse: ...

    def upload_storage_object(
        self,
        *,
        authorization: str,
        bucket_name: str,
        path: str,
        data: bytes,
        content_type: str,
    ) -> TransportResponse: ...

    def download_storage_object(
        self,
        *,
        authorization: str,
        bucket_name: str,
        path: str,
        byte_range: str | None = None,
    ) -> TransportResponse: ...

    def acquire_project_lock(
        self,
        *,
        authorization: str,
        key: str,
        ttl: int,
        token: str,
        request_id: str | None = None,
    ) -> TransportResponse: ...

    def release_project_lock(
        self,
        *,
        authorization: str,
        key: str,
        token: str,
        request_id: str | None = None,
    ) -> TransportResponse: ...


@runtime_checkable
class AsyncDatabaseSelectTransport(Protocol):
    """Async database query capability used by cancellable realtime fetches."""

    async def query_database_select_async(
        self,
        *,
        authorization: str,
        database_name: str,
        body: dict[str, object],
    ) -> TransportResponse: ...


P = ParamSpec("P")


T = TypeVar("T")
