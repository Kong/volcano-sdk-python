"""Distributed lock facade."""

from __future__ import annotations

import secrets
import threading
import time
from contextlib import contextmanager
from datetime import datetime
from typing import TYPE_CHECKING, Protocol, cast
from uuid import uuid4

from ._transport import Transport, invoke, response_payload
from .errors import VolcanoError
from .models import LockLease, LockState

if TYPE_CHECKING:
    from collections.abc import Generator

MIN_LOCK_TTL_SECONDS = 5
MAX_LOCK_TTL_SECONDS = 7_776_000
MAX_RENEWAL_DELAY_SECONDS = 60.0
RENEWAL_SAFETY_MARGIN_SECONDS = 1.0
RENEWAL_REQUEST_BUDGET_SECONDS = 1.0
RENEWER_SHUTDOWN_TIMEOUT_SECONDS = 1.0
EXPIRY_POLL_INTERVAL_SECONDS = 1.0
RENEWER_SHUTDOWN_TIMEOUT_MESSAGE = "lock renewal did not stop before cleanup"
UNSAFE_RENEWAL_MESSAGE = "lock renewal returned no safe lease window"
SUSPEND_AWARE_CLOCK_ID = getattr(time, "CLOCK_BOOTTIME", time.CLOCK_MONOTONIC)


def _lease_now() -> float:
    return time.clock_gettime(SUSPEND_AWARE_CLOCK_ID)


class LocksContext(Protocol):
    """Client capabilities required by distributed locks."""

    _transport: Transport

    def _service_token(self) -> str: ...


class LockGetTransport(Protocol):
    """Transport capability required to inspect a lock."""

    def get_project_lock(
        self,
        *,
        authorization: str,
        key: str,
    ) -> object:
        """Get one project-scoped lock."""
        ...


class LockRenewTransport(Protocol):
    """Transport capability required to renew a lock."""

    def renew_project_lock(
        self,
        *,
        authorization: str,
        key: str,
        ttl: int,
        token: str,
    ) -> object:
        """Renew one project-scoped lock."""
        ...


class LockForceReleaseTransport(Protocol):
    """Transport capability required to force release a lock."""

    def force_release_project_lock(
        self,
        *,
        authorization: str,
        key: str,
    ) -> object:
        """Force release one project-scoped lock."""
        ...


def _parse_datetime(value: object) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(str(value))


def _validate_ttl(ttl: object) -> None:
    if (
        isinstance(ttl, bool)
        or not isinstance(ttl, int)
        or not MIN_LOCK_TTL_SECONDS <= ttl <= MAX_LOCK_TTL_SECONDS
    ):
        message = "ttl must be an integer between 5 seconds and 90 days"
        raise ValueError(message)


def _renewal_delay(
    ttl: int,
    *,
    remaining: float | None = None,
) -> float:
    delay = min(ttl / 3, MAX_RENEWAL_DELAY_SECONDS)
    latest_delay: float | None = None
    if remaining is not None:
        latest_delay = max(
            0.0,
            remaining - RENEWAL_SAFETY_MARGIN_SECONDS - RENEWAL_REQUEST_BUDGET_SECONDS,
        )
        delay = min(delay, latest_delay)
    jitter = (secrets.randbelow(2_001) / 10_000) - 0.1
    jittered_delay = max(0.0, delay * (1 + jitter))
    return jittered_delay if latest_delay is None else min(jittered_delay, latest_delay)


class LockGuard:
    """Thread-safe state for an automatically renewed lock lease."""

    def __init__(
        self,
        lease: LockLease,
        *,
        ttl: int,
        started_at: float,
    ) -> None:
        """Create a guard around an acquired lease."""
        self._state_lock = threading.Lock()
        self._lease = lease
        self._ttl = ttl
        self._absolute_deadline = started_at + MAX_LOCK_TTL_SECONDS
        self._lease_deadline = min(started_at + ttl, self._absolute_deadline)
        self._failure: Exception | None = None
        self._lost = threading.Event()
        self._expiry_timer: threading.Timer | None = None
        self._expiry_generation = 0
        self._expiry_active = False

    @property
    def lease(self) -> LockLease:
        """Return the latest successfully renewed immutable lease."""
        with self._state_lock:
            return self._lease

    @property
    def lost(self) -> bool:
        """Return whether renewal failed or the latest lease expired."""
        with self._state_lock:
            self._expire_if_needed_locked()
            return self._lost.is_set()

    def wait_lost(self, timeout: float | None = None) -> bool:
        """Wait until renewal fails or the timeout expires."""
        deadline = None if timeout is None else _lease_now() + timeout
        while not self.lost:
            remaining = None if deadline is None else deadline - _lease_now()
            if remaining is not None and remaining <= 0:
                return False
            wait = EXPIRY_POLL_INTERVAL_SECONDS
            if remaining is not None:
                wait = min(wait, remaining)
            self._lost.wait(wait)
        return True

    def _start_expiry_watch(self) -> None:
        with self._state_lock:
            self._expiry_active = True
            self._schedule_expiry_locked()

    def _replace_lease(
        self,
        lease: LockLease,
        *,
        started_at: float,
    ) -> bool:
        with self._state_lock:
            if self._lost.is_set():
                return False
            self._lease = lease
            self._lease_deadline = min(
                started_at + self._ttl,
                self._absolute_deadline,
            )
            if self._renewal_delay_locked() == 0:
                self._failure = TimeoutError(UNSAFE_RENEWAL_MESSAGE)
                self._lost.set()
                return False
            if self._expiry_active:
                try:
                    self._schedule_expiry_locked()
                except RuntimeError as error:
                    self._failure = error
                    self._lost.set()
                    return False
            return True

    def _mark_lost(self, failure: Exception) -> None:
        with self._state_lock:
            if self._failure is None:
                self._failure = failure
            self._cancel_expiry_locked()
            self._lost.set()

    def _stop_expiry_watch(self) -> None:
        with self._state_lock:
            self._expire_if_needed_locked()
            self._expiry_active = False
            self._cancel_expiry_locked()

    def _renewal_delay(self) -> float:
        with self._state_lock:
            return self._renewal_delay_locked()

    def _renewal_delay_locked(self) -> float:
        return _renewal_delay(
            self._ttl,
            remaining=self._remaining_seconds_locked(),
        )

    def _schedule_expiry_locked(self) -> None:
        self._cancel_expiry_locked()
        self._expiry_generation += 1
        generation = self._expiry_generation
        delay = min(
            self._remaining_seconds_locked(),
            EXPIRY_POLL_INTERVAL_SECONDS,
        )
        timer = threading.Timer(delay, self._expire, args=(generation,))
        timer.daemon = True
        self._expiry_timer = timer
        timer.start()

    def _cancel_expiry_locked(self) -> None:
        self._expiry_generation += 1
        if self._expiry_timer is not None:
            self._expiry_timer.cancel()
            self._expiry_timer = None

    def _remaining_seconds_locked(self) -> float:
        return max(0.0, self._lease_deadline - _lease_now())

    def _expiry_delay(self) -> float:
        with self._state_lock:
            return self._remaining_seconds_locked()

    def _expire_if_needed_locked(self) -> None:
        if self._failure is None and self._remaining_seconds_locked() == 0:
            self._failure = TimeoutError("lock lease expired before renewal completed")
            self._lost.set()

    def _expire(self, generation: int) -> None:
        with self._state_lock:
            if generation != self._expiry_generation or self._failure is not None:
                return
            self._expiry_timer = None
            self._expire_if_needed_locked()
            if self._expiry_active and self._failure is None:
                self._schedule_expiry_locked()

    def _renewal_failure(self) -> Exception | None:
        with self._state_lock:
            self._expire_if_needed_locked()
            return self._failure


class _LockRenewer:
    def __init__(self, locks: Locks, key: str, guard: LockGuard, ttl: int) -> None:
        self._locks = locks
        self._key = key
        self._guard = guard
        self._ttl = ttl
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        self._thread.join(timeout=RENEWER_SHUTDOWN_TIMEOUT_SECONDS)
        if self._thread.is_alive():
            self._guard._mark_lost(TimeoutError(RENEWER_SHUTDOWN_TIMEOUT_MESSAGE))

    def _run(self) -> None:
        while not self._guard.lost:
            if self._stop.wait(self._guard._renewal_delay()):
                return
            if self._guard.lost:
                return
            try:
                started_at = _lease_now()
                lease = self._locks.renew(
                    self._key,
                    self._guard.lease,
                    ttl=self._ttl,
                )
            except (KeyError, TypeError, ValueError, VolcanoError) as error:
                self._guard._mark_lost(error)
                return
            if not self._guard._replace_lease(
                lease,
                started_at=started_at,
            ):
                return


class Locks:
    """Acquire and release project-scoped distributed locks."""

    def __init__(self, client: LocksContext) -> None:
        """Create a lock facade backed by a client."""
        self._client = client

    def get(self, key: str) -> LockState:
        """Return the current state of a project-scoped lock."""
        transport = cast("LockGetTransport", self._client._transport)
        response = invoke(
            transport.get_project_lock,
            authorization=self._client._service_token(),
            key=key,
        )
        payload = response_payload(response, 200)
        return LockState(
            held=payload["held"],
            expires_at=_parse_datetime(payload.get("expires_at")),
            fencing_token=payload.get("fencing_token"),
        )

    def acquire(self, key: str, *, ttl: int) -> LockLease:
        """Acquire a lock lease for the requested number of seconds."""
        token = str(uuid4())
        response = invoke(
            self._client._transport.acquire_project_lock,
            authorization=self._client._service_token(),
            key=key,
            ttl=ttl,
            token=token,
        )
        payload = response_payload(response, 201)
        return LockLease(
            key=key,
            token=token,
            expires_at=_parse_datetime(payload.get("expires_at")),
            fencing_token=payload.get("fencing_token"),
        )

    def renew(self, key: str, lease: LockLease, *, ttl: int) -> LockLease:
        """Renew a lock lease and return its immutable replacement."""
        transport = cast("LockRenewTransport", self._client._transport)
        response = invoke(
            transport.renew_project_lock,
            authorization=self._client._service_token(),
            key=key,
            ttl=ttl,
            token=lease.token,
        )
        payload = response_payload(response, 200)
        return LockLease(
            key=key,
            token=lease.token,
            expires_at=_parse_datetime(payload.get("expires_at")),
            fencing_token=payload.get("fencing_token"),
        )

    def release(self, key: str, lease: LockLease) -> None:
        """Release a lock lease."""
        response = invoke(
            self._client._transport.release_project_lock,
            authorization=self._client._service_token(),
            key=key,
            token=lease.token,
        )
        response_payload(response, 204)

    def force_release(self, key: str) -> None:
        """Release a lock regardless of which token owns it."""
        transport = cast("LockForceReleaseTransport", self._client._transport)
        response = invoke(
            transport.force_release_project_lock,
            authorization=self._client._service_token(),
            key=key,
        )
        response_payload(response, 204)

    @contextmanager
    def with_lock(self, key: str, *, ttl: int) -> Generator[LockGuard]:
        """Hold and automatically renew a lock for the context's lifetime."""
        _validate_ttl(ttl)
        started_at = _lease_now()
        guard = LockGuard(
            self.acquire(key, ttl=ttl),
            ttl=ttl,
            started_at=started_at,
        )
        renewer = _LockRenewer(self, key, guard, ttl)
        renewer_started = False
        body_failed = False
        try:
            self._prepare_guard(key, guard, ttl=ttl)
            guard._start_expiry_watch()
            renewer.start()
            renewer_started = True
            yield guard
        except BaseException:
            body_failed = True
            raise
        finally:
            try:
                if renewer_started:
                    renewer.stop()
            finally:
                guard._stop_expiry_watch()
                failure = guard._renewal_failure()
                self._finish_guard(
                    key,
                    guard,
                    body_failed=body_failed,
                    failure=failure,
                )

    def _prepare_guard(self, key: str, guard: LockGuard, *, ttl: int) -> None:
        if guard._renewal_delay() != 0:
            return
        started_at = _lease_now()
        renewed = self.renew(key, guard.lease, ttl=ttl)
        if guard._replace_lease(
            renewed,
            started_at=started_at,
        ):
            return
        failure = guard._renewal_failure()
        if failure is not None:
            raise failure

    def _finish_guard(
        self,
        key: str,
        guard: LockGuard,
        *,
        body_failed: bool,
        failure: Exception | None,
    ) -> None:
        release_error: Exception | None = None
        try:
            self.release(key, guard.lease)
        except (KeyError, TypeError, ValueError, VolcanoError) as error:
            release_error = error
        if body_failed:
            return
        if failure is not None:
            raise failure
        if release_error is not None:
            raise release_error
