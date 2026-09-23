"""Bound refresh and revocation work to one explicitly established session."""

from __future__ import annotations

from concurrent.futures import Future
from threading import Lock
from typing import TYPE_CHECKING, TypeVar

from .errors import SessionChangedError, VolcanoError

if TYPE_CHECKING:
    from _thread import LockType
    from collections.abc import Callable

    from .models import Session

_T = TypeVar("_T")


def _copy_failure(error: BaseException, *, include_cause: bool = True) -> BaseException:
    """Copy public failure details without retaining request frames or contexts.

    Returns
    -------
    BaseException
        A fresh exception with the original type and arguments. Volcano errors
        also retain their status, code, retry delay, and one optional SDK cause.

    """
    copied = type(error).__new__(type(error), *error.args)
    if isinstance(error, VolcanoError) and isinstance(copied, VolcanoError):
        copied.status = error.status
        copied.code = error.code
        copied.retry_after = error.retry_after
    if include_cause and isinstance(error.__cause__, VolcanoError):
        copied.__cause__ = _copy_failure(error.__cause__, include_cause=False)
    return copied


class SessionOperations:
    """Retain only this session's latest refresh and shared sign-out outcome."""

    def __init__(self, verified: Session | None = None) -> None:
        self._lock: LockType = Lock()
        self.refreshing: Future[Session] | None = None
        self.signing_out: Future[BaseException | None] | None = None
        self._locally_cleared: bool = False
        self._verified_pair: tuple[str, str | None] | None = (
            (verified.access_token, verified.refresh_token)
            if verified is not None
            else None
        )

    def verify_pair(self, session: Session | None) -> None:
        with self._lock:
            if self._locally_cleared:
                return
            self._verified_pair = (
                (session.access_token, session.refresh_token)
                if session is not None
                else None
            )

    def clear_local_credentials(self) -> None:
        """Keep pending revocation joinable; discard credentials after other clears."""
        with self._lock:
            if self.signing_out is not None:
                return
            self._locally_cleared = True
            self._verified_pair = None
            refreshing = self.refreshing
        if refreshing is not None:
            refreshing.add_done_callback(self._forget_refresh)

    def _forget_refresh(self, refreshing: Future[Session]) -> None:
        with self._lock:
            if self.refreshing is refreshing:
                self.refreshing = None

    def has_verified_pair(self, session: Session) -> bool:
        with self._lock:
            return session.refresh_token is not None and self._verified_pair == (
                session.access_token,
                session.refresh_token,
            )

    def refresh(self, operation: Callable[[], Session]) -> Session:
        with self._lock:
            if self.signing_out is not None or self._locally_cleared:
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
            self._complete_revocation(future, operation, preceding, pending=pending)
        self._sign_out_result(future)

    def wait_for_sign_out(self) -> None:
        with self._lock:
            future = self.signing_out
            pending = future is not None and not future.done()
        if pending and future is not None:
            self._sign_out_result(future)

    @staticmethod
    def _sign_out_result(future: Future[BaseException | None]) -> None:
        failure = future.result()
        if failure is not None:
            # Raising the retained template would attach credential-bearing frames.
            raise _copy_failure(failure)

    def _complete_revocation(
        self,
        future: Future[BaseException | None],
        operation: Callable[[Future[Session] | None, bool], None],
        preceding: Future[Session] | None,
        *,
        pending: bool,
    ) -> None:
        try:
            self._revoke(operation, preceding, pending=pending)
        except BaseException as error:
            future.set_result(_copy_failure(error))
            raise
        future.set_result(None)

    def _revoke(
        self,
        operation: Callable[[Future[Session] | None, bool], None],
        preceding: Future[Session] | None,
        *,
        pending: bool,
    ) -> None:
        try:
            operation(preceding, pending)
        finally:
            with self._lock:
                self._verified_pair = None
                self.refreshing = None

    @staticmethod
    def _complete(future: Future[_T], operation: Callable[[], _T]) -> None:
        try:
            future.set_result(operation())
        except BaseException as error:
            # Every waiter must finish, including when the owner is interrupted.
            future.set_exception(error)
            raise
