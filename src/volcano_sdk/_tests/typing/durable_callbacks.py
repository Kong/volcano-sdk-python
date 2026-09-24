"""Durable operation selection preserves callback signatures and results."""

from typing import assert_type

from volcano_sdk._callbacks import named_operation, operation_callable


def label(value: int, *, prefix: str) -> str:
    return f"{prefix}{value}"


def preserved_signatures() -> None:
    named, named_callback = named_operation("label", label, "step")
    unnamed, unnamed_callback = named_operation(label, None, "step")
    omitted, omitted_callback = named_operation(None, label, "step")
    checked = operation_callable(label, "map")
    _ = assert_type(named, str | None)
    _ = assert_type(unnamed, str | None)
    _ = assert_type(omitted, str | None)
    _ = assert_type(named_callback(1, prefix="order-"), str)
    _ = assert_type(unnamed_callback(2, prefix="order-"), str)
    _ = assert_type(omitted_callback(3, prefix="order-"), str)
    _ = assert_type(checked(4, prefix="order-"), str)
    _ = named_callback("wrong", prefix="order-")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
    unnamed_callback(1, wrong="order-")  # type: ignore[call-arg]  # pyright: ignore[reportCallIssue]
