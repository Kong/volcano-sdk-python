"""Authentication facade."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import TYPE_CHECKING, Any, Protocol, cast

from ._transport import Transport, TransportResponse, invoke, response_payload
from .errors import AuthenticationError
from .models import Session, SignUpResult, User

if TYPE_CHECKING:
    from collections.abc import Callable

    from .models import JSONValue

_INVALID_AUTH_RESPONSE = "Authentication response is missing required fields"
_MISSING_AUTH_STATE = "No refresh token available"
_HTTP_UNAUTHORIZED = 401


class AuthContext(Protocol):
    """Client capabilities required by the authentication facade."""

    _transport: Transport

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
        self._client._commit_auth(session, user)
        return session

    def sign_out(self) -> None:
        """Revoke the refresh token and always clear local auth state."""
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
            self._client._clear_auth()

    def get_user(self) -> User:
        """Load the current user from the API."""
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
        session = self._client.current_session
        if session is None or session.refresh_token is None:
            self._client._clear_auth()
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
            self._client._commit_auth(refreshed, user)
            succeeded = True
            return refreshed
        finally:
            if not succeeded:
                self._client._clear_auth()

    def on_auth_state_change(
        self,
        listener: Callable[[User | None], None],
    ) -> Callable[[], None]:
        """Observe committed auth state and return an idempotent unsubscribe."""
        return self._client._subscribe_auth(listener)

    def _authenticated_payload(
        self,
        operation: Callable[..., TransportResponse],
        *,
        expected_status: int,
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
                or session.refresh_token is None
            ):
                raise
        self.refresh_session()
        response = invoke(
            operation,
            authorization=self._client._session_token(),
            **kwargs,
        )
        return response_payload(response, expected_status)
