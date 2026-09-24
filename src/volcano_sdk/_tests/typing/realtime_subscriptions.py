"""Subscription lookup preserves the value and fallback types."""

from typing import assert_type

from volcano_sdk.realtime import _ProjectAwareSubscriptions


def subscription_types() -> None:
    subscriptions = _ProjectAwareSubscriptions[str]({"room": "subscription"})
    _room = assert_type(subscriptions.get("room"), str | None)
    _room_alias = assert_type(subscriptions.get("project:room", None), str | None)
    _fallback_str = assert_type(subscriptions.get("project:room", "fallback"), str)
    _fallback_int = assert_type(subscriptions.get("missing", 0), str | int)
    _fallback_bytes = assert_type(
        subscriptions.get(key="missing", default=b"fallback"), str | bytes
    )
    subscriptions["room"] = 1  # type: ignore[assignment]  # pyright: ignore[reportArgumentType]
    _ = subscriptions.get(1)  # type: ignore[call-overload]  # pyright: ignore[reportArgumentType]
