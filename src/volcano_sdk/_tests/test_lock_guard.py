from __future__ import annotations

import time
from datetime import UTC, datetime

import pytest

import volcano_sdk._lock_guard as guard_module
from volcano_sdk import LockLease
from volcano_sdk import _lock_renewer as renewer_module

from .lock_inspection import InspectedLockGuard


def lease(*, expires_at: datetime | None = None) -> LockLease:
    return LockLease(
        key="build",
        token="00000000-0000-4000-8000-000000000001",
        expires_at=expires_at,
        fencing_token=7,
    )


@pytest.mark.parametrize(
    ("clock_id", "expected"),
    [(7, 7), (None, None), ("invalid", None)],
)
def test_suspend_aware_clock_id_accepts_only_integer_clock_ids(
    clock_id: object, expected: int | None
) -> None:
    assert guard_module.suspend_aware_clock_id(clock_id) == expected


def test_lease_clock_falls_back_to_portable_monotonic(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delattr(time, "clock_gettime", raising=False)
    monkeypatch.setattr(guard_module, "_FALLBACK_CLOCK", lambda: 123.0)

    assert guard_module.lease_now() == pytest.approx(123.0)


def test_lease_clock_falls_back_when_clock_gettime_is_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(time, "clock_gettime", None)
    monkeypatch.setattr(guard_module, "SUSPEND_AWARE_CLOCK_ID", 7)
    monkeypatch.setattr(guard_module, "_FALLBACK_CLOCK", lambda: 123.0)

    assert guard_module.lease_now() == pytest.approx(123.0)


def test_lease_clock_uses_the_suspend_aware_system_clock(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requested_clocks: list[int] = []

    def clock_gettime(clock_id: int) -> float:
        requested_clocks.append(clock_id)
        return 456.0

    monkeypatch.setattr(guard_module, "SUSPEND_AWARE_CLOCK_ID", 7)
    monkeypatch.setattr(time, "clock_gettime", clock_gettime, raising=False)

    assert guard_module.lease_now() == pytest.approx(456.0)
    assert requested_clocks == [7]


@pytest.mark.parametrize(
    ("timeout", "expected_lost", "expected_waits"),
    [(None, True, [1.0] * 5), (0.25, False, [0.25])],
)
def test_lock_guard_bounds_waits_by_lease_and_caller_deadlines(
    monkeypatch: pytest.MonkeyPatch,
    timeout: float | None,
    *,
    expected_lost: bool,
    expected_waits: list[float],
) -> None:
    clock = [100.0]
    waits: list[float] = []
    reads = [0]

    def now() -> float:
        reads[0] += 1
        assert reads[0] < 30, "guard polled without waiting"
        return clock[0]

    monkeypatch.setattr(guard_module, "lease_now", now)
    guard = InspectedLockGuard(lease(), ttl=5, started_at=clock[0])

    def wait(timeout: float | None) -> bool:
        assert len(waits) < 6, "guard wait did not converge"
        assert timeout is not None
        waits.append(timeout)
        clock[0] += timeout
        return False

    monkeypatch.setattr(guard.loss_event(), "wait", wait)

    assert guard.wait_lost(timeout=timeout) is expected_lost
    assert guard.lost is expected_lost
    assert waits == expected_waits


def test_lock_guard_rejects_an_already_expired_renewal_window(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(guard_module, "lease_now", lambda: 100.0)
    original = lease()
    guard = InspectedLockGuard(original, ttl=5, started_at=100.0)

    assert not guard.replace_lease(lease(), started_at=95.0)

    assert guard.lease is original
    assert guard.lost
    failure = guard.renewal_failure()
    assert isinstance(failure, TimeoutError)
    assert str(failure) == "lock lease expired before renewal completed"


def test_fallback_clock_includes_system_suspend(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monotonic = iter((100.0, 100.0))
    wall = iter((1_000.0, 1_005.0))
    monkeypatch.setattr(time, "monotonic", lambda: next(monotonic))
    monkeypatch.setattr(time, "time", lambda: next(wall))
    clock = guard_module.FallbackClock()

    assert clock() == pytest.approx(1_005.0)


def test_fallback_clock_ignores_wall_clock_rollbacks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monotonic = iter((100.0, 101.0))
    wall = iter((1_000.0, 900.0))
    monkeypatch.setattr(time, "monotonic", lambda: next(monotonic))
    monkeypatch.setattr(time, "time", lambda: next(wall))
    clock = guard_module.FallbackClock()

    assert clock() == pytest.approx(1_001.0)


def test_fallback_clock_does_not_advance_without_elapsed_time(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(time, "monotonic", lambda: 100.0)
    monkeypatch.setattr(time, "time", lambda: 1_000.0)
    clock = guard_module.FallbackClock()

    assert clock() == pytest.approx(1_000.0)


def test_fallback_clock_accumulates_monotonic_time_across_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monotonic = iter((100.0, 101.0, 102.0))
    wall = iter((1_000.0, 900.0, 900.0))
    monkeypatch.setattr(time, "monotonic", lambda: next(monotonic))
    monkeypatch.setattr(time, "time", lambda: next(wall))
    clock = guard_module.FallbackClock()

    assert clock() == pytest.approx(1_001.0)
    assert clock() == pytest.approx(1_002.0)


def test_expired_guard_retains_the_ownership_loss_reason(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [100.0]
    monkeypatch.setattr(guard_module, "lease_now", lambda: clock[0])
    guard = InspectedLockGuard(lease(), ttl=5, started_at=clock[0])

    clock[0] = 105.0

    assert guard.lost
    assert str(guard.renewal_failure()) == "lock lease expired before renewal completed"


def test_lock_guard_exposes_the_latest_immutable_lease(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [100.0]
    monkeypatch.setattr(guard_module, "lease_now", lambda: clock[0])
    original = lease(expires_at=datetime(2026, 9, 3, 12, 0, 5, tzinfo=UTC))
    renewed = lease(expires_at=datetime(2026, 9, 3, 12, 0, 9, tzinfo=UTC))
    guard = InspectedLockGuard(original, ttl=5, started_at=clock[0])

    clock[0] = 104.0
    assert guard.replace_lease(renewed, started_at=clock[0])

    assert guard.lease is renewed
    assert not guard.lost
    assert guard.remaining_seconds() == pytest.approx(5.0)


def test_lock_guard_calculates_renewal_delay_from_remaining_lease(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(guard_module, "lease_now", lambda: 100.0)
    monkeypatch.setattr(renewer_module, "renewal_jitter", lambda: 0.0)
    guard = InspectedLockGuard(lease(), ttl=30, started_at=100.0)

    assert guard.renewal_delay() == pytest.approx(10.0)


def test_lock_guard_rejects_a_renewal_completed_after_lease_expiry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [100.0]
    monkeypatch.setattr(guard_module, "lease_now", lambda: clock[0])
    original = lease()
    guard = InspectedLockGuard(original, ttl=5, started_at=clock[0])

    clock[0] = 105.0

    assert not guard.replace_lease(lease(), started_at=104.0)
    assert guard.lease is original
    assert guard.lost
    assert isinstance(guard.renewal_failure(), TimeoutError)


def test_lock_guard_detects_suspend_aware_expiry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [100.0]
    monkeypatch.setattr(guard_module, "lease_now", lambda: clock[0])
    guard = InspectedLockGuard(lease(), ttl=5, started_at=clock[0])

    clock[0] = 105.0

    assert guard.wait_lost(timeout=0)
    assert guard.lost


def test_lock_guard_wait_times_out_while_the_lease_is_held(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [100.0]

    def now() -> float:
        clock[0] += 0.25
        return clock[0]

    monkeypatch.setattr(guard_module, "lease_now", now)
    guard = InspectedLockGuard(lease(), ttl=5, started_at=100.0)
    waits = [0]

    def wait(_timeout: float | None) -> bool:
        waits[0] += 1
        assert waits[0] < 10, "guard ignored the caller timeout"
        return False

    monkeypatch.setattr(guard.loss_event(), "wait", wait)

    assert not guard.wait_lost(timeout=0)
    assert not guard.lost
    assert waits[0] == 0


def test_lock_guard_preserves_the_absolute_acquisition_deadline(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [0.0]
    monkeypatch.setattr(guard_module, "lease_now", lambda: clock[0])
    guard = InspectedLockGuard(
        lease(),
        ttl=guard_module.MAX_LOCK_LIFETIME_SECONDS,
        started_at=clock[0],
        lease_started_at=10.0,
    )

    clock[0] = guard_module.MAX_LOCK_LIFETIME_SECONDS - 1
    assert not guard.replace_lease(lease(), started_at=clock[0])
    assert guard.lost
    assert str(guard.renewal_failure()) == "lock renewal returned no safe lease window"


def test_lock_guard_preserves_the_first_loss_reason(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(guard_module, "lease_now", lambda: 100.0)
    guard = InspectedLockGuard(lease(), ttl=5, started_at=100.0)
    first = RuntimeError("renewal failed")

    guard.mark_lost(first)
    guard.mark_lost(RuntimeError("later failure"))

    assert guard.lost
    assert guard.wait_lost(timeout=0)
    assert guard.renewal_failure() is first


def test_lock_guard_classifies_expiry_before_a_late_renewal_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [100.0]
    monkeypatch.setattr(guard_module, "lease_now", lambda: clock[0])
    guard = InspectedLockGuard(lease(), ttl=5, started_at=clock[0])

    clock[0] = 105.0
    guard.mark_lost(RuntimeError("renewal timed out"))

    assert isinstance(guard.renewal_failure(), TimeoutError)
