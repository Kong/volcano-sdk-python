"""Authentication facade."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, cast

from ._transport import (
    AuthGetUserTransport,
    AuthLogoutTransport,
    AuthRefreshTransport,
    AuthSignUpTransport,
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
    values: Mapping[object, object] = (
        cast("Mapping[object, object]", payload) if isinstance(payload, Mapping) else {}
    )
    raw_user = values.get("user")
    user: Mapping[object, object] = (
        cast("Mapping[object, object]", raw_user)
        if isinstance(raw_user, Mapping)
        else {}
    )
    user_id = user.get("id")
    email = user.get("email")
    status = user.get("status")
    email_confirmed = user.get("email_confirmed")
    metadata = user.get("user_metadata")
    valid = all(_is_non_empty_string(value) for value in (user_id, email, status))
    valid = valid and (email_confirmed is None or isinstance(email_confirmed, bool))
    valid = valid and (metadata is None or isinstance(metadata, Mapping))
    if not valid:
        raise AuthenticationError(_INVALID_USER)
    return User(
        id=cast("str", user_id),
        email=cast("str", email),
        status=cast("str", status),
        email_confirmed=cast("bool | None", email_confirmed),
        user_metadata=cast("Mapping[str, JSONValue] | None", metadata),
    )


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
