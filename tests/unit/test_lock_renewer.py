from __future__ import annotations

import pytest

from volcano_sdk import _lock_renewer as renewer


@pytest.mark.parametrize(
    ("ttl", "remaining", "draw", "expected"),
    [
        (30, 30.0, 1_000, 10.0),
        (300, 300.0, 1_000, 60.0),
        (30, 30.0, 0, 9.0),
        (30, 30.0, 2_000, 11.0),
        (30, 2.5, 2_000, 0.5),
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
