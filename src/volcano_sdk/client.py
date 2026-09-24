"""Top-level Volcano client."""

from __future__ import annotations

import threading
from collections import deque
from dataclasses import replace
from itertools import count
from typing import TYPE_CHECKING, Unpack
from uuid import UUID

from ._auth_requests import AuthRequests
from ._client_context import ClientContext
from ._client_session import BootstrapCredentials, CallbackOutcome, bootstrap_session
from ._session import validate_refresh_identity
from ._session_operations import SessionOperations
from ._transport import GeneratedTransport, Transport
from .auth import Auth, AuthContext
from .database import Database
from .durable import Durable
from .errors import AuthenticationError
from .functions import Functions
from .locks import Locks
from .logs import Logs
from .models import (
    AuthChangeEvent,
    AuthStateCallback,
    AuthSubscription,
    JSONValue,
    Session,
)
from .realtime import CentrifugeFactory, Realtime
from .storage import Storage

if TYPE_CHECKING:
    from _thread import LockType
    from collections.abc import Callable, Mapping

_NO_ACTIVE_SESSION = "No active session"
_NO_SERVICE_KEY = "No service key configured"
_PROFILE_USER_MISMATCH = "Profile user does not match the active session"


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
        **credentials: Unpack[BootstrapCredentials],
    ) -> None:
        """Create a client for a Volcano project."""
        self._api_url: str = api_url.rstrip("/")
        self._anon_key: str = anon_key
        self._service_key: str | None = service_key
        self._session_lock: LockType = threading.Lock()
        self._generation_ids: count[int] = count()
        self._session_generation: int = next(self._generation_ids)
        self._session_lineage: SessionOperations = SessionOperations()
        self._current_session: Session | None = bootstrap_session(credentials)
        self._auth_callbacks: dict[int, AuthStateCallback] = {}
        self._auth_callback_ids: count[int] = count()
        self._auth_notifications: deque[
            tuple[
                tuple[int, ...],
                AuthChangeEvent,
                Session | None,
            ]
        ] = deque()
        self._dispatching_auth_notifications: bool = False
        self._transport: Transport = (
            _transport
            if _transport is not None
            else GeneratedTransport(api_url=self._api_url, timeout=timeout)
        )

        auth_context = self._auth_context()
        self._auth_requests: AuthRequests = AuthRequests(auth_context)
        self.auth: Auth = Auth(auth_context, _requests=self._auth_requests)
        self._facades: ClientContext = self._facade_context()
        self.functions: Functions = Functions(self._facades)
        self.durable: Durable = Durable(self._facades)
        self.logs: Logs = Logs(self._facades)
        self.storage: Storage = Storage(self._facades)
        self.locks: Locks = Locks(self._facades)
        if _realtime_client_factory is None:
            self.realtime: Realtime = Realtime(self._facades, api_url=self._api_url)
        else:
            self.realtime = Realtime(
                self._facades,
                api_url=self._api_url,
                client_factory=_realtime_client_factory,
            )

    def _auth_context(self) -> AuthContext:
        def capture_auth_session_binding() -> tuple[
            int, SessionOperations, Session | None
        ]:
            return self._capture_session_binding()

        return AuthContext(
            transport=lambda: self._transport,
            current_session=lambda: self.current_session,
            anon_token=self._anon_token,
            api_base_url=self._api_base_url,
            set_session=self._set_session,
            capture_session=self._capture_session,
            capture_session_binding=capture_auth_session_binding,
            update_session_user_if_current=self._update_session_user_if_current,
            set_session_if_current=self._set_session_if_current,
            clear_session_if_current=self._clear_session_if_current,
            subscribe_auth_state_change=self._subscribe_auth_state_change,
        )

    def _facade_context(self) -> ClientContext:
        return ClientContext(
            _get_transport=lambda: self._transport,
            _get_auth=lambda: self._auth_requests,
            _get_anon_token=self._anon_token,
            _get_session_token=self._session_token,
            _get_function_token=self._function_token,
            _get_service_token=self._service_token,
            _get_api_base_url=self._api_base_url,
            _get_capture_session_binding=self._capture_session_binding,
        )

    @property
    def current_session(self) -> Session | None:
        """The authenticated session, if one exists."""
        return self._capture_session()[1]

    def database(self, name: str) -> Database:
        """Create a query facade for a project database.

        Returns:
            A query facade bound to the named database.

        """
        return Database(self._facades, name)

    def _anon_token(self) -> str:
        return self._anon_key

    def _api_base_url(self) -> str:
        return self._api_url

    def _session_token(self) -> str:
        session = self._capture_session()[1]
        if session is None:
            raise RuntimeError(_NO_ACTIVE_SESSION)
        return session.access_token

    def _service_token(self) -> str:
        if self._service_key is None:
            raise RuntimeError(_NO_SERVICE_KEY)
        return self._service_key

    def _function_token(self) -> str:
        session = self._capture_session()[1]
        if session is not None:
            return session.access_token
        if self._service_key is not None:
            return self._service_key
        return self._anon_key

    def _set_session(
        self,
        session: Session,
        *,
        event: AuthChangeEvent | None,
    ) -> None:
        with self._session_lock:
            self._current_session = session
            self._session_generation = next(self._generation_ids)
            self._session_lineage = SessionOperations()
            if event is None:
                return
            callback_ids = tuple(self._auth_callbacks)
            dispatch = self._enqueue_auth_state_change(callback_ids, event, session)
        if dispatch:
            self._drain_auth_state_changes()

    def _capture_session(self) -> tuple[int, Session | None]:
        with self._session_lock:
            return self._session_generation, self._current_session

    def _capture_session_binding(self) -> tuple[int, SessionOperations, Session | None]:
        with self._session_lock:
            return (
                self._session_generation,
                self._session_lineage,
                self._current_session,
            )

    def _update_session_user_if_current(
        self, user: Mapping[str, JSONValue], generation: int
    ) -> bool:
        with self._session_lock:
            current = self._current_session
            if generation != self._session_generation or current is None:
                return False
            user_id = str(user["id"]) if current.user_id is None else current.user_id
            try:
                incoming_user_id = UUID(str(user["id"]))
                expected_user_id = UUID(user_id)
            except ValueError:
                raise AuthenticationError(_PROFILE_USER_MISMATCH) from None
            if incoming_user_id != expected_user_id:
                raise AuthenticationError(_PROFILE_USER_MISMATCH)
            # Profile updates do not replace credentials or invalidate other requests.
            self._current_session = replace(
                current, user_id=user_id, user={**user, "id": user_id}
            )
        return True

    def _set_session_if_current(
        self,
        session: Session,
        generation: int,
        *,
        event: AuthChangeEvent,
        notifications: list[Callable[[], None]] | None = None,
    ) -> bool:
        with self._session_lock:
            if generation != self._session_generation:
                return False
            if event == "TOKEN_REFRESHED":
                validate_refresh_identity(self._current_session, session)
            self._current_session = session
            self._session_generation = next(self._generation_ids)
            if event != "TOKEN_REFRESHED":
                self._session_lineage = SessionOperations(session)
            callback_ids = tuple(self._auth_callbacks)
            dispatch = self._enqueue_auth_state_change(callback_ids, event, session)
        if dispatch:
            self._dispatch_or_defer(notifications)
        return True

    def _clear_session_if_current(
        self,
        generation: int,
        *,
        lineage: SessionOperations | None = None,
        event: AuthChangeEvent,
        notifications: list[Callable[[], None]] | None = None,
    ) -> bool:
        with self._session_lock:
            if not self._owns_session_binding(generation, lineage):
                return False
            if self._current_session is None:
                return True
            self._current_session = None
            self._session_lineage.clear_local_credentials()
            self._session_generation = next(self._generation_ids)
            callback_ids = tuple(self._auth_callbacks)
            dispatch = self._enqueue_auth_state_change(callback_ids, event, None)
        if dispatch:
            self._dispatch_or_defer(notifications)
        return True

    def _owns_session_binding(
        self, generation: int, lineage: SessionOperations | None
    ) -> bool:
        # Call only while holding the session lock used for the state change.
        if lineage is not None:
            return lineage == self._session_lineage
        return generation == self._session_generation

    def _dispatch_or_defer(
        self, notifications: list[Callable[[], None]] | None
    ) -> None:
        if notifications is None:
            self._drain_auth_state_changes()
        else:
            notifications.append(self._drain_auth_state_changes)

    def _subscribe_auth_state_change(
        self,
        callback: AuthStateCallback,
    ) -> AuthSubscription:
        with self._session_lock:
            callback_id = next(self._auth_callback_ids)
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
            _ = self._auth_callbacks.pop(callback_id, None)

    def _enqueue_auth_state_change(
        self,
        callback_ids: tuple[int, ...],
        event: AuthChangeEvent,
        session: Session | None,
    ) -> bool:
        dispatch = bool(callback_ids) and not self._dispatching_auth_notifications
        if callback_ids:
            self._auth_notifications.append((callback_ids, event, session))
        if dispatch:
            self._dispatching_auth_notifications = True
        return dispatch

    def _drain_auth_state_changes(self) -> None:
        failure: BaseException | None = None
        while True:
            with self._session_lock:
                if not self._auth_notifications:
                    self._dispatching_auth_notifications = False
                    break
                callback_ids, event, session = self._auth_notifications.popleft()
            current_failure = self._notify_auth_state_change(
                callback_ids,
                event,
                session,
            )
            if failure is None:
                failure = current_failure
        if failure is not None:
            raise failure

    def _notify_auth_state_change(
        self,
        callback_ids: tuple[int, ...],
        event: AuthChangeEvent,
        session: Session | None,
    ) -> BaseException | None:
        failure: BaseException | None = None
        for callback_id in callback_ids:
            with self._session_lock:
                callback = self._auth_callbacks.get(callback_id)
            if callback is None:
                continue
            outcome = CallbackOutcome()
            with outcome:
                callback(event, session)
            if outcome.error is None or isinstance(outcome.error, Exception):
                continue
            self._unsubscribe_auth_state_change(callback_id)
            if failure is None:
                failure = outcome.error
        return failure
