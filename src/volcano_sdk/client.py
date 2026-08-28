"""Top-level Volcano client."""

from __future__ import annotations

from typing import TypedDict, Unpack

from ._transport import GeneratedTransport, Transport
from .auth import Auth
from .database import Database
from .locks import Locks
from .models import Session, User
from .realtime import CentrifugeFactory, Realtime
from .storage import Storage

_NO_ACTIVE_SESSION = "No active session"
_NO_SERVICE_KEY = "No service key configured"
_REFRESH_WITHOUT_ACCESS = "refresh_token requires access_token"


class _AuthBootstrap(TypedDict, total=False):
    access_token: str | None
    refresh_token: str | None


class VolcanoClient:
    """Volcano SDK entry point."""

    def __init__(
        self,
        *,
        anon_key: str,
        api_url: str = "https://api.volcano.dev",
        service_key: str | None = None,
        timeout: float = 60.0,
        _transport: Transport | None = None,
        _realtime_client_factory: CentrifugeFactory | None = None,
        **auth_bootstrap: Unpack[_AuthBootstrap],
    ) -> None:
        """Create a client for a Volcano project."""
        self._api_url = api_url.rstrip("/")
        self._anon_key = anon_key
        self._service_key = service_key
        access_token = auth_bootstrap.get("access_token")
        refresh_token = auth_bootstrap.get("refresh_token")
        if access_token is None and refresh_token is not None:
            raise ValueError(_REFRESH_WITHOUT_ACCESS)
        self._current_session = (
            Session(access_token=access_token, refresh_token=refresh_token)
            if access_token is not None
            else None
        )
        self._current_user: User | None = None
        self._transport: Transport = (
            _transport
            if _transport is not None
            else GeneratedTransport(api_url=self._api_url, timeout=timeout)
        )
        self.auth = Auth(self)
        self.storage = Storage(self)
        self.locks = Locks(self)
        if _realtime_client_factory is None:
            self.realtime = Realtime(self, api_url=self._api_url)
        else:
            self.realtime = Realtime(
                self,
                api_url=self._api_url,
                client_factory=_realtime_client_factory,
            )

    @property
    def current_session(self) -> Session | None:
        """Return the authenticated session, if one exists."""
        return self._current_session

    @property
    def current_user(self) -> User | None:
        """Return the authenticated user, if one has been loaded."""
        return self._current_user

    def database(self, name: str) -> Database:
        """Create a query facade for a project database."""
        return Database(self, name)

    def _anon_token(self) -> str:
        return self._anon_key

    def _session_token(self) -> str:
        if self._current_session is None:
            raise RuntimeError(_NO_ACTIVE_SESSION)
        return self._current_session.access_token

    def _service_token(self) -> str:
        if self._service_key is None:
            raise RuntimeError(_NO_SERVICE_KEY)
        return self._service_key

    def _set_session(self, session: Session) -> None:
        self._current_session = session

    def _commit_auth(self, session: Session, user: User) -> None:
        self._current_session = session
        self._current_user = user

    def _set_user(self, user: User) -> None:
        self._current_user = user

    def _clear_auth(self) -> None:
        self._current_session = None
        self._current_user = None
