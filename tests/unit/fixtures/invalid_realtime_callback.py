from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from volcano_sdk.realtime import Channel, Realtime


def register_non_callable(realtime: Realtime) -> None:
    # Native mypy must report arg-type; unused-ignore rejects a missing diagnostic.
    realtime.on_connect(None)  # type: ignore[arg-type]


def register_unsupported_postgres_event(channel: Channel) -> None:
    channel.on_postgres_changes(
        "UPSERT",  # type: ignore[arg-type]
        schema="public",
        table="messages",
        callback=lambda _change: None,
    )
