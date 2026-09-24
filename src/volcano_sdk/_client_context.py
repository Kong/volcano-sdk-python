"""Capabilities shared by SDK facades without exposing client internals."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from ._auth_requests import AuthRequests
    from ._session_operations import SessionOperations
    from ._transport import Transport
    from .models import Session


@dataclass(frozen=True)
class ClientContext:
    """Live transport, credentials, and authentication operations for facades."""

    _get_transport: Callable[[], Transport]
    _get_auth: Callable[[], AuthRequests]
    _get_anon_token: Callable[[], str]
    _get_session_token: Callable[[], str]
    _get_function_token: Callable[[], str]
    _get_service_token: Callable[[], str]
    _get_api_base_url: Callable[[], str]
    _get_capture_session_binding: Callable[
        [], tuple[int, SessionOperations, Session | None]
    ]

    def transport(self) -> Transport:
        """Return the current transport."""
        return self._get_transport()

    def auth(self) -> AuthRequests:
        """Return the current auth."""
        return self._get_auth()

    def anon_token(self) -> str:
        """Return the current anon token."""
        return self._get_anon_token()

    def session_token(self) -> str:
        """Return the current session token."""
        return self._get_session_token()

    def function_token(self) -> str:
        """Return the current function token."""
        return self._get_function_token()

    def service_token(self) -> str:
        """Return the current service token."""
        return self._get_service_token()

    def api_base_url(self) -> str:
        """Return the current api base url."""
        return self._get_api_base_url()

    def capture_session_binding(self) -> tuple[int, SessionOperations, Session | None]:
        """Return the current capture session binding."""
        return self._get_capture_session_binding()
