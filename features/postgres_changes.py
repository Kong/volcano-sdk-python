from __future__ import annotations

import asyncio
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from collections.abc import Mapping

    from contract_support import ContractWorld

    from volcano_sdk.models import JSONValue
    from volcano_sdk.realtime import Channel, PostgresChange


class ChangeObserver:
    def __init__(self, channel: Channel, table: str, row_id: JSONValue) -> None:
        self.row_id = row_id
        self.events: list[PostgresChange] = []
        self.queue: asyncio.Queue[PostgresChange] = asyncio.Queue()
        self.inserts: list[PostgresChange] = []
        self.wrong_table: list[PostgresChange] = []
        self.stops = [
            channel.on_postgres_changes(
                "*", schema="public", table=table, callback=self.record
            ),
            channel.on_postgres_changes(
                "INSERT", schema="public", table=table, callback=self.record_insert
            ),
            channel.on_postgres_changes(
                "*",
                schema="public",
                table=table + "_other",
                callback=self.record_wrong_table,
            ),
        ]

    def owns(self, change: PostgresChange) -> bool:
        identity = change.record.get("id") if change.record is not None else change.id
        return identity == self.row_id

    def record_insert(self, change: PostgresChange) -> None:
        if self.owns(change):
            self.inserts.append(change)

    def record_wrong_table(self, change: PostgresChange) -> None:
        if self.owns(change):
            self.wrong_table.append(change)

    def record(self, change: PostgresChange) -> None:
        if not self.owns(change):
            return
        self.events.append(change)
        self.queue.put_nowait(change)

    async def next(self) -> PostgresChange:
        return await asyncio.wait_for(self.queue.get(), timeout=10)

    def close(self) -> None:
        for stop in self.stops:
            stop()


def verify_change(
    event: PostgresChange,
    kind: str,
    table: str,
    row: Mapping[str, JSONValue],
    *,
    automatic: bool,
) -> None:
    assert (event.type, event.schema, event.table) == (kind, "public", table)
    datetime.fromisoformat(event.timestamp)
    if automatic:
        assert event.record == row
        assert event.id is None
        assert event.mode is None
    else:
        assert event.id == row["id"]
        assert event.mode == "lightweight"
        assert event.record is None


async def verify_postgres_changes(world: ContractWorld) -> list[str]:
    table_name = world.fixture["realtime_table_name"]
    row: dict[str, JSONValue] = {
        "id": str(uuid4()),
        "value": "inserted",
        "owner_id": world.fixture["user_id"],
    }
    table = world.client.database(world.fixture["database_name"]).from_(table_name)
    world.cleanup_callbacks.append(lambda: table.delete().eq("id", row["id"]).execute())
    channels = postgres_channels(world, table_name)
    observers = [ChangeObserver(channel, table_name, row["id"]) for channel in channels]
    try:
        await asyncio.gather(*(channel.subscribe() for channel in channels))
        for index, kind in enumerate(["INSERT", "UPDATE"]):
            expected = {**row, "value": "inserted" if index == 0 else "updated"}
            operation = (
                table.insert(expected)
                if index == 0
                else table.update({"value": expected["value"]}).eq("id", row["id"])
            )
            assert await asyncio.to_thread(operation.execute) == [expected]
            events = await asyncio.gather(*(observer.next() for observer in observers))
            for client_index, event in enumerate(events):
                verify_change(
                    event, kind, table_name, expected, automatic=client_index == 0
                )
        for observer in observers:
            assert [event.type for event in observer.events] == ["INSERT", "UPDATE"]
            assert len(observer.inserts) == 1
            assert not observer.wrong_table
    finally:
        for observer in observers:
            observer.close()
        await asyncio.gather(*(channel.unsubscribe() for channel in channels))
    return ["INSERT", "UPDATE"]


def postgres_channels(world: ContractWorld, table_name: str) -> list[Channel]:
    channels: list[Channel] = []
    for index, client in enumerate(world.realtime_clients):
        client.realtime.set_database_name(world.fixture["database_name"])
        channels.append(
            client.realtime.channel(
                "public:" + table_name,
                channel_type="postgres",
                auto_fetch=index == 0,
            )
        )
    return channels
