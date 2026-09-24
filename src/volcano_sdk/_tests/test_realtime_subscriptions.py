from __future__ import annotations

import pytest

from volcano_sdk._realtime_transport import (
    ProjectAwareSubscriptions,
    VolcanoCentrifugeConnection,
)

from .test_realtime import FakeCentrifugeClient


def test_subscription_lookup_preserves_exact_and_most_specific_matches() -> None:
    subscriptions = ProjectAwareSubscriptions[str](
        {"room": "short", "broadcast:room": "specific", "project:room": "exact"}
    )

    assert subscriptions.get("project:room") == "exact"
    assert subscriptions.get("project:broadcast:room") == "specific"
    assert subscriptions.get("other:room") == "short"


def test_subscription_lookup_preserves_missing_defaults() -> None:
    subscriptions = ProjectAwareSubscriptions[str]({"room": "subscription"})

    assert subscriptions.get("missing") is None
    assert subscriptions.get("missing", 0) == 0
    assert subscriptions.get(key="missing", default=b"fallback") == b"fallback"


def test_native_adapter_preserves_existing_subscription_identity() -> None:
    native = FakeCentrifugeClient()
    subscription = native.new_subscription("broadcast:room", events=None)

    _ = VolcanoCentrifugeConnection(native)

    assert native.subscriptions.get("project:broadcast:room") is subscription


@pytest.mark.parametrize("registry", [None, [], {1: object()}])
def test_native_adapter_rejects_incompatible_registry_without_replacing_it(
    monkeypatch: pytest.MonkeyPatch, registry: object
) -> None:
    native = FakeCentrifugeClient()
    monkeypatch.setattr(native, "_subs", registry)

    with pytest.raises(TypeError, match="subscription registry"):
        _ = VolcanoCentrifugeConnection(native)

    assert native.subscriptions is registry
