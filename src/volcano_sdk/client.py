"""Top-level Volcano client."""

from __future__ import annotations

import threading
from collections import deque
from contextlib import suppress

from ._transport import GeneratedTransport, Transport
from .auth import Auth
from .database import Database
from .locks import Locks
from .models import (
    AuthChangeEvent,
    AuthStateCallback,
    AuthSubscription,
    Session,
)
from .realtime import CentrifugeFactory, Realtime
from .storage import Storage

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
        self._auth_callbacks: dict[int, AuthStateCallback] = {}
        self._next_auth_callback_id = 0
        self._auth_notifications: deque[
            tuple[
                tuple[int, ...],
                AuthChangeEvent,
                Session | None,
            ]
        ] = deque()
        self._dispatching_auth_notifications = False
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

    def _set_session(
        self,
        session: Session,
        *,
        event: AuthChangeEvent = "SIGNED_IN",
    ) -> None:
        with self._session_lock:
            self._current_session = session
            self._session_generation += 1
            callback_ids = tuple(self._auth_callbacks)
            dispatch = self._enqueue_auth_state_change(callback_ids, event, session)
        if dispatch:
            self._drain_auth_state_changes()

    def _capture_session(self) -> tuple[int, Session | None]:
        with self._session_lock:
            return self._session_generation, self._current_session

    def _set_session_if_current(
        self,
        session: Session,
        generation: int,
        *,
        event: AuthChangeEvent = "SIGNED_IN",
    ) -> bool:
        with self._session_lock:
            if generation != self._session_generation:
                return False
            self._current_session = session
            self._session_generation += 1
            callback_ids = tuple(self._auth_callbacks)
            dispatch = self._enqueue_auth_state_change(callback_ids, event, session)
        if dispatch:
            self._drain_auth_state_changes()
        return True

    def _clear_session_if_current(
        self,
        generation: int,
        *,
        event: AuthChangeEvent = "SIGNED_OUT",
    ) -> bool:
        with self._session_lock:
            if generation != self._session_generation:
                return False
            self._current_session = None
            self._session_generation += 1
            callback_ids = tuple(self._auth_callbacks)
            dispatch = self._enqueue_auth_state_change(callback_ids, event, None)
        if dispatch:
            self._drain_auth_state_changes()
        return True

    def _subscribe_auth_state_change(
        self,
        callback: AuthStateCallback,
    ) -> AuthSubscription:
        with self._session_lock:
            callback_id = self._next_auth_callback_id
            self._next_auth_callback_id += 1
            self._auth_callbacks[callback_id] = callback
            current = self._current_session
            dispatch = self._enqueue_auth_state_change(
                (callback_id,),
                "INITIAL_SESSION",
                current,
            )
        if dispatch:
            self._drain_auth_state_changes()
        return AuthSubscription(
            lambda: self._unsubscribe_auth_state_change(callback_id)
        )

    def _unsubscribe_auth_state_change(self, callback_id: int) -> None:
        with self._session_lock:
            self._auth_callbacks.pop(callback_id, None)

    def _enqueue_auth_state_change(
        self,
        callback_ids: tuple[int, ...],
        event: AuthChangeEvent,
        session: Session | None,
    ) -> bool:
        if not callback_ids:
            return False
        self._auth_notifications.append((callback_ids, event, session))
        if self._dispatching_auth_notifications:
            return False
        self._dispatching_auth_notifications = True
        return True

    def _drain_auth_state_changes(self) -> None:
        completed = False
        try:
            while True:
                with self._session_lock:
                    if not self._auth_notifications:
                        self._dispatching_auth_notifications = False
                        completed = True
                        return
                    callback_ids, event, session = self._auth_notifications.popleft()
                self._notify_auth_state_change(callback_ids, event, session)
        finally:
            if not completed:
                with self._session_lock:
                    self._auth_notifications.clear()
                    self._dispatching_auth_notifications = False

    def _notify_auth_state_change(
        self,
        callback_ids: tuple[int, ...],
        event: AuthChangeEvent,
        session: Session | None,
    ) -> None:
        for callback_id in callback_ids:
            with self._session_lock:
                callback = self._auth_callbacks.get(callback_id)
            if callback is None:
                continue
            with suppress(Exception):
                callback(event, session)
