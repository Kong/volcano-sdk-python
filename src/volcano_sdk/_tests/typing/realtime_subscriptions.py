"""Subscription lookup preserves the value and fallback types."""

from collections.abc import Mapping

from volcano_sdk._realtime_transport import (
    ProjectAwareSubscriptions,
)
from volcano_sdk._tests.typing import assert_type
from volcano_sdk.realtime import (
    Channel,
    Realtime,
    RealtimePresenceInfo,
)


def subscription_types() -> None:
    subscriptions = ProjectAwareSubscriptions[str]({"room": "subscription"})
    _room = assert_type(subscriptions.get("room"), str | None)
    _room_alias = assert_type(subscriptions.get("project:room", None), str | None)
    _fallback_str = assert_type(subscriptions.get("project:room", "fallback"), str)
    _fallback_int = assert_type(subscriptions.get("missing", 0), str | int)
    _fallback_bytes = assert_type(
        subscriptions.get(key="missing", default=b"fallback"), str | bytes
    )
    subscriptions["room"] = 1  # type: ignore[assignment]  # pyright: ignore[reportArgumentType]
    _ = subscriptions.get(1)  # type: ignore[call-overload]  # pyright: ignore[reportArgumentType]


def legacy_callback_types(channel: Channel) -> None:
    """Generic message callbacks keep the established caller-defined payload type."""

    def text_message(value: str) -> str:
        return value.upper()

    def record_message(value: dict[str, int]) -> int:
        return value["count"]

    _text_channel = assert_type(channel.on("message", text_message), Channel)
    _record_channel = assert_type(channel.on("message", record_message), Channel)


async def channel_facade_types(realtime: Realtime) -> None:
    """The public factory preserves channel methods across the internal split."""
    channel = assert_type(realtime.channel("members", channel_type="presence"), Channel)
    _name = assert_type(channel.name, str)
    _presence = assert_type(
        channel.get_presence_state(), Mapping[str, RealtimePresenceInfo]
    )
    await channel.subscribe()
    await channel.track({"status": "online"})
    await channel.unsubscribe()
    await realtime.remove_channel("members", channel_type="presence")
    await realtime.remove_all_channels()
    await realtime.disconnect()
