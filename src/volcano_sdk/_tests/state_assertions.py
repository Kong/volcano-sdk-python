"""Assertions for state that changes across method calls and asynchronous work."""

from __future__ import annotations


def assert_same(actual: object, *, expected: object) -> None:
    """Check singleton identity without narrowing a mutable caller attribute."""
    assert actual is expected, f"Expected {expected!r}, observed {actual!r}"
