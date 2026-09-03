from __future__ import annotations

import threading
from typing import TYPE_CHECKING

from volcano_sdk import LockLease, VolcanoError
from volcano_sdk import _lock_guard as guard_module
from volcano_sdk import _lock_worker as worker_module
from volcano_sdk._lock_guard import LockGuard
from volcano_sdk._lock_worker import LockRenewer

if TYPE_CHECKING:
    import pytest


def lease(*, fencing_token: int = 7) -> LockLease:
    return LockLease(
        key="build",
        token="00000000-0000-4000-8000-000000000001",
        expires_at=None,
        fencing_token=fencing_token,
    )


class RecordingLocks:
    def __init__(self, replacement: LockLease) -> None:
        self.replacement = replacement
        self.calls: list[tuple[str, LockLease, int]] = []

    def renew(self, key: str, lease: LockLease, *, ttl: int) -> LockLease:
        self.calls.append((key, lease, ttl))
        return self.replacement


class FailingLocks:
    def __init__(self, failure: VolcanoError) -> None:
        self.failure = failure

    def renew(self, key: str, lease: LockLease, *, ttl: int) -> LockLease:
        del key, lease, ttl
        raise self.failure


class StalledLocks:
    def __init__(self) -> None:
        self.entered = threading.Event()
        self.release = threading.Event()

    def renew(self, key: str, lease: LockLease, *, ttl: int) -> LockLease:
        del key, ttl
        self.entered.set()
        self.release.wait()
        return lease


class ExpiringWait:
    def __init__(self, clock: list[float]) -> None:
        self.clock = clock

    def wait(self, timeout: float | None = None) -> bool:
        del timeout
        self.clock[0] = 106.0
        return False

    def is_set(self) -> bool:
        return False


def test_lock_renewer_replaces_a_successfully_renewed_lease(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(guard_module, "_lease_now", lambda: 100.0)
    monkeypatch.setattr(worker_module, "_lease_now", lambda: 101.0)
    original = lease()
    replacement = lease(fencing_token=8)
    guard = LockGuard(original, ttl=30, started_at=100.0)
    locks = RecordingLocks(replacement)
    renewer = LockRenewer(locks, "build", guard, ttl=30)

    assert renewer._renew_once()

    assert guard.lease is replacement
    assert locks.calls == [("build", original, 30)]


def test_lock_renewer_records_an_sdk_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(guard_module, "_lease_now", lambda: 100.0)
    failure = VolcanoError("renewal failed")
    guard = LockGuard(lease(), ttl=30, started_at=100.0)
    renewer = LockRenewer(FailingLocks(failure), "build", guard, ttl=30)

    assert not renewer._renew_once()

    assert guard.lost
    assert guard._renewal_failure() is failure


def test_lock_renewer_stop_interrupts_a_scheduled_wait(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(guard_module, "_lease_now", lambda: 100.0)
    guard = LockGuard(lease(), ttl=30, started_at=100.0)
    locks = RecordingLocks(lease(fencing_token=8))
    renewer = LockRenewer(locks, "build", guard, ttl=30)

    renewer.start()
    renewer.stop()

    assert locks.calls == []
    assert not guard.lost


def test_lock_renewer_does_not_renew_after_the_lease_expires_while_waiting(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [100.0]
    monkeypatch.setattr(guard_module, "_lease_now", lambda: clock[0])
    guard = LockGuard(lease(), ttl=5, started_at=clock[0])
    locks = RecordingLocks(lease(fencing_token=8))
    renewer = LockRenewer(locks, "build", guard, ttl=5)
    monkeypatch.setattr(renewer, "_stop", ExpiringWait(clock))

    renewer._run()

    assert locks.calls == []
    assert guard.lost


def test_lock_renewer_bounds_stalled_shutdown(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(guard_module, "_lease_now", lambda: 100.0)
    monkeypatch.setattr(worker_module, "RENEWER_SHUTDOWN_TIMEOUT_SECONDS", 0.01)
    guard = LockGuard(lease(), ttl=30, started_at=100.0)
    monkeypatch.setattr(guard, "renewal_delay", lambda: 0.0)
    locks = StalledLocks()
    renewer = LockRenewer(locks, "build", guard, ttl=30)

    renewer.start()
    assert locks.entered.wait(timeout=1)
    try:
        renewer.stop()

        assert guard.lost
        failure = guard._renewal_failure()
        assert isinstance(failure, TimeoutError)
        assert str(failure) == "lock renewal did not stop before cleanup"
    finally:
        locks.release.set()
        renewer.stop()
