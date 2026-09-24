"""Typed client capabilities for authentication."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from ._session_operations import SessionOperations
    from ._transport import (
        Transport,
    )
    from .models import (
        AuthChangeEvent,
        AuthStateCallback,
        AuthSubscription,
        JSONValue,
        Session,
    )


class SetSession(Protocol):
    def __call__(
        self,
        session: Session,
        *,
        event: AuthChangeEvent | None,
    ) -> None: ...


class SetSessionIfCurrent(Protocol):
    def __call__(
        self,
        session: Session,
        generation: int,
        *,
        event: AuthChangeEvent,
        notifications: list[Callable[[], None]] | None = None,
    ) -> bool: ...


class ClearSessionIfCurrent(Protocol):
    def __call__(
        self,
        generation: int,
        *,
        lineage: SessionOperations | None = None,
        event: AuthChangeEvent,
        notifications: list[Callable[[], None]] | None = None,
    ) -> bool: ...


@dataclass(frozen=True, slots=True)
class AuthContext:
    """Typed client operations required by the authentication facade."""

    transport: Callable[[], Transport]
    current_session: Callable[[], Session | None]
    anon_token: Callable[[], str]
    api_base_url: Callable[[], str]
    set_session: SetSession
    capture_session: Callable[[], tuple[int, Session | None]]
    capture_session_binding: Callable[[], tuple[int, SessionOperations, Session | None]]
    update_session_user_if_current: Callable[[Mapping[str, JSONValue], int], bool]
    set_session_if_current: SetSessionIfCurrent
    clear_session_if_current: ClearSessionIfCurrent
    subscribe_auth_state_change: Callable[[AuthStateCallback], AuthSubscription]
