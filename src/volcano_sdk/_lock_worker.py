"""Background renewal for one lock lease."""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Protocol

from ._lock_guard import LockGuard, _lease_now

if TYPE_CHECKING:
    from types import TracebackType

    from .models import LockLease

RENEWER_SHUTDOWN_TIMEOUT_SECONDS = 1.0
MAX_RENEWAL_WAIT_SLICE_SECONDS = 1.0
_RENEWER_SHUTDOWN_TIMEOUT_MESSAGE = "lock renewal did not stop before cleanup"


class LockRenewalClient(Protocol):
    """Lock facade capability required by the renewal worker."""

    def renew(self, key: str, lease: LockLease, *, ttl: int) -> LockLease:
        """Renew one lease."""
        ...


class _RenewalFailureRecorder:
    def __init__(self, guard: LockGuard) -> None:
        self._guard = guard

    def __enter__(self) -> None:
        return None

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        del exception_type, traceback
        if not isinstance(exception, Exception):
            return False
        self._guard.mark_lost(exception)
        return True


class LockRenewer:
    """Renew a guarded lease until stopped or ownership is lost."""

    def __init__(
        self,
        locks: LockRenewalClient,
        key: str,
        guard: LockGuard,
        *,
        ttl: int,
    ) -> None:
        self._locks = locks
        self._key = key
        self._guard = guard
        self._ttl = ttl
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self) -> None:
        """Start renewing the guarded lease."""
        self._thread.start()

    def stop(self) -> None:
        """Stop renewal without waiting indefinitely for a request."""
        self._stop.set()
        self._thread.join(timeout=RENEWER_SHUTDOWN_TIMEOUT_SECONDS)
        if self._thread.is_alive():
            self._guard.mark_lost(TimeoutError(_RENEWER_SHUTDOWN_TIMEOUT_MESSAGE))

    def _run(self) -> None:
        with _RenewalFailureRecorder(self._guard):
            while self._wait_until_renewal():
                if not self._renew_once():
                    return

    def _wait_until_renewal(self) -> bool:
        renew_at = _lease_now() + self._guard.renewal_delay()
        while not self._stop.is_set():
            if self._guard.lost:
                return False
            remaining = renew_at - _lease_now()
            if remaining <= 0:
                return True
            if self._stop.wait(min(remaining, MAX_RENEWAL_WAIT_SLICE_SECONDS)):
                return False
        return False

    def _renew_once(self) -> bool:
        started_at = _lease_now()
        with _RenewalFailureRecorder(self._guard):
            lease = self._locks.renew(
                self._key,
                self._guard.lease,
                ttl=self._ttl,
            )
            return self._guard.replace_lease(lease, started_at=started_at)
        return False
