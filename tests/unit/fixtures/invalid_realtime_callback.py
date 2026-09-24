from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from volcano_sdk.realtime import (
        Channel,
        MessageCallback,
        Realtime,
        RealtimeCallback,
    )


def register_non_callable(realtime: Realtime) -> None:
    # Native mypy must report arg-type; unused-ignore rejects a missing diagnostic.
    _ = realtime.on_connect(None)  # type: ignore[arg-type]


def register_callback_without_message(channel: Channel) -> None:
    def receive_nothing() -> None:
        return None

    _ = channel.on("message", receive_nothing)  # type: ignore[arg-type]


def assign_callback_without_message() -> None:
    def receive_nothing() -> None:
        return None

    message_callback: MessageCallback = receive_nothing  # type: ignore[assignment]
    realtime_callback: RealtimeCallback = receive_nothing  # type: ignore[assignment]
    del message_callback, realtime_callback
