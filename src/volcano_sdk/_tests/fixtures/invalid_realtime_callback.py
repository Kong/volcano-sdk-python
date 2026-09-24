from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from volcano_sdk.realtime import (
        Channel,
        MessageCallback,
        Realtime,
        RealtimeCallback,
        RealtimeConnectContext,
    )


def register_non_callable(realtime: Realtime) -> None:
    # Native mypy must report arg-type; unused-ignore rejects a missing diagnostic.
    _ = realtime.on_connect(None)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


def register_callback_without_message(channel: Channel) -> None:
    def receive_nothing() -> None:
        return None

    _ = channel.on("message", receive_nothing)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


def assign_callback_without_message() -> None:
    def receive_nothing() -> None:
        return None

    message_callback: MessageCallback[str] = receive_nothing  # type: ignore[assignment]  # pyright: ignore[reportAssignmentType]
    realtime_callback: RealtimeCallback[RealtimeConnectContext] = receive_nothing  # type: ignore[assignment]  # pyright: ignore[reportAssignmentType]
    del message_callback, realtime_callback


def assign_narrow_callbacks() -> None:
    def receive_message(message: str) -> None:
        del message

    def connected(context: RealtimeConnectContext) -> None:
        del context

    message_callback: MessageCallback[str] = receive_message
    realtime_callback: RealtimeCallback[RealtimeConnectContext] = connected
    del message_callback, realtime_callback
