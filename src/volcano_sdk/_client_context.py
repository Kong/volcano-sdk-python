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

    transport: Callable[[], Transport]
    auth: Callable[[], AuthRequests]
    anon_token: Callable[[], str]
    session_token: Callable[[], str]
    function_token: Callable[[], str]
    service_token: Callable[[], str]
    api_base_url: Callable[[], str]
    capture_session_binding: Callable[[], tuple[int, SessionOperations, Session | None]]
