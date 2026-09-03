from __future__ import annotations

import time
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from volcano_sdk import LockLease
from volcano_sdk import _lock_guard as guard_module
from volcano_sdk._lock_guard import LockGuard

if TYPE_CHECKING:
    import pytest


def lease(*, expires_at: datetime | None = None) -> LockLease:
    return LockLease(
        key="build",
        token="00000000-0000-4000-8000-000000000001",
        expires_at=expires_at,
        fencing_token=7,
    )


def test_lease_clock_falls_back_to_portable_monotonic(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delattr(time, "clock_gettime", raising=False)
    monkeypatch.setattr(time, "monotonic", lambda: 123.0)

    assert guard_module._lease_now() == 123.0


def test_lock_guard_exposes_the_latest_immutable_lease(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [100.0]
    monkeypatch.setattr(guard_module, "_lease_now", lambda: clock[0])
    original = lease(expires_at=datetime(2026, 9, 3, 12, 0, 5, tzinfo=UTC))
    renewed = lease(expires_at=datetime(2026, 9, 3, 12, 0, 9, tzinfo=UTC))
    guard = LockGuard(original, ttl=5, started_at=clock[0])

    clock[0] = 104.0
    assert guard._replace_lease(renewed, started_at=clock[0])

    assert guard.lease is renewed
    assert not guard.lost
    assert guard._remaining_seconds() == 5.0


def test_lock_guard_rejects_a_renewal_completed_after_lease_expiry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [100.0]
    monkeypatch.setattr(guard_module, "_lease_now", lambda: clock[0])
    original = lease()
    guard = LockGuard(original, ttl=5, started_at=clock[0])

    clock[0] = 105.0

    assert not guard._replace_lease(lease(), started_at=104.0)
    assert guard.lease is original
    assert guard.lost
    assert isinstance(guard._renewal_failure(), TimeoutError)


def test_lock_guard_detects_suspend_aware_expiry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [100.0]
    monkeypatch.setattr(guard_module, "_lease_now", lambda: clock[0])
    guard = LockGuard(lease(), ttl=5, started_at=clock[0])

    clock[0] = 105.0

    assert guard.wait_lost(timeout=0)
    assert guard.lost


def test_lock_guard_wait_times_out_while_the_lease_is_held(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(guard_module, "_lease_now", lambda: 100.0)
    guard = LockGuard(lease(), ttl=5, started_at=100.0)

    assert not guard.wait_lost(timeout=0)
    assert not guard.lost


def test_lock_guard_preserves_the_absolute_acquisition_deadline(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [0.0]
    monkeypatch.setattr(guard_module, "_lease_now", lambda: clock[0])
    guard = LockGuard(
        lease(),
        ttl=guard_module.MAX_LOCK_LIFETIME_SECONDS,
        started_at=clock[0],
    )

    clock[0] = guard_module.MAX_LOCK_LIFETIME_SECONDS - 1
    assert guard._replace_lease(lease(), started_at=clock[0])

    assert guard._remaining_seconds() == 1.0


def test_lock_guard_preserves_the_first_loss_reason(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(guard_module, "_lease_now", lambda: 100.0)
    guard = LockGuard(lease(), ttl=5, started_at=100.0)
    first = RuntimeError("renewal failed")

    guard._mark_lost(first)
    guard._mark_lost(RuntimeError("later failure"))

    assert guard.lost
    assert guard.wait_lost(timeout=0)
    assert guard._renewal_failure() is first
