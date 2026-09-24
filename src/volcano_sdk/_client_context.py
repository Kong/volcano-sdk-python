"""Capabilities shared by SDK facades without exposing client internals."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol, TypeVar, runtime_checkable

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
        """Read a live facade capability.

        Returns:
            The current transport.

        """
        return self._get_transport()

    def auth(self) -> AuthRequests:
        """Read a live facade capability.

        Returns:
            The current auth.

        """
        return self._get_auth()

    def anon_token(self) -> str:
        """Read a live facade capability.

        Returns:
            The current anon token.

        """
        return self._get_anon_token()

    def session_token(self) -> str:
        """Read a live facade capability.

        Returns:
            The current session token.

        """
        return self._get_session_token()

    def function_token(self) -> str:
        """Read a live facade capability.

        Returns:
            The current function token.

        """
        return self._get_function_token()

    def service_token(self) -> str:
        """Read a live facade capability.

        Returns:
            The current service token.

        """
        return self._get_service_token()

    def api_base_url(self) -> str:
        """Read a live facade capability.

        Returns:
            The current api base url.

        """
        return self._get_api_base_url()

    def capture_session_binding(self) -> tuple[int, SessionOperations, Session | None]:
        """Read a live facade capability.

        Returns:
            The current capture session binding.

        """
        return self._get_capture_session_binding()


@runtime_checkable
class ClientContextSource(Protocol):
    """The private context factory retained by VolcanoClient."""

    def _facade_context(self) -> ClientContext: ...


ContextT = TypeVar("ContextT")


def facade_context(client: ClientContextSource | ContextT) -> ClientContext | ContextT:
    """Accept legacy direct facade construction without exposing client internals.

    Returns:
        The client's live capabilities or the supplied narrow context.

    """
    if isinstance(client, ClientContextSource):
        return client._facade_context()  # ruff: ignore[private-member-access] # pyright: ignore[reportPrivateUsage]
    return client
