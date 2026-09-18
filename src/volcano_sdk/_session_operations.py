"""Bound refresh and revocation work to one explicitly established session."""

from __future__ import annotations

from concurrent.futures import Future
from threading import Lock
from typing import TYPE_CHECKING, TypeVar

from .errors import SessionChangedError

if TYPE_CHECKING:
    from collections.abc import Callable

    from .models import Session

_T = TypeVar("_T")


class SessionOperations:
    """Retain only this session's latest refresh and shared sign-out outcome."""

    def __init__(self, verified: Session | None = None) -> None:
        self._lock = Lock()
        self.refreshing: Future[Session] | None = None
        self.signing_out: Future[None] | None = None
        self._verified_pair = (
            (verified.access_token, verified.refresh_token)
            if verified is not None
            else None
        )

    def verify_pair(self, session: Session | None) -> None:
        with self._lock:
            self._verified_pair = (
                (session.access_token, session.refresh_token)
                if session is not None
                else None
            )

    def has_verified_pair(self, session: Session) -> bool:
        with self._lock:
            return session.refresh_token is not None and self._verified_pair == (
                session.access_token,
                session.refresh_token,
            )

    def refresh(self, operation: Callable[[], Session]) -> Session:
        with self._lock:
            if self.signing_out is not None:
                raise SessionChangedError
            future = self.refreshing
            if future is None or future.done():
                future = self.refreshing = Future()
                owner = True
            else:
                owner = False
        if owner:
            self._complete(future, operation)
        return future.result()

    def sign_out(
        self, operation: Callable[[Future[Session] | None, bool], None]
    ) -> None:
        with self._lock:
            future = self.signing_out
            if future is None:
                future = self.signing_out = Future()
                owner = True
            else:
                owner = False
            preceding = self.refreshing
            pending = preceding is not None and not preceding.done()
        if owner:
            self._complete(future, lambda: operation(preceding, pending))
        future.result()

    @staticmethod
    def _complete(future: Future[_T], operation: Callable[[], _T]) -> None:
        try:
            future.set_result(operation())
        except BaseException as error:
            # Every waiter must finish, including when the owner is interrupted.
            future.set_exception(error)
            raise
