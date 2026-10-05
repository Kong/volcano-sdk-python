from __future__ import annotations

from pathlib import Path

import pytest

PROPERTY_SUPPORT = (
    Path(__file__)
    .parents[2]
    .joinpath("src/volcano_sdk/_tests/property_support.py")
    .read_text()
)


def test_failing_property_preserves_seed_and_counterexample(
    pytester: pytest.Pytester,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("VOLCANO_PROPERTY_SEED", "12345")
    _ = pytester.makepyfile(property_support=PROPERTY_SUPPORT)
    _ = pytester.makepyfile(
        """
        from hypothesis import given, seed, strategies as st
        from property_support import PROPERTY_SEED

        @seed(PROPERTY_SEED)
        @given(st.integers(min_value=0, max_value=100))
        def test_property(value):
            assert value < 0
        """,
    )
    result = pytester.runpytest_subprocess("-q", "--junitxml=reports/unit.xml")
    result.assert_outcomes(failed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    assert (pytester.path / "reports/hypothesis/seed.txt").read_text() == "12345\n"
    report = (pytester.path / "reports/unit.xml").read_text()
    assert "Failing test case:" in report
    assert "value=0" in report
    assert "@reproduce_failure(" in report
