from __future__ import annotations

import pytest

from volcano_sdk import _function_resolution, client, locks

from .client_inspection import InspectedAuthRequests, InspectedSessionOperations
from .lock_inspection import InspectedLockGuard


@pytest.fixture(autouse=True)
def isolate_function_resolution_cache() -> None:
    """Function name resolutions are cached process-wide; keep tests independent."""
    _function_resolution.clear()


@pytest.fixture(autouse=True)
def inspect_session_lifecycle(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(client, "AuthRequests", InspectedAuthRequests)
    monkeypatch.setattr(client, "SessionOperations", InspectedSessionOperations)


@pytest.fixture(autouse=True)
def inspect_lock_lifecycle(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(locks, "ManagedLockGuard", InspectedLockGuard)
