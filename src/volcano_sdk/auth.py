"""Authentication facade."""

from __future__ import annotations

from collections.abc import Mapping
from contextlib import suppress
from datetime import datetime
from hmac import compare_digest
from secrets import token_urlsafe
from threading import RLock
from typing import TYPE_CHECKING, Any, Literal, Protocol, cast
from urllib.parse import quote, urlencode
from uuid import UUID

from ._transport import Transport, TransportResponse, invoke, response_payload
from .errors import AuthenticationError, ValidationError, VolcanoError
from .models import (
    AuthorizationRequest,
    AuthSession,
    EmailChangeResult,
    MessageResult,
    OAuthProvider,
    OAuthProviderName,
    OAuthTokenResult,
    Session,
    SessionPage,
    SignUpResult,
    User,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from .models import JSONValue

_INVALID_AUTH_RESPONSE = "Authentication response is missing required fields"
_MISSING_AUTH_STATE = "No refresh token available"
_HTTP_UNAUTHORIZED = 401
_INVALID_OAUTH_STATE = "OAuth state does not match"
_INVALID_OAUTH_PROVIDER = "Unsupported OAuth provider"
_MISSING_AUTHORIZATION_URL = "Authentication response is missing authorization URL"
_INVALID_SESSION_ID = "session_id must be a valid UUID"
_SUPPORTED_OAUTH_PROVIDERS = frozenset({"google", "github", "microsoft", "apple"})


class AuthContext(Protocol):
    """Client capabilities required by the authentication facade."""

    _transport: Transport
    _api_url: str

    @property
    def current_session(self) -> Session | None:
        """Return the client-owned session."""
        ...

    @property
    def current_user(self) -> User | None:
        """Return the client-owned user."""
        ...

    def _anon_token(self) -> str: ...

    def _session_token(self) -> str: ...

    def _commit_auth(self, session: Session, user: User) -> None: ...

    def _set_user(self, user: User) -> None: ...

    def _clear_auth(self) -> None: ...

    def _subscribe_auth(
        self,
        listener: Callable[[User | None], None],
    ) -> Callable[[], None]: ...


def _mapping(value: object) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return cast("Mapping[str, Any]", value)
    raise AuthenticationError(_INVALID_AUTH_RESPONSE)


def _optional_text(value: object) -> str | None:
    return value if isinstance(value, str) else None


def _optional_bool(value: object) -> bool | None:
    return value if isinstance(value, bool) else None


def _optional_int(value: object) -> int | None:
    return value if isinstance(value, int) else None


def _optional_datetime(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _optional_metadata(value: object) -> dict[str, JSONValue] | None:
    if not isinstance(value, dict):
        return None
    metadata = cast("dict[object, object]", value)
    if not all(isinstance(key, str) for key in metadata):
        return None
    return cast("dict[str, JSONValue]", metadata.copy())


def _json_value(value: object) -> JSONValue:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        items = cast("list[object]", value)
        return [_json_value(item) for item in items]
    if isinstance(value, dict):
        mapping = cast("dict[object, object]", value)
        if not all(isinstance(key, str) for key in mapping):
            raise AuthenticationError(_INVALID_AUTH_RESPONSE)
        return {cast("str", key): _json_value(item) for key, item in mapping.items()}
    raise AuthenticationError(_INVALID_AUTH_RESPONSE)


def _provider(value: str) -> OAuthProviderName:
    if value not in _SUPPORTED_OAUTH_PROVIDERS:
        raise ValidationError(_INVALID_OAUTH_PROVIDER)
    return cast("OAuthProviderName", value)


def _message(payload: Mapping[str, Any]) -> MessageResult:
    message = payload.get("message")
    if not isinstance(message, str):
        raise AuthenticationError(_INVALID_AUTH_RESPONSE)
    return MessageResult(message=message)


def _oauth_token(payload: Mapping[str, Any]) -> OAuthTokenResult:
    provider_value = payload.get("provider")
    if not isinstance(provider_value, str):
        raise AuthenticationError(_INVALID_AUTH_RESPONSE)
    return OAuthTokenResult(
        provider=_provider(provider_value),
        expires_in=_optional_int(payload.get("expires_in")),
        message=_optional_text(payload.get("message")),
    )


def _auth_session(payload: Mapping[str, Any]) -> AuthSession:
    session_id = payload.get("id")
    user_id = payload.get("user_id")
    provider = payload.get("provider")
    expires_at = _optional_datetime(payload.get("expires_at"))
    is_active = payload.get("is_active")
    is_current = payload.get("is_current")
    if (
        not isinstance(session_id, str)
        or not isinstance(user_id, str)
        or not isinstance(provider, str)
        or expires_at is None
        or not isinstance(is_active, bool)
        or not isinstance(is_current, bool)
    ):
        raise AuthenticationError(_INVALID_AUTH_RESPONSE)
    return AuthSession(
        id=session_id,
        user_id=user_id,
        provider=provider,
        expires_at=expires_at,
        is_active=is_active,
        is_current=is_current,
        user_agent=_optional_text(payload.get("user_agent")),
        ip_address=_optional_text(payload.get("ip_address")),
        last_ip_address=_optional_text(payload.get("last_ip_address")),
        last_activity_at=_optional_datetime(payload.get("last_activity_at")),
        session_started_at=_optional_datetime(payload.get("session_started_at")),
        created_at=_optional_datetime(payload.get("created_at")),
        updated_at=_optional_datetime(payload.get("updated_at")),
    )


def _user(payload: Mapping[str, Any]) -> User:
    user_id = payload.get("id")
    if not isinstance(user_id, str):
        raise AuthenticationError(_INVALID_AUTH_RESPONSE)
    email_value = payload.get("email")
    if not isinstance(email_value, str):
        raise AuthenticationError(_INVALID_AUTH_RESPONSE)
    return User(
        id=user_id,
        email=email_value,
        project_id=_optional_text(payload.get("project_id")),
        email_confirmed=_optional_bool(payload.get("email_confirmed")),
        user_metadata=_optional_metadata(payload.get("user_metadata")),
        app_metadata=_optional_metadata(payload.get("app_metadata")),
        avatar_url=_optional_text(payload.get("avatar_url")),
        status=_optional_text(payload.get("status")),
        banned_until=_optional_datetime(payload.get("banned_until")),
        last_sign_in_at=_optional_datetime(payload.get("last_sign_in_at")),
        created_at=_optional_datetime(payload.get("created_at")),
        updated_at=_optional_datetime(payload.get("updated_at")),
    )


def _session_and_user(payload: Mapping[str, Any]) -> tuple[Session, User]:
    access_token = payload.get("access_token")
    if not isinstance(access_token, str) or not access_token:
        raise AuthenticationError(_INVALID_AUTH_RESPONSE)
    refresh_token_value = payload.get("refresh_token")
    refresh_token = (
        refresh_token_value if isinstance(refresh_token_value, str) else None
    )
    user = _user(_mapping(payload.get("user")))
    return (
        Session(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=_optional_int(payload.get("expires_in")),
            user_id=user.id,
        ),
        user,
    )


class Auth:
    """Authenticate users and update client-owned auth state."""

    def __init__(self, client: AuthContext) -> None:
        """Create an authentication facade backed by a client."""
        self._client = client
        self._operation_lock = RLock()
        self._current_device_session_ids: set[str] = set()

    def sign_up(
        self,
        *,
        email: str,
        password: str,
        user_metadata: dict[str, JSONValue] | None = None,
        sign_in: bool = False,
    ) -> SignUpResult:
        """Create an account and optionally sign in when policy permits."""
        response = invoke(
            self._client._transport.auth_signup,
            authorization=self._client._anon_token(),
            email=email,
            password=password,
            user_metadata=user_metadata,
        )
        payload = _mapping(response_payload(response, 201))
        confirmation_required = payload.get("confirmation_required") is True
        message_value = payload.get("message")
        message = message_value if isinstance(message_value, str) else ""
        if sign_in and not confirmation_required:
            session = self.sign_in(email=email, password=password)
            return SignUpResult(
                confirmation_required=False,
                message=message,
                user=self._client.current_user,
                session=session,
            )
        return SignUpResult(
            confirmation_required=confirmation_required,
            message=message,
        )

    def sign_in(self, *, email: str, password: str) -> Session:
        """Sign in a user and replace client-owned auth state."""
        response = invoke(
            self._client._transport.auth_signin,
            authorization=self._client._anon_token(),
            email=email,
            password=password,
        )
        session, user = _session_and_user(_mapping(response_payload(response, 200)))
        self._replace_auth(session, user)
        return session

    def sign_out(self) -> None:
        """Revoke the refresh token and always clear local auth state."""
        with self._operation_lock:
            session = self._client.current_session
            try:
                if session is not None and session.refresh_token is not None:
                    response = invoke(
                        self._client._transport.auth_logout,
                        authorization=self._client._anon_token(),
                        refresh_token=session.refresh_token,
                    )
                    response_payload(response, 204)
            finally:
                self._clear_auth()

    def get_user(self) -> User:
        """Load the current user from the API."""
        with self._operation_lock:
            payload = _mapping(
                self._authenticated_payload(
                    self._client._transport.auth_get_user,
                    expected_status=200,
                )
            )
            user = _user(_mapping(payload.get("user")))
            self._client._set_user(user)
            return user

    def update_user(
        self,
        *,
        password: str | None = None,
        user_metadata: dict[str, JSONValue] | None = None,
    ) -> User:
        """Update the current user's password or metadata."""
        with self._operation_lock:
            payload = _mapping(
                self._authenticated_payload(
                    self._client._transport.auth_update_user,
                    expected_status=200,
                    password=password,
                    user_metadata=user_metadata,
                )
            )
            user = _user(_mapping(payload.get("user")))
            self._client._set_user(user)
            return user

    def refresh_session(self) -> Session:
        """Rotate the current refresh token and replace local auth state."""
        with self._operation_lock:
            return self._refresh_session()

    def _refresh_session(self) -> Session:
        session = self._client.current_session
        if session is None or session.refresh_token is None:
            self._clear_auth()
            raise AuthenticationError(_MISSING_AUTH_STATE)

        succeeded = False
        try:
            response = invoke(
                self._client._transport.auth_refresh,
                authorization=self._client._anon_token(),
                refresh_token=session.refresh_token,
            )
            refreshed, user = _session_and_user(
                _mapping(response_payload(response, 200))
            )
            if refreshed.refresh_token is None:
                raise AuthenticationError(_INVALID_AUTH_RESPONSE)
            self._replace_auth(refreshed, user)
            succeeded = True
            return refreshed
        finally:
            if not succeeded:
                self._clear_auth()

    def on_auth_state_change(
        self,
        listener: Callable[[User | None], None],
    ) -> Callable[[], None]:
        """Observe committed auth state and return an idempotent unsubscribe."""
        return self._client._subscribe_auth(listener)

    def sign_up_anonymous(
        self,
        *,
        user_metadata: dict[str, JSONValue] | None = None,
    ) -> Session:
        """Create an anonymous user and replace client-owned auth state."""
        response = invoke(
            self._client._transport.auth_signup_anonymous,
            authorization=self._client._anon_token(),
            user_metadata=user_metadata,
        )
        session, user = _session_and_user(_mapping(response_payload(response, 201)))
        self._replace_auth(session, user)
        return session

    def convert_anonymous(
        self,
        *,
        email: str,
        password: str,
        user_metadata: dict[str, JSONValue] | None = None,
    ) -> User:
        """Convert the current anonymous user to an email account."""
        with self._operation_lock:
            payload = _mapping(
                self._authenticated_payload(
                    self._client._transport.auth_convert_anonymous,
                    expected_status=200,
                    email=email,
                    password=password,
                    user_metadata=user_metadata,
                )
            )
            converted_user = _user(_mapping(payload.get("user")))
            with suppress(VolcanoError):
                self.refresh_session()
            return self._client.current_user or converted_user

    def confirm_email(self, *, token: str) -> MessageResult:
        """Confirm an email address with its one-time token."""
        response = invoke(
            self._client._transport.auth_confirm_email,
            authorization=self._client._anon_token(),
            token=token,
        )
        result = _message(_mapping(response_payload(response, 200)))
        if self._client.current_session is not None:
            with suppress(VolcanoError):
                self.get_user()
        return result

    def resend_confirmation(self, *, email: str) -> MessageResult:
        """Request another email-confirmation message."""
        response = invoke(
            self._client._transport.auth_resend_confirmation,
            authorization=self._client._anon_token(),
            email=email,
        )
        return _message(_mapping(response_payload(response, 200)))

    def forgot_password(self, *, email: str) -> MessageResult:
        """Request a password-reset message."""
        response = invoke(
            self._client._transport.auth_forgot_password,
            authorization=self._client._anon_token(),
            email=email,
        )
        return _message(_mapping(response_payload(response, 200)))

    def reset_password(self, *, token: str, new_password: str) -> MessageResult:
        """Reset a password with its one-time recovery token."""
        response = invoke(
            self._client._transport.auth_reset_password,
            authorization=self._client._anon_token(),
            token=token,
            new_password=new_password,
        )
        result = _message(_mapping(response_payload(response, 200)))
        if self._client.current_session is not None:
            with suppress(VolcanoError):
                self.get_user()
        return result

    def request_email_change(self, *, new_email: str) -> EmailChangeResult:
        """Request a change to the current user's email address."""
        payload = _mapping(
            self._authenticated_payload(
                self._client._transport.auth_request_email_change,
                expected_status=200,
                new_email=new_email,
            )
        )
        message = payload.get("message")
        response_email = payload.get("new_email")
        if not isinstance(message, str) or not isinstance(response_email, str):
            raise AuthenticationError(_INVALID_AUTH_RESPONSE)
        return EmailChangeResult(
            message=message,
            new_email=response_email,
            email_change_token=_optional_text(payload.get("email_change_token")),
        )

    def confirm_email_change(self, *, token: str) -> MessageResult:
        """Confirm a pending email change."""
        with self._operation_lock:
            payload = self._authenticated_payload(
                self._client._transport.auth_confirm_email_change,
                expected_status=200,
                email_change_token=token,
            )
            response = _mapping(payload)
            self._client._set_user(_user(_mapping(response.get("user"))))
            return _message(response)

    def cancel_email_change(self) -> MessageResult:
        """Cancel the current user's pending email change."""
        payload = self._authenticated_payload(
            self._client._transport.auth_cancel_email_change,
            expected_status=200,
        )
        return _message(_mapping(payload))

    def get_hosted_auth_url(
        self,
        *,
        project_id: str,
        action: Literal["login", "signup", "forgot-password"] | None = None,
    ) -> AuthorizationRequest:
        """Build a hosted-auth URL without navigating a browser."""
        state = token_urlsafe(32)
        query = {"anon_key": self._client._anon_token()}
        if action is not None:
            query["action"] = action
        query["state"] = state
        url = (
            f"{self._client._api_url}/projects/{quote(project_id, safe='')}/auth/hosted"
            f"?{urlencode(query)}"
        )
        return AuthorizationRequest(authorization_url=url, state=state)

    def get_oauth_authorization_url(
        self,
        *,
        provider: OAuthProviderName,
        redirect_url: str,
    ) -> AuthorizationRequest:
        """Start an OAuth flow and return its provider authorization URL."""
        validated_provider = _provider(provider)
        state = token_urlsafe(32)
        response = invoke(
            self._client._transport.auth_oauth_authorize,
            authorization=self._client._anon_token(),
            provider=validated_provider,
            redirect_url=redirect_url,
            state=state,
        )
        response_payload(response, 307)
        authorization_url = self._response_header(response, "Location")
        if authorization_url is None:
            raise AuthenticationError(_MISSING_AUTHORIZATION_URL)
        return AuthorizationRequest(
            authorization_url=authorization_url,
            state=state,
        )

    def exchange_oauth_code(
        self,
        *,
        code: str,
        redirect_url: str,
        state: str,
        expected_state: str,
    ) -> Session:
        """Validate caller state and exchange an OAuth code for a session."""
        if not compare_digest(state.encode(), expected_state.encode()):
            raise ValidationError(_INVALID_OAUTH_STATE)
        response = invoke(
            self._client._transport.auth_oauth_exchange,
            authorization=self._client._anon_token(),
            code=code,
            redirect_url=redirect_url,
        )
        session, user = _session_and_user(_mapping(response_payload(response, 200)))
        self._replace_auth(session, user)
        return session

    def link_oauth_provider(
        self,
        *,
        provider: OAuthProviderName,
        redirect_url: str,
    ) -> AuthorizationRequest:
        """Start a flow that links an OAuth provider to the current user."""
        validated_provider = _provider(provider)
        state = token_urlsafe(32)
        payload = _mapping(
            self._authenticated_payload(
                self._client._transport.auth_link_oauth_provider,
                expected_status=200,
                provider=validated_provider,
                redirect_url=redirect_url,
                state=state,
            )
        )
        authorization_url = payload.get("authorization_url")
        if not isinstance(authorization_url, str):
            raise AuthenticationError(_MISSING_AUTHORIZATION_URL)
        return AuthorizationRequest(
            authorization_url=authorization_url,
            state=state,
        )

    def unlink_oauth_provider(self, *, provider: OAuthProviderName) -> None:
        """Unlink an OAuth provider from the current user."""
        self._authenticated_payload(
            self._client._transport.auth_unlink_oauth_provider,
            expected_status=204,
            provider=_provider(provider),
        )

    def get_linked_oauth_providers(self) -> tuple[OAuthProvider, ...]:
        """Return OAuth providers linked to the current user."""
        payload = _mapping(
            self._authenticated_payload(
                self._client._transport.auth_list_oauth_providers,
                expected_status=200,
            )
        )
        providers_value = payload.get("providers")
        if not isinstance(providers_value, list):
            raise AuthenticationError(_INVALID_AUTH_RESPONSE)
        providers = cast("list[object]", providers_value)
        return tuple(
            OAuthProvider(
                provider=_provider(str(provider_payload.get("provider"))),
                linked_at=_optional_datetime(provider_payload.get("linked_at")),
                updated_at=_optional_datetime(provider_payload.get("updated_at")),
            )
            for provider_payload in (_mapping(item) for item in providers)
        )

    def refresh_oauth_token(
        self,
        *,
        provider: OAuthProviderName,
    ) -> OAuthTokenResult:
        """Refresh the stored access token for an OAuth provider."""
        payload = self._authenticated_payload(
            self._client._transport.refresh_oauth_provider_token,
            expected_status=200,
            provider=_provider(provider),
        )
        return _oauth_token(_mapping(payload))

    def get_oauth_provider_token(
        self,
        *,
        provider: OAuthProviderName,
    ) -> OAuthTokenResult:
        """Get metadata for the current OAuth provider token."""
        payload = self._authenticated_payload(
            self._client._transport.get_oauth_provider_token,
            expected_status=200,
            provider=_provider(provider),
        )
        return _oauth_token(_mapping(payload))

    def call_oauth_api(
        self,
        *,
        provider: OAuthProviderName,
        endpoint: str,
        method: Literal["GET", "POST"] = "GET",
        body: dict[str, JSONValue] | None = None,
    ) -> JSONValue:
        """Call a provider API through Volcano's fixed-host proxy."""
        with self._operation_lock:
            arguments = {
                "provider": _provider(provider),
                "endpoint": endpoint,
                "method": method,
                "body": body,
            }
            try:
                payload = self._provider_api_payload(arguments)
            except AuthenticationError as error:
                session = self._client.current_session
                if (
                    error.status != _HTTP_UNAUTHORIZED
                    or session is None
                    or session.refresh_token is None
                    or "not linked" in str(error).lower()
                ):
                    raise
                self.refresh_session()
                payload = self._provider_api_payload(arguments)
        return _json_value(payload)

    def _provider_api_payload(self, arguments: Mapping[str, object]) -> object:
        return self._authenticated_payload(
            self._client._transport.call_oauth_provider_api,
            expected_status=200,
            retry_unauthorized=False,
            **arguments,
        )

    def get_sessions(self, *, page: int = 1, limit: int = 20) -> SessionPage:
        """Return a page of the current user's device sessions."""
        with self._operation_lock:
            payload = _mapping(
                self._authenticated_payload(
                    self._client._transport.auth_get_my_sessions,
                    expected_status=200,
                    page=page,
                    limit=limit,
                )
            )
            sessions_value = payload.get("sessions", payload.get("data"))
            if not isinstance(sessions_value, list):
                raise AuthenticationError(_INVALID_AUTH_RESPONSE)
            sessions = cast("list[object]", sessions_value)
            mapped_sessions = tuple(_auth_session(_mapping(item)) for item in sessions)
            self._current_device_session_ids.update(
                session.id for session in mapped_sessions if session.is_current
            )
            return SessionPage(
                sessions=mapped_sessions,
                total=_optional_int(payload.get("total")),
                page=_optional_int(payload.get("page")),
                limit=_optional_int(payload.get("limit")),
                total_pages=_optional_int(payload.get("total_pages")),
            )

    def delete_session(self, *, session_id: str) -> None:
        """Delete one device session."""
        with self._operation_lock:
            try:
                normalized_session_id = str(UUID(session_id))
            except (TypeError, ValueError, AttributeError) as error:
                raise ValidationError(_INVALID_SESSION_ID) from error
            deletes_current_session = (
                normalized_session_id in self._current_device_session_ids
            )
            self._authenticated_payload(
                self._client._transport.auth_delete_my_session,
                expected_status=204,
                session_id=normalized_session_id,
            )
            if deletes_current_session:
                self._clear_auth()

    def delete_all_other_sessions(self) -> None:
        """Delete every device session except the current one."""
        self._authenticated_payload(
            self._client._transport.auth_delete_all_my_sessions,
            expected_status=204,
        )

    @staticmethod
    def _response_header(response: TransportResponse, name: str) -> str | None:
        if response.headers is None:
            return None
        for key, value in response.headers.items():
            if key.lower() == name.lower():
                return value
        return None

    def _authenticated_payload(
        self,
        operation: Callable[..., TransportResponse],
        *,
        expected_status: int,
        retry_unauthorized: bool = True,
        **kwargs: object,
    ) -> object:
        with self._operation_lock:
            return self._authenticated_payload_locked(
                operation,
                expected_status=expected_status,
                retry_unauthorized=retry_unauthorized,
                **kwargs,
            )

    def _authenticated_payload_locked(
        self,
        operation: Callable[..., TransportResponse],
        *,
        expected_status: int,
        retry_unauthorized: bool,
        **kwargs: object,
    ) -> object:
        try:
            response = invoke(
                operation,
                authorization=self._client._session_token(),
                **kwargs,
            )
            return response_payload(response, expected_status)
        except AuthenticationError as error:
            session = self._client.current_session
            if (
                error.status != _HTTP_UNAUTHORIZED
                or session is None
                or not retry_unauthorized
            ):
                raise
            if session.refresh_token is None:
                self._clear_auth()
                raise
        self.refresh_session()
        response = invoke(
            operation,
            authorization=self._client._session_token(),
            **kwargs,
        )
        try:
            return response_payload(response, expected_status)
        except AuthenticationError as error:
            if error.status == _HTTP_UNAUTHORIZED:
                self._clear_auth()
            raise

    def _replace_auth(self, session: Session, user: User) -> None:
        with self._operation_lock:
            self._current_device_session_ids.clear()
            self._client._commit_auth(session, user)

    def _clear_auth(self) -> None:
        with self._operation_lock:
            self._current_device_session_ids.clear()
            self._client._clear_auth()
