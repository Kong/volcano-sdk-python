"""Thread-safe state for an automatically renewed lock lease."""

from __future__ import annotations

import threading
import time
from typing import TYPE_CHECKING

from ._lock_renewer import renewal_delay as _calculate_renewal_delay

if TYPE_CHECKING:
    from .models import LockLease

MAX_LOCK_LIFETIME_SECONDS = 7_776_000
LOSS_POLL_INTERVAL_SECONDS = 1.0
SUSPEND_AWARE_CLOCK_ID = getattr(time, "CLOCK_BOOTTIME", None)
_LEASE_EXPIRED = "lock lease expired before renewal completed"
_NO_SAFE_RENEWAL_WINDOW = "lock renewal returned no safe lease window"


class _FallbackClock:
    """Combine monotonic progress with suspend-aware wall time."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._monotonic = time.monotonic()
        self._value = time.time()

    def __call__(self) -> float:
        with self._lock:
            monotonic = time.monotonic()
            elapsed = max(0.0, monotonic - self._monotonic)
            self._monotonic = monotonic
            self._value = max(self._value + elapsed, time.time())
            return self._value


_FALLBACK_CLOCK = _FallbackClock()


def _lease_now() -> float:
    clock_gettime = getattr(time, "clock_gettime", None)
    if clock_gettime is None or SUSPEND_AWARE_CLOCK_ID is None:
        return _FALLBACK_CLOCK()
    return float(clock_gettime(SUSPEND_AWARE_CLOCK_ID))


class LockGuard:
    """Expose the latest lease and whether its ownership has been lost."""

    def __init__(
        self,
        lease: LockLease,
        *,
        ttl: int,
        started_at: float,
    ) -> None:
        """Track one acquired lease against its local monotonic deadline."""
        self._state_lock = threading.Lock()
        self._lease = lease
        self._ttl = ttl
        self._absolute_deadline = started_at + MAX_LOCK_LIFETIME_SECONDS
        self._lease_deadline = min(started_at + ttl, self._absolute_deadline)
        self._failure: Exception | None = None
        self._lost = threading.Event()

    @property
    def lease(self) -> LockLease:
        """Return the latest successfully renewed immutable lease."""
        with self._state_lock:
            return self._lease

    @property
    def lost(self) -> bool:
        """Return whether renewal failed or the latest lease expired."""
        with self._state_lock:
            self._expire_if_needed_locked(_lease_now())
            return self._lost.is_set()

    def wait_lost(self, timeout: float | None = None) -> bool:
        """Wait until ownership is lost or the timeout expires."""
        timeout_deadline = None if timeout is None else _lease_now() + timeout
        while True:
            with self._state_lock:
                now = _lease_now()
                self._expire_if_needed_locked(now)
                if self._lost.is_set():
                    return True
                wait = min(
                    LOSS_POLL_INTERVAL_SECONDS,
                    self._remaining_seconds_locked(now),
                )
            if timeout_deadline is not None:
                timeout_remaining = timeout_deadline - _lease_now()
                if timeout_remaining <= 0:
                    return False
                wait = min(wait, timeout_remaining)
            self._lost.wait(wait)

    def replace_lease(self, lease: LockLease, *, started_at: float) -> bool:
        with self._state_lock:
            now = _lease_now()
            self._expire_if_needed_locked(now)
            if self._lost.is_set():
                return False
            deadline = min(started_at + self._ttl, self._absolute_deadline)
            if deadline <= now:
                self._mark_lost_locked(TimeoutError(_LEASE_EXPIRED))
                return False
            if _calculate_renewal_delay(self._ttl, remaining=deadline - now) == 0:
                self._mark_lost_locked(TimeoutError(_NO_SAFE_RENEWAL_WINDOW))
                return False
            self._lease = lease
            self._lease_deadline = deadline
            return True

    def mark_lost(self, failure: Exception) -> None:
        with self._state_lock:
            self._expire_if_needed_locked(_lease_now())
            self._mark_lost_locked(failure)

    def _remaining_seconds(self) -> float:
        with self._state_lock:
            now = _lease_now()
            self._expire_if_needed_locked(now)
            return self._remaining_seconds_locked(now)

    def renewal_delay(self) -> float:
        with self._state_lock:
            now = _lease_now()
            self._expire_if_needed_locked(now)
            if self._lost.is_set():
                return 0.0
            return _calculate_renewal_delay(
                self._ttl,
                remaining=self._remaining_seconds_locked(now),
            )

    def _renewal_failure(self) -> Exception | None:
        with self._state_lock:
            self._expire_if_needed_locked(_lease_now())
            return self._failure

    def _mark_lost_locked(self, failure: Exception) -> None:
        if self._failure is None:
            self._failure = failure
        self._lost.set()

    def _remaining_seconds_locked(self, now: float) -> float:
        return max(0.0, self._lease_deadline - now)

    def _expire_if_needed_locked(self, now: float) -> None:
        if self._failure is None and self._remaining_seconds_locked(now) == 0:
            self._mark_lost_locked(TimeoutError(_LEASE_EXPIRED))
