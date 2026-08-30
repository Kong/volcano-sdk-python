"""Authentication facade."""

from __future__ import annotations

from typing import Protocol

from ._transport import Transport, invoke, response_payload
from .models import Session

_INCOMPLETE_SESSION = "Expected a complete Session"


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


class AuthContext(Protocol):
    """Client capabilities required by the authentication facade."""

    _transport: Transport

    @property
    def current_session(self) -> Session | None:
        """Return the locally held session, if one exists."""
        ...

    def _anon_token(self) -> str: ...

    def _set_session(self, session: Session) -> None: ...


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

    def sign_in(self, *, email: str, password: str) -> Session:
        """Sign in a user and store the returned session."""
        response = invoke(
            self._client._transport.auth_signin,
            authorization=self._client._anon_token(),
            email=email,
            password=password,
        )
        payload = response_payload(response, 200)
        session = Session(
            access_token=payload["access_token"],
            refresh_token=payload["refresh_token"],
            user_id=payload["user"]["id"],
        )
        self._client._set_session(session)
        return session
