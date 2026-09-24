from __future__ import annotations

from volcano_sdk._tests.typing import Any, Literal

# Intentionally invalid examples: unused-ignore makes missing diagnostics fail.
# The normal mypy task checks this file; pytest never executes it.


class Base:
    value: float = 0.0

    def describe(self) -> str:
        return f"base:{self.value}"


class ImplicitOverride(Base):
    def describe(self) -> str:  # type: ignore[explicit-override]  # pyright: ignore[reportImplicitOverride]
        return f"derived:{self.value}"


class NarrowedMutableAttribute(Base):
    value: int  # type: ignore[mutable-override]  # pyright: ignore[reportIncompatibleVariableOverride]


def missing_match_case(value: Literal["first", "second"]) -> None:
    match value:  # type: ignore[exhaustive-match]  # pyright: ignore[reportMatchNotExhaustive]
        case "first":
            return


def possibly_undefined(*, value: bool) -> int:
    if value:
        result = 1
    return result  # type: ignore[possibly-undefined]  # pyright: ignore[reportPossiblyUnboundVariable]


def impossible_none_comparison(value: int) -> bool:
    return value is None  # type: ignore[comparison-overlap]  # pyright: ignore[reportUnnecessaryComparison]


explicit_any: Any = 1  # type: ignore[explicit-any]  # pyright: ignore[reportExplicitAny]
