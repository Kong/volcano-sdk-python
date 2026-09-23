from __future__ import annotations

import secrets

import pytest

from volcano_sdk import _lock_renewer as renewer


@pytest.mark.parametrize(
    ("ttl", "remaining", "draw", "expected"),
    [
        (30, 30.0, 1_000, 10.0),
        (300, 300.0, 1_000, 60.0),
        (300, 300.0, 2_000, 60.0),
        (300, 300.0, 0, 54.0),
        (30, 30.0, 0, 9.0),
        (30, 30.0, 2_000, 11.0),
        (30, 2.5, 2_000, 0.5),
        (30, 5.0, 0, 2.7),
        (30, 2.5, 0, 0.45),
        (30, 2.0, 1_000, 0.0),
    ],
)
def test_renewal_delay_stays_inside_the_safe_lease_window(
    monkeypatch: pytest.MonkeyPatch,
    ttl: int,
    remaining: float,
    draw: int,
    expected: float,
) -> None:
    jitter = (draw / 10_000) - 0.1
    monkeypatch.setattr(renewer, "_renewal_jitter", lambda: jitter)

    assert renewer.renewal_delay(ttl, remaining=remaining) == expected


@pytest.mark.parametrize(("draw", "expected"), [(0, -0.1), (2_000, 0.1)])
def test_renewal_jitter_is_symmetric_at_the_draw_boundaries(
    monkeypatch: pytest.MonkeyPatch, draw: int, expected: float
) -> None:
    def draw_number(_stop: int) -> int:
        return draw

    monkeypatch.setattr(secrets, "randbelow", draw_number)

    assert renewer._renewal_jitter() == pytest.approx(expected)
