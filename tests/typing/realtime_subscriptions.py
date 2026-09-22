"""Subscription lookup preserves the value and fallback types."""

from typing import assert_type

from volcano_sdk.realtime import _ProjectAwareSubscriptions


def subscription_types() -> None:
    subscriptions = _ProjectAwareSubscriptions[str]({"room": "subscription"})
    assert_type(subscriptions.get("room"), str | None)
    assert_type(subscriptions.get("project:room", None), str | None)
    assert_type(subscriptions.get("project:room", "fallback"), str)
    assert_type(subscriptions.get("missing", 0), str | int)
    assert_type(subscriptions.get(key="missing", default=b"fallback"), str | bytes)
    subscriptions["room"] = 1  # type: ignore[assignment]
    subscriptions.get(1)  # type: ignore[call-overload]
