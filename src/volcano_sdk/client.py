"""Top-level Volcano client."""

from __future__ import annotations

import logging
from contextlib import suppress
from threading import RLock
from typing import TYPE_CHECKING, TypedDict, Unpack, cast

from ._transport import GeneratedTransport, Transport
from .auth import Auth
from .database import Database
from .locks import Locks
from .models import Session, User
from .realtime import CentrifugeFactory, Realtime
from .storage import Storage

if TYPE_CHECKING:
    from collections.abc import Callable

_NO_ACTIVE_SESSION = "No active session"
_NO_SERVICE_KEY = "No service key configured"
_REFRESH_WITHOUT_ACCESS = "refresh_token requires access_token"
_AUTH_LISTENER_FAILED = "Authentication state listener failed"

_LOGGER = logging.getLogger(__name__)
_AUTH_BOOTSTRAP_KEYS = frozenset({"access_token", "refresh_token"})


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
        _transport: object | None = None,
        _realtime_client_factory: CentrifugeFactory | None = None,
        **auth_bootstrap: Unpack[_AuthBootstrap],
    ) -> None:
        """Create a client for a Volcano project."""
        self._api_url = api_url.rstrip("/")
        self._anon_key = anon_key
        self._service_key = service_key
        unknown_auth = auth_bootstrap.keys() - _AUTH_BOOTSTRAP_KEYS
        if unknown_auth:
            unexpected = next(iter(unknown_auth))
            message = f"unexpected authentication keyword: {unexpected}"
            raise TypeError(message)
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
        self._auth_state_lock = RLock()
        self._auth_listeners: dict[int, Callable[[User | None], None]] = {}
        self._next_auth_listener_id = 0
        self._transport: Transport = (
            cast("Transport", _transport)
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
        with self._auth_state_lock:
            return self._current_session

    @property
    def current_user(self) -> User | None:
        """Return the authenticated user, if one has been loaded."""
        with self._auth_state_lock:
            return self._current_user

    def database(self, name: str) -> Database:
        """Create a query facade for a project database."""
        return Database(self, name)

    def _anon_token(self) -> str:
        return self._anon_key

    def _session_token(self) -> str:
        with self._auth_state_lock:
            if self._current_session is None:
                raise RuntimeError(_NO_ACTIVE_SESSION)
            return self._current_session.access_token

    def _service_token(self) -> str:
        if self._service_key is None:
            raise RuntimeError(_NO_SERVICE_KEY)
        return self._service_key

    def _set_session(self, session: Session) -> None:
        with self._auth_state_lock:
            self._current_session = session
            self.realtime.on_auth_change()

    def _commit_auth(self, session: Session, user: User) -> None:
        with self._auth_state_lock:
            self._current_session = session
            self._current_user = user
            self.realtime.on_auth_change()
            self._notify_auth_listeners()

    def _set_user(self, user: User) -> None:
        with self._auth_state_lock:
            self._current_user = user
            self._notify_auth_listeners()

    def _clear_auth(self) -> None:
        with self._auth_state_lock:
            self._current_session = None
            self._current_user = None
            self.realtime.on_auth_change()
            self._notify_auth_listeners()

    def _subscribe_auth(
        self,
        listener: Callable[[User | None], None],
    ) -> Callable[[], None]:
        with self._auth_state_lock:
            listener_id = self._next_auth_listener_id
            self._next_auth_listener_id += 1
            self._auth_listeners[listener_id] = listener
            if self._current_session is None or self._current_user is not None:
                self._invoke_auth_listener(listener)

        def unsubscribe() -> None:
            with self._auth_state_lock:
                self._auth_listeners.pop(listener_id, None)

        return unsubscribe

    def _notify_auth_listeners(self) -> None:
        for listener in tuple(self._auth_listeners.values()):
            self._invoke_auth_listener(listener)

    def _invoke_auth_listener(
        self,
        listener: Callable[[User | None], None],
    ) -> None:
        completed = False
        with suppress(Exception):
            listener(self._current_user)
            completed = True
        if not completed:
            _LOGGER.error(_AUTH_LISTENER_FAILED)
