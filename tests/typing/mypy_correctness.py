from __future__ import annotations

from typing import Literal

# Intentionally invalid examples: unused-ignore makes missing diagnostics fail.
# The normal mypy task checks this file; pytest never executes it.


class Base:
    value: float

    def describe(self) -> str:
        return "base"


class ImplicitOverride(Base):
    def describe(self) -> str:  # type: ignore[explicit-override]
        return "derived"


class NarrowedMutableAttribute(Base):
    value: int  # type: ignore[mutable-override]


def missing_match_case(value: Literal["first", "second"]) -> None:
    match value:  # type: ignore[exhaustive-match]
        case "first":
            return


def possibly_undefined(*, value: bool) -> int:
    if value:
        result = 1
    return result  # type: ignore[possibly-undefined]


def impossible_none_comparison(value: int) -> bool:
    return value is None  # type: ignore[comparison-overlap]
