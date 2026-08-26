from __future__ import annotations

from typing import Protocol

from ._transport import Transport, invoke, response_payload
from .models import Session


class AuthContext(Protocol):
    _transport: Transport

    def _anon_token(self) -> str: ...

    def _set_session(self, session: Session) -> None: ...


class Auth:
    def __init__(self, client: AuthContext) -> None:
        self._client = client

    def sign_in(self, *, email: str, password: str) -> Session:
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
