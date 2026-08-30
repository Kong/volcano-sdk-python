"""Top-level Volcano client."""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING

from ._transport import GeneratedTransport, Transport
from .auth import Auth
from .database import Database
from .locks import Locks
from .realtime import CentrifugeFactory, Realtime
from .storage import Storage

if TYPE_CHECKING:
    from .models import Session

_NO_ACTIVE_SESSION = "No active session"
_NO_SERVICE_KEY = "No service key configured"


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
    ) -> None:
        """Create a client for a Volcano project."""
        self._api_url = api_url.rstrip("/")
        self._anon_key = anon_key
        self._service_key = service_key
        self._session_lock = threading.Lock()
        self._session_generation = 0
        self._current_session: Session | None = None
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
        return self._capture_session()[1]

    def database(self, name: str) -> Database:
        """Create a query facade for a project database."""
        return Database(self, name)

    def _anon_token(self) -> str:
        return self._anon_key

    def _session_token(self) -> str:
        session = self._capture_session()[1]
        if session is None:
            raise RuntimeError(_NO_ACTIVE_SESSION)
        return session.access_token

    def _service_token(self) -> str:
        if self._service_key is None:
            raise RuntimeError(_NO_SERVICE_KEY)
        return self._service_key

    def _set_session(self, session: Session) -> None:
        with self._session_lock:
            self._current_session = session
            self._session_generation += 1

    def _capture_session(self) -> tuple[int, Session | None]:
        with self._session_lock:
            return self._session_generation, self._current_session

    def _set_session_if_current(self, session: Session, generation: int) -> bool:
        with self._session_lock:
            if generation != self._session_generation:
                return False
            self._current_session = session
            self._session_generation += 1
            return True

    def _clear_session_if_current(self, generation: int) -> bool:
        with self._session_lock:
            if generation != self._session_generation:
                return False
            self._current_session = None
            self._session_generation += 1
            return True
