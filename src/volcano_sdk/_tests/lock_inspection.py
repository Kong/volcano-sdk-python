"""Typed test subclasses for lock ownership and renewal behavior."""

from __future__ import annotations

from typing import TYPE_CHECKING

from volcano_sdk._lock_guard import ManagedLockGuard
from volcano_sdk._lock_worker import LockRenewer
from volcano_sdk.locks import Locks

if TYPE_CHECKING:
    from threading import Event, Thread


class InspectedLockGuard(ManagedLockGuard):
    def remaining_seconds(self) -> float:
        return self._remaining_seconds()

    def loss_event(self) -> Event:
        return self._lost


class InspectedLockRenewer(LockRenewer):
    def renew_once(self) -> bool:
        return self._renew_once()

    def run_worker(self) -> None:
        self._run()

    def wait_until_renewal(self) -> bool:
        return self._wait_until_renewal()

    def worker_thread(self) -> Thread:
        return self._thread

    def stop_event(self) -> Event:
        return self._stop


class InspectedLocks(Locks):
    def prepare_guard(self, key: str, guard: ManagedLockGuard, *, ttl: int) -> None:
        self._prepare_guard(key, guard, ttl=ttl)
