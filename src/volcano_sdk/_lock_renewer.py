"""Renewal scheduling for automatically held lock leases."""

from __future__ import annotations

import secrets

MAX_RENEWAL_DELAY_SECONDS = 60.0
RENEWAL_SAFETY_MARGIN_SECONDS = 1.0
RENEWAL_REQUEST_BUDGET_SECONDS = 1.0
_JITTER_STEPS = 2_001
_JITTER_SCALE = 10_000
_MINIMUM_JITTER = 0.1


def _renewal_jitter() -> float:
    return (secrets.randbelow(_JITTER_STEPS) / _JITTER_SCALE) - _MINIMUM_JITTER


def renewal_delay(ttl: int, *, remaining: float) -> float:
    """Choose a jittered renewal time inside the current lease window."""
    latest = max(
        0.0,
        remaining - RENEWAL_SAFETY_MARGIN_SECONDS - RENEWAL_REQUEST_BUDGET_SECONDS,
    )
    delay = min(ttl / 3, MAX_RENEWAL_DELAY_SECONDS, latest)
    return min(
        max(0.0, delay * (1 + _renewal_jitter())),
        MAX_RENEWAL_DELAY_SECONDS,
        latest,
    )
