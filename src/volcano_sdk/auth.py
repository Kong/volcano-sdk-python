"""Authentication facade."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, TypeVar, cast

from ._generated.models.auth_get_user_response_200 import AuthGetUserResponse200
from ._generated.models.auth_update_user_response_200 import AuthUpdateUserResponse200
from ._generated.types import Unset
from ._transport import (
    AuthConfirmEmailTransport,
    AuthForgotPasswordTransport,
    AuthGetUserTransport,
    AuthLogoutTransport,
    AuthRefreshTransport,
    AuthResendConfirmationTransport,
    AuthResetPasswordTransport,
    AuthSignUpTransport,
    AuthUpdateUserTransport,
    Transport,
    invoke,
    response_payload,
)
from .errors import AuthenticationError, SessionChangedError, VolcanoError
from .models import JSONValue, Session, SignUpResult, User

_INCOMPLETE_SESSION = "Expected a complete Session"
_INVALID_SIGN_UP_RESULT = "Expected a complete sign-up acknowledgement"
_INVALID_USER = "Expected a complete user profile"
_NO_ACTIVE_SESSION = "No active session"
_T = TypeVar("_T")


def _is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _has_complete_values(session: Session) -> bool:
    return all(
        _is_non_empty_string(value)
        for value in (
            session.access_token,
            session.refresh_token,
            session.user_id,
        )
    )


def _copy_complete_session(session: object) -> Session:
    if not isinstance(session, Session) or not _has_complete_values(session):
        raise ValueError(_INCOMPLETE_SESSION)
    return Session(
        access_token=session.access_token,
        refresh_token=session.refresh_token,
        user_id=session.user_id,
    )


def _session_from_payload(payload: object) -> Session:
    values: Mapping[object, object] = (
        cast("Mapping[object, object]", payload) if isinstance(payload, Mapping) else {}
    )
    raw_user = values.get("user")
    user: Mapping[object, object] = (
        cast("Mapping[object, object]", raw_user)
        if isinstance(raw_user, Mapping)
        else {}
    )
    return _copy_complete_session(
        Session(
            access_token=cast("str", values.get("access_token")),
            refresh_token=cast("str", values.get("refresh_token")),
            user_id=cast("str", user.get("id")),
        )
    )


def _sign_up_result_from_payload(payload: object) -> SignUpResult:
    values: Mapping[object, object] = (
        cast("Mapping[object, object]", payload) if isinstance(payload, Mapping) else {}
    )
    confirmation_required = values.get("confirmation_required")
    message = values.get("message")
    if not isinstance(confirmation_required, bool) or not isinstance(message, str):
        raise TypeError(_INVALID_SIGN_UP_RESULT)
    return SignUpResult(
        confirmation_required=confirmation_required,
        message=message,
    )


def _user_from_payload(payload: object) -> User:
    if not isinstance(
        payload,
        (AuthGetUserResponse200, AuthUpdateUserResponse200),
    ) or isinstance(payload.user, Unset):
        raise AuthenticationError(_INVALID_USER)
    user = payload.user
    project_id = _none_if_unset(user.project_id)
    user_metadata = _none_if_unset(user.user_metadata)
    app_metadata = _none_if_unset(user.app_metadata)
    return User(
        id=str(user.id),
        email=user.email,
        status=user.status,
        project_id=None if project_id is None else str(project_id),
        email_confirmed=_none_if_unset(user.email_confirmed),
        user_metadata=(
            None
            if user_metadata is None
            else cast("Mapping[str, JSONValue]", user_metadata.to_dict())
        ),
        app_metadata=(
            None
            if app_metadata is None
            else cast("Mapping[str, JSONValue]", app_metadata.to_dict())
        ),
        avatar_url=_none_if_unset(user.avatar_url),
        banned_until=_none_if_unset(user.banned_until),
        last_sign_in_at=_none_if_unset(user.last_sign_in_at),
        created_at=_none_if_unset(user.created_at),
        updated_at=_none_if_unset(user.updated_at),
    )


def _none_if_unset(value: _T | Unset) -> _T | None:
    return None if isinstance(value, Unset) else value


class AuthContext(Protocol):
    """Client capabilities required by the authentication facade."""

    _transport: Transport

    @property
    def current_session(self) -> Session | None:
        """Return the locally held session, if one exists."""
        ...

    def _anon_token(self) -> str: ...

    def _set_session(self, session: Session) -> None: ...

    def _capture_session(self) -> tuple[int, Session | None]: ...

    def _set_session_if_current(self, session: Session, generation: int) -> bool: ...

    def _clear_session_if_current(self, generation: int) -> bool: ...


class Auth:
    """Authenticate users and update the client session."""

    def __init__(self, client: AuthContext) -> None:
        """Create an authentication facade backed by a client."""
        self._client = client

    def get_session(self) -> Session | None:
        """Return the immutable locally held session without validating it."""
        return self._client.current_session

    def set_session(self, session: Session) -> Session:
        """Copy a complete session into local client state."""
        owned = _copy_complete_session(session)
        self._client._set_session(owned)
        return owned

    def sign_up(
        self,
        *,
        email: str,
        password: str,
        metadata: Mapping[str, object] | None = None,
    ) -> SignUpResult:
        """Create an account without creating or replacing a local session."""
        transport = cast("AuthSignUpTransport", self._client._transport)
        response = invoke(
            transport.auth_signup,
            authorization=self._client._anon_token(),
            email=email,
            password=password,
            metadata=dict(metadata or {}),
        )
        return _sign_up_result_from_payload(response_payload(response, 201))

    def reset_password_for_email(self, *, email: str) -> None:
        """Request a reset email without revealing whether the account exists."""
        transport = cast("AuthForgotPasswordTransport", self._client._transport)
        response = invoke(
            transport.auth_forgot_password,
            authorization=self._client._anon_token(),
            email=email,
        )
        response_payload(response, 200)

    def confirm_email(self, *, token: str) -> None:
        """Confirm an email with its token without changing local state."""
        transport = cast("AuthConfirmEmailTransport", self._client._transport)
        response = invoke(
            transport.auth_confirm_email,
            authorization=self._client._anon_token(),
            token=token,
        )
        response_payload(response, 200)

    def resend_confirmation(self, *, email: str) -> None:
        """Request a generic confirmation resend without changing local state."""
        transport = cast("AuthResendConfirmationTransport", self._client._transport)
        response = invoke(
            transport.auth_resend_confirmation,
            authorization=self._client._anon_token(),
            email=email,
        )
        response_payload(response, 200)

    def reset_password(self, *, token: str, new_password: str) -> None:
        """Set a new password with a recovery token without changing local state."""
        transport = cast("AuthResetPasswordTransport", self._client._transport)
        response = invoke(
            transport.auth_reset_password,
            authorization=self._client._anon_token(),
            token=token,
            new_password=new_password,
        )
        response_payload(response, 200)

    def get_user(self) -> User:
        """Load a server-validated profile for the current session."""
        generation, current = self._client._capture_session()
        if current is None:
            raise AuthenticationError(_NO_ACTIVE_SESSION)
        transport = cast("AuthGetUserTransport", self._client._transport)
        response = invoke(transport.auth_get_user, authorization=current.access_token)
        user = _user_from_payload(response_payload(response, 200))
        if self._client._capture_session()[0] != generation:
            raise SessionChangedError
        return user

    def update_user(
        self,
        *,
        password: str | None = None,
        metadata: Mapping[str, object] | None = None,
    ) -> User:
        """Update and return the current user's server-validated profile."""
        generation, current = self._client._capture_session()
        if current is None:
            raise AuthenticationError(_NO_ACTIVE_SESSION)
        transport = cast("AuthUpdateUserTransport", self._client._transport)
        response = invoke(
            transport.auth_update_user,
            authorization=current.access_token,
            password=password,
            metadata=None if metadata is None else dict(metadata),
        )
        user = _user_from_payload(response_payload(response, 200))
        if self._client._capture_session()[0] != generation:
            raise SessionChangedError
        return user

    def sign_in(self, *, email: str, password: str) -> Session:
        """Sign in a user and store the returned session."""
        response = invoke(
            self._client._transport.auth_signin,
            authorization=self._client._anon_token(),
            email=email,
            password=password,
        )
        payload = response_payload(response, 200)
        session = _session_from_payload(payload)
        self._client._set_session(session)
        return session

    def refresh_session(self) -> Session:
        """Refresh and replace the current session."""
        generation, current = self._client._capture_session()
        if current is None:
            raise AuthenticationError(_NO_ACTIVE_SESSION)

        transport = cast("AuthRefreshTransport", self._client._transport)
        response = invoke(
            transport.auth_refresh,
            authorization=self._client._anon_token(),
            refresh_token=current.refresh_token,
        )
        try:
            payload = response_payload(response, 200)
        except AuthenticationError:
            self._client._clear_session_if_current(generation)
            raise
        refreshed = _session_from_payload(payload)
        if not self._client._set_session_if_current(refreshed, generation):
            raise SessionChangedError
        return refreshed

    def sign_out(self) -> None:
        """Revoke and clear the current session."""
        generation, current = self._client._capture_session()
        if current is None:
            return
        transport = cast("AuthLogoutTransport", self._client._transport)
        error: VolcanoError | None = None
        try:
            response = invoke(
                transport.auth_logout,
                authorization=self._client._anon_token(),
                refresh_token=current.refresh_token,
            )
            response_payload(response, 204)
        except VolcanoError as caught:
            error = caught
        if not self._client._clear_session_if_current(generation):
            raise SessionChangedError from error
        if error is not None:
            raise error
