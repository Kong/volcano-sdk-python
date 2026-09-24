from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from volcano_sdk import PostgresChange, VolcanoClient
from volcano_sdk.realtime import _filter_postgres_changes, _postgres_change

if TYPE_CHECKING:
    from volcano_sdk.realtime import ChannelType, PostgresEvent, PostgresListenerEvent


@pytest.mark.parametrize("payload", [None, [], False, "change", 42])
def test_postgres_parser_rejects_non_object_publications(payload: object) -> None:
    assert _postgres_change(payload) is None


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("mode", "unknown"),
        ("mode", False),
        ("mode", []),
        ("columns", "id"),
        ("columns", {"id": True}),
        ("columns", ["id", 42]),
        ("columns", ("id", None)),
    ],
)
def test_postgres_parser_rejects_invalid_delivery_metadata(
    field: str, value: object
) -> None:
    payload = {
        "type": "UPDATE",
        "schema": "public",
        "table": "messages",
        "timestamp": "2026-09-22T12:00:00Z",
        "record": {"id": 42},
        field: value,
    }

    assert _postgres_change(payload) is None


@pytest.mark.parametrize("columns", [None, [], (), ["id", "body"], ("id", "body")])
def test_postgres_parser_preserves_valid_column_metadata(
    columns: list[str] | tuple[str, ...] | None,
) -> None:
    change = _postgres_change(
        {
            "type": "UPDATE",
            "schema": "public",
            "table": "messages",
            "timestamp": "2026-09-22T12:00:00Z",
            "columns": columns,
        }
    )

    assert change is not None
    assert change.columns == (None if columns is None else tuple(columns))


@pytest.mark.parametrize(
    ("listener_event", "event", "schema", "table", "matches"),
    [
        ("UPDATE", "UPDATE", "public", "messages", True),
        ("*", "INSERT", "public", "messages", True),
        ("UPDATE", "INSERT", "public", "messages", False),
        ("UPDATE", "UPDATE", "private", "messages", False),
        ("UPDATE", "UPDATE", "public", "other", False),
    ],
)
def test_postgres_filter_delivers_only_matching_changes(
    listener_event: PostgresListenerEvent,
    event: PostgresEvent,
    schema: str,
    table: str,
    *,
    matches: bool,
) -> None:
    changes: list[PostgresChange] = []

    def callback(change: PostgresChange) -> str:
        changes.append(change)
        return "delivered"

    listener = _filter_postgres_changes(listener_event, "public", "messages", callback)
    change = PostgresChange(type=event, schema=schema, table=table)

    assert listener(change) == ("delivered" if matches else None)
    assert changes == ([change] if matches else [])


@pytest.mark.parametrize("channel_type", ["broadcast", "presence", "postgres"])
def test_channel_rejects_unsupported_events(channel_type: ChannelType) -> None:
    channel = VolcanoClient(anon_key="anon").realtime.channel(
        "events", channel_type=channel_type
    )
    with pytest.raises(ValueError, match="unsupported realtime event: invalid"):
        _ = channel.on("invalid", lambda _value: None)
