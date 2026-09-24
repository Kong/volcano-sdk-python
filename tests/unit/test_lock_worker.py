from __future__ import annotations

import threading

import pytest
from lock_inspection import InspectedLockGuard, InspectedLockRenewer

from volcano_sdk import LockLease, VolcanoError
from volcano_sdk import _lock_guard as guard_module
from volcano_sdk import _lock_worker as worker_module


def lease(*, fencing_token: int = 7) -> LockLease:
    return LockLease(
        key="build",
        token="00000000-0000-4000-8000-000000000001",
        expires_at=None,
        fencing_token=fencing_token,
    )


class RecordingLocks:
    def __init__(self, replacement: LockLease) -> None:
        self.replacement: LockLease = replacement
        self.calls: list[tuple[str, LockLease, int]] = []

    def renew(self, key: str, lease: LockLease, *, ttl: int) -> LockLease:
        self.calls.append((key, lease, ttl))
        return self.replacement


class FailingLocks:
    def __init__(self, failure: Exception) -> None:
        self.failure: Exception = failure

    def renew(self, key: str, lease: LockLease, *, ttl: int) -> LockLease:
        del key, lease, ttl
        raise self.failure


class StalledLocks:
    def __init__(self) -> None:
        self.entered: threading.Event = threading.Event()
        self.release: threading.Event = threading.Event()
        self.calls: list[tuple[str, LockLease, int]] = []

    def renew(self, key: str, lease: LockLease, *, ttl: int) -> LockLease:
        self.calls.append((key, lease, ttl))
        self.entered.set()
        _ = self.release.wait()
        return lease


class ExpiringWait:
    def __init__(self, clock: list[float]) -> None:
        self.clock: list[float] = clock

    def wait(self, timeout: float | None = None) -> bool:
        del timeout
        self.clock[0] = 106.0
        return False

    def is_set(self) -> bool:
        return False


class SuspendWait:
    def __init__(self, clock: list[float]) -> None:
        self.clock: list[float] = clock
        self.calls: list[float | None] = []

    def wait(self, timeout: float | None = None) -> bool:
        self.calls.append(timeout)
        assert len(self.calls) <= 2, "renewal wait did not converge"
        self.clock[0] = 101.0 if len(self.calls) == 1 else 111.0
        return False

    def is_set(self) -> bool:
        return False


def test_lock_renewer_replaces_a_successfully_renewed_lease(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(guard_module, "lease_now", lambda: 100.0)
    monkeypatch.setattr(worker_module, "lease_now", lambda: 101.0)
    original = lease()
    replacement = lease(fencing_token=8)
    guard = InspectedLockGuard(original, ttl=30, started_at=100.0)
    locks = RecordingLocks(replacement)
    renewer = InspectedLockRenewer(locks, "build", guard, ttl=30)

    assert renewer.renew_once()

    assert guard.lease is replacement
    assert locks.calls == [("build", original, 30)]


def test_lock_renewer_runs_as_a_daemon() -> None:
    guard = InspectedLockGuard(lease(), ttl=30, started_at=guard_module.lease_now())
    renewer = InspectedLockRenewer(RecordingLocks(lease()), "build", guard, ttl=30)

    assert renewer.worker_thread().daemon


def test_lock_renewer_continues_after_a_successful_renewal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    guard = InspectedLockGuard(lease(), ttl=30, started_at=guard_module.lease_now())
    renewer = InspectedLockRenewer(RecordingLocks(lease()), "build", guard, ttl=30)
    waits = iter((True, True, False))
    renewed: list[bool] = []

    def renew_once() -> bool:
        renewed.append(True)
        return True

    monkeypatch.setattr(renewer, "_wait_until_renewal", lambda: next(waits))
    monkeypatch.setattr(renewer, "_renew_once", renew_once)

    renewer.run_worker()

    assert renewed == [True, True]


def test_lock_renewer_does_not_swallow_process_interrupts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    guard = InspectedLockGuard(lease(), ttl=30, started_at=guard_module.lease_now())
    renewer = InspectedLockRenewer(RecordingLocks(lease()), "build", guard, ttl=30)

    def interrupt() -> bool:
        raise KeyboardInterrupt

    monkeypatch.setattr(renewer, "_wait_until_renewal", interrupt)

    with pytest.raises(KeyboardInterrupt):
        renewer.run_worker()
    assert not guard.lost


def test_lock_renewer_records_an_sdk_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(guard_module, "lease_now", lambda: 100.0)
    failure = VolcanoError("renewal failed")
    guard = InspectedLockGuard(lease(), ttl=30, started_at=100.0)
    renewer = InspectedLockRenewer(FailingLocks(failure), "build", guard, ttl=30)

    assert not renewer.renew_once()

    assert guard.lost
    assert guard.renewal_failure() is failure


def test_lock_renewer_records_an_unexpected_ordinary_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(guard_module, "lease_now", lambda: 100.0)
    failure = RuntimeError("service credential changed")
    guard = InspectedLockGuard(lease(), ttl=30, started_at=100.0)
    renewer = InspectedLockRenewer(FailingLocks(failure), "build", guard, ttl=30)

    assert not renewer.renew_once()

    assert guard.lost
    assert guard.renewal_failure() is failure


def test_lock_renewer_records_a_failure_outside_the_renewal_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(guard_module, "lease_now", lambda: 100.0)
    failure = RuntimeError("scheduling failed")
    guard = InspectedLockGuard(lease(), ttl=30, started_at=100.0)

    def fail_schedule() -> float:
        raise failure

    monkeypatch.setattr(guard, "renewal_delay", fail_schedule)
    renewer = InspectedLockRenewer(RecordingLocks(lease()), "build", guard, ttl=30)

    renewer.run_worker()

    assert guard.lost
    assert guard.renewal_failure() is failure


def test_lock_renewer_stop_interrupts_a_scheduled_wait(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(guard_module, "lease_now", lambda: 100.0)
    guard = InspectedLockGuard(lease(), ttl=30, started_at=100.0)
    locks = RecordingLocks(lease(fencing_token=8))
    renewer = InspectedLockRenewer(locks, "build", guard, ttl=30)

    renewer.start()
    renewer.stop()

    assert locks.calls == []
    assert not guard.lost


def test_lock_renewer_does_not_renew_after_the_lease_expires_while_waiting(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [100.0]
    monkeypatch.setattr(guard_module, "lease_now", lambda: clock[0])
    guard = InspectedLockGuard(lease(), ttl=5, started_at=clock[0])
    locks = RecordingLocks(lease(fencing_token=8))
    renewer = InspectedLockRenewer(locks, "build", guard, ttl=5)
    monkeypatch.setattr(renewer, "_stop", ExpiringWait(clock))

    renewer.run_worker()

    assert locks.calls == []
    assert guard.lost


def test_lock_renewer_rechecks_the_suspend_aware_clock_in_bounded_waits(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [100.0]
    monkeypatch.setattr(guard_module, "lease_now", lambda: clock[0])
    monkeypatch.setattr(worker_module, "lease_now", lambda: clock[0])
    guard = InspectedLockGuard(lease(), ttl=30, started_at=clock[0])
    monkeypatch.setattr(guard, "renewal_delay", lambda: 10.0)
    renewer = InspectedLockRenewer(RecordingLocks(lease()), "build", guard, ttl=30)
    wait = SuspendWait(clock)
    monkeypatch.setattr(renewer, "_stop", wait)

    assert renewer.wait_until_renewal()

    assert wait.calls == [1.0, 1.0]


def test_lock_renewer_waits_through_the_final_fractional_second(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [100.0]
    monkeypatch.setattr(guard_module, "lease_now", lambda: clock[0])
    monkeypatch.setattr(worker_module, "lease_now", lambda: clock[0])
    guard = InspectedLockGuard(lease(), ttl=30, started_at=clock[0])
    monkeypatch.setattr(guard, "renewal_delay", lambda: 10.0)
    renewer = InspectedLockRenewer(RecordingLocks(lease()), "build", guard, ttl=30)
    waits: list[float | None] = []

    class NearDeadlineWait:
        def is_set(self) -> bool:
            return False

        def wait(self, timeout: float | None = None) -> bool:
            waits.append(timeout)
            assert len(waits) <= 2
            clock[0] = 109.5 if len(waits) == 1 else 110.0
            return False

    monkeypatch.setattr(renewer, "_stop", NearDeadlineWait())

    assert renewer.wait_until_renewal()
    assert waits == [1.0, 0.5]


def test_lock_renewer_passes_a_bounded_join_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    guard = InspectedLockGuard(lease(), ttl=30, started_at=guard_module.lease_now())
    renewer = InspectedLockRenewer(RecordingLocks(lease()), "build", guard, ttl=30)
    waits: list[float | None] = []

    class RecordingThread:
        def join(self, timeout: float | None = None) -> None:
            waits.append(timeout)

        def is_alive(self) -> bool:
            return False

    monkeypatch.setattr(renewer, "_thread", RecordingThread())

    renewer.stop()

    assert waits == [worker_module.RENEWER_SHUTDOWN_TIMEOUT_SECONDS]


def test_lock_renewer_bounds_stalled_shutdown(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(guard_module, "lease_now", lambda: 100.0)
    monkeypatch.setattr(worker_module, "RENEWER_SHUTDOWN_TIMEOUT_SECONDS", 0.01)
    guard = InspectedLockGuard(lease(), ttl=30, started_at=100.0)
    monkeypatch.setattr(guard, "renewal_delay", lambda: 0.0)
    locks = StalledLocks()
    renewer = InspectedLockRenewer(locks, "build", guard, ttl=30)

    renewer.start()
    assert locks.entered.wait(timeout=1)
    try:
        renewer.stop()

        assert guard.lost
        failure = guard.renewal_failure()
        assert isinstance(failure, TimeoutError)
        assert str(failure) == "lock renewal did not stop before cleanup"
    finally:
        locks.release.set()
        renewer.stop()


def test_lock_renewer_stops_after_an_in_flight_request_completes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(guard_module, "lease_now", lambda: 100.0)
    monkeypatch.setattr(worker_module, "lease_now", lambda: 100.0)
    original = lease()
    guard = InspectedLockGuard(original, ttl=30, started_at=100.0)
    monkeypatch.setattr(guard, "renewal_delay", lambda: 0.0)
    locks = StalledLocks()
    renewer = InspectedLockRenewer(locks, "build", guard, ttl=30)

    renewer.start()
    try:
        assert locks.entered.wait(timeout=1)
        renewer.stop_event().set()
        locks.release.set()
        renewer.stop()

        assert locks.calls == [("build", original, 30)]
        assert guard.lease is original
        assert not guard.lost
        assert not renewer.worker_thread().is_alive()
    finally:
        locks.release.set()
        renewer.stop()
