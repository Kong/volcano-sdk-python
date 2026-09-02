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
MIN_RENEWAL_DELAY_SECONDS = 0.001


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


def _validate_ttl(ttl: int) -> None:
    if isinstance(ttl, bool) or not MIN_LOCK_TTL_SECONDS <= ttl <= MAX_LOCK_TTL_SECONDS:
        message = "ttl must be an integer between 5 seconds and 90 days"
        raise ValueError(message)


def _renewal_delay(ttl: int, lease: LockLease) -> float:
    delay = min(ttl / 3, MAX_RENEWAL_DELAY_SECONDS)
    if lease.expires_at is not None:
        remaining = (lease.expires_at.timestamp() - time.time()) / 3
        delay = min(delay, max(MIN_RENEWAL_DELAY_SECONDS, remaining))
    jitter = (secrets.randbelow(2_001) / 10_000) - 0.1
    return max(MIN_RENEWAL_DELAY_SECONDS, delay * (1 + jitter))


class LockGuard:
    """Thread-safe state for an automatically renewed lock lease."""

    def __init__(self, lease: LockLease) -> None:
        """Create a guard around an acquired lease."""
        self._state_lock = threading.Lock()
        self._lease = lease
        self._failure: Exception | None = None
        self._lost = threading.Event()

    @property
    def lease(self) -> LockLease:
        """Return the latest successfully renewed immutable lease."""
        with self._state_lock:
            return self._lease

    @property
    def lost(self) -> bool:
        """Return whether automatic renewal failed."""
        return self._lost.is_set()

    def wait_lost(self, timeout: float | None = None) -> bool:
        """Wait until renewal fails or the timeout expires."""
        return self._lost.wait(timeout)

    def _replace_lease(self, lease: LockLease) -> None:
        with self._state_lock:
            self._lease = lease

    def _mark_lost(self, failure: Exception) -> None:
        with self._state_lock:
            self._failure = failure
        self._lost.set()

    def _renewal_failure(self) -> Exception | None:
        with self._state_lock:
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
        self._thread.join()

    def _run(self) -> None:
        while not self._stop.wait(_renewal_delay(self._ttl, self._guard.lease)):
            try:
                lease = self._locks.renew(
                    self._key,
                    self._guard.lease,
                    ttl=self._ttl,
                )
            except (KeyError, TypeError, ValueError, VolcanoError) as error:
                self._guard._mark_lost(error)
                return
            self._guard._replace_lease(lease)


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
        guard = LockGuard(self.acquire(key, ttl=ttl))
        renewer = _LockRenewer(self, key, guard, ttl)
        renewer.start()
        body_failed = False
        try:
            yield guard
        except BaseException:
            body_failed = True
            raise
        finally:
            renewer.stop()
            self._finish_guard(key, guard, body_failed=body_failed)

    def _finish_guard(
        self,
        key: str,
        guard: LockGuard,
        *,
        body_failed: bool,
    ) -> None:
        release_error: Exception | None = None
        try:
            self.release(key, guard.lease)
        except (KeyError, TypeError, ValueError, VolcanoError) as error:
            release_error = error
        if body_failed:
            return
        failure = guard._renewal_failure()
        if failure is not None:
            raise failure
        if release_error is not None:
            raise release_error
