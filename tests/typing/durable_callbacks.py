"""Durable operation selection preserves callback signatures and results."""

from typing import assert_type

from volcano_sdk.durable_authoring import _callable, _named


def label(value: int, *, prefix: str) -> str:
    return f"{prefix}{value}"


def preserved_signatures() -> None:
    named, named_callback = _named("label", label, "step")
    unnamed, unnamed_callback = _named(label, None, "step")
    omitted, omitted_callback = _named(None, label, "step")
    checked = _callable(label, "map")
    _ = assert_type(named, str | None)
    _ = assert_type(unnamed, str | None)
    _ = assert_type(omitted, str | None)
    _ = assert_type(named_callback(1, prefix="order-"), str)
    _ = assert_type(unnamed_callback(2, prefix="order-"), str)
    _ = assert_type(omitted_callback(3, prefix="order-"), str)
    _ = assert_type(checked(4, prefix="order-"), str)
    _ = named_callback("wrong", prefix="order-")  # type: ignore[arg-type]
    unnamed_callback(1, wrong="order-")  # type: ignore[call-arg]
