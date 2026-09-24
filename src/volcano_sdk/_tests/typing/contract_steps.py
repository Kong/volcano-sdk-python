"""Behave registration preserves the argument types of each step."""

from __future__ import annotations

from typing import TYPE_CHECKING, assert_type

from behave import given, then, when

if TYPE_CHECKING:
    from behave.runner import Context


@given("a typed count {count:d}")
@when("the typed count becomes {count:d}")
@then("the typed count is {count:d}")
def counted_step(context: Context, count: int) -> None:
    context.count = count


def check_step_types(context: Context) -> None:
    assert_type(counted_step(context, 1), None)
    counted_step(context, "invalid")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
    counted_step("invalid", 1)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
