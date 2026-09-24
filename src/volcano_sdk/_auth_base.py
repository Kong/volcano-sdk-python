"""Shared authentication facade capabilities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._auth_context import auth_context
from ._auth_requests import AuthRequests
from ._auth_values import (
    user_from_payload,
)
from .errors import (
    SessionChangedError,
)

if TYPE_CHECKING:
    from ._auth_context import AuthContext, AuthContextSource
    from ._session_operations import SessionOperations
    from .models import (
        Session,
        User,
    )


class AuthBase:
    """Share typed client capabilities across authentication operation groups."""

    def __init__(
        self,
        client: AuthContext | AuthContextSource,
        *,
        _requests: AuthRequests | None = None,
    ) -> None:
        """Create an authentication facade backed by a client."""
        self._client: AuthContext = auth_context(client)
        self._requests: AuthRequests = (
            AuthRequests(self._client) if _requests is None else _requests
        )

    def _update_current_user(
        self, payload: object, binding: tuple[int, SessionOperations, Session | None]
    ) -> User:
        generation = self._requests.owned_session(binding)[0]
        user, snapshot = user_from_payload(payload)
        if not self._client.update_session_user_if_current(snapshot, generation):
            raise SessionChangedError
        return user
