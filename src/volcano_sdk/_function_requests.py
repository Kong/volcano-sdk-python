"""Credential-scoped retries for one resolved function invocation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar

from ._function_values import HTTP_UNAUTHORIZED
from .errors import AuthenticationError, SessionChangedError, VolcanoError

if TYPE_CHECKING:
    from collections.abc import Callable

    from ._auth_requests import AuthRequests
    from ._session_operations import SessionOperations
    from ._transport import Transport
    from .models import Session

_Result = TypeVar("_Result")


class FunctionsContext(Protocol):
    """Client capabilities required by function invocation."""

    def transport(self) -> Transport: ...
    def auth(self) -> AuthRequests: ...

    def capture_session_binding(
        self,
    ) -> tuple[int, SessionOperations, Session | None]: ...

    def function_token(self) -> str: ...

    def api_base_url(self) -> str: ...


class FunctionAuth:
    def __init__(self, client: FunctionsContext) -> None:
        self._client: FunctionsContext = client
        self._binding: tuple[int, SessionOperations, Session | None] = (
            client.capture_session_binding()
        )
        self._fallback_token: str = client.function_token()

    def run(self, operation: Callable[[str], _Result]) -> _Result:
        if self._binding[2] is not None:
            self._binding = self._client.auth().owned_session(self._binding)
        try:
            return self._run(operation)
        finally:
            if self._binding[2] is not None:
                self._client.auth().validate_failure(self._binding)
            elif self._client.capture_session_binding()[1] != self._binding[1]:
                raise SessionChangedError

    def _run(self, operation: Callable[[str], _Result]) -> _Result:
        try:
            return operation(self._token())
        except AuthenticationError as original:
            if self._binding[2] is None or original.status != HTTP_UNAUTHORIZED:
                raise
            try:
                # Resolve has released its cache lock before refresh callbacks run.
                _ = self._client.auth().refresh(self._binding)
            except SessionChangedError:
                raise
            except VolcanoError:
                raise original from None
            return operation(self._token())

    def _token(self) -> str:
        if self._binding[2] is None:
            if self._client.capture_session_binding()[1] != self._binding[1]:
                raise SessionChangedError
            return self._fallback_token
        session = self._client.auth().owned_session(self._binding)[2]
        return session.access_token
