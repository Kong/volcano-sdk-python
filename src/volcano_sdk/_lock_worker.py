"""Background renewal for one lock lease."""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Protocol

from ._lock_guard import LockGuard, _lease_now
from .errors import VolcanoError

if TYPE_CHECKING:
    from .models import LockLease

RENEWER_SHUTDOWN_TIMEOUT_SECONDS = 1.0
MAX_RENEWAL_WAIT_SLICE_SECONDS = 1.0
_RENEWER_SHUTDOWN_TIMEOUT_MESSAGE = "lock renewal did not stop before cleanup"


class LockRenewalClient(Protocol):
    """Lock facade capability required by the renewal worker."""

    def renew(self, key: str, lease: LockLease, *, ttl: int) -> LockLease:
        """Renew one lease."""
        ...


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
        try:
            lease = self._locks.renew(
                self._key,
                self._guard.lease,
                ttl=self._ttl,
            )
        except (KeyError, TypeError, ValueError, VolcanoError) as error:
            self._guard.mark_lost(error)
            return False
        return self._guard.replace_lease(lease, started_at=started_at)
