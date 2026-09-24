"""Typed probes for session ownership and authentication request lifecycle."""

from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import override

from volcano_sdk import VolcanoClient
from volcano_sdk._auth_requests import AuthRequests
from volcano_sdk._session_operations import SessionOperations

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping
    from concurrent.futures import Future

    from volcano_sdk import Session
    from volcano_sdk._client_context import ClientContext
    from volcano_sdk.errors import VolcanoError
    from volcano_sdk.models import AuthChangeEvent, JSONValue


class InspectedAuthRequests(AuthRequests):
    def perform_refresh(
        self,
        binding: tuple[int, SessionOperations, Session | None],
        current: Session,
        notifications: list[Callable[[], None]],
    ) -> Session:
        return super()._perform_refresh(binding, current, notifications)

    def refresh_with_recovery(
        self,
        credentials: tuple[Session, str],
        binding: tuple[int, SessionOperations, Session | None],
        notifications: list[Callable[[], None]],
        *,
        verified: bool,
    ) -> Session:
        return super()._refresh_with_recovery(
            credentials, binding, notifications, verified=verified
        )

    def request_refreshed_session(self, refresh_token: str) -> Session:
        return super()._request_refreshed_session(refresh_token)

    def sign_out_captured(
        self,
        binding: tuple[int, SessionOperations, Session | None],
        preceding: Future[Session] | None,
        notifications: list[Callable[[], None]],
        *,
        pending: bool,
    ) -> None:
        super()._sign_out_captured(binding, preceding, notifications, pending=pending)

    @override
    def _sign_out_captured(
        self,
        binding: tuple[int, SessionOperations, Session | None],
        preceding: Future[Session] | None,
        notifications: list[Callable[[], None]],
        *,
        pending: bool,
    ) -> None:
        self.sign_out_captured(binding, preceding, notifications, pending=pending)

    def revoke_session(
        self,
        session: Session,
        owner: SessionOperations,
        refresh_error: VolcanoError | None,
        *,
        joined: bool,
    ) -> None:
        super()._revoke_session(session, owner, refresh_error, joined=joined)

    def revoke_access_session(
        self,
        session: Session,
        session_id: str,
        refresh_error: VolcanoError | None,
        *,
        joined: bool,
    ) -> None:
        super()._revoke_access_session(
            session, session_id, refresh_error, joined=joined
        )


class InspectedSessionOperations(SessionOperations):
    @property
    def retains_verified_credentials(self) -> bool:
        return self._verified_pair is not None


class InspectedClient(VolcanoClient):
    @property
    def requests(self) -> InspectedAuthRequests:
        requests = self._auth_requests
        assert isinstance(requests, InspectedAuthRequests)
        return requests

    @property
    def context(self) -> ClientContext:
        return self._facades

    def capture_session(self) -> tuple[int, Session | None]:
        return self._capture_session()

    def capture_session_binding(
        self,
    ) -> tuple[int, InspectedSessionOperations, Session | None]:
        generation, owner, session = super()._capture_session_binding()
        assert isinstance(owner, InspectedSessionOperations)
        return generation, owner, session

    def update_session_user_if_current(
        self, user: Mapping[str, JSONValue], generation: int
    ) -> bool:
        return self._update_session_user_if_current(user, generation)

    def set_session_if_current(
        self, session: Session, generation: int, *, event: AuthChangeEvent
    ) -> bool:
        return self._set_session_if_current(session, generation, event=event)

    def clear_session_if_current(
        self, generation: int, *, event: AuthChangeEvent
    ) -> bool:
        return self._clear_session_if_current(generation, event=event)

    @property
    def dispatching_auth_notifications(self) -> bool:
        return self._dispatching_auth_notifications

    def replace_current_session(self, session: Session) -> None:
        self._current_session: Session | None = session

    def replace_anon_key(self, key: str) -> None:
        self._anon_key: str = key

    def replace_service_key(self, key: str) -> None:
        self._service_key: str | None = key
