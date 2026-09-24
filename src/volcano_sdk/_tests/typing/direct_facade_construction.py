"""Direct public facade constructors continue to accept VolcanoClient."""

from __future__ import annotations

from typing import TYPE_CHECKING, assert_type

from volcano_sdk.auth import Auth
from volcano_sdk.database import (
    Database,
    DeleteBuilder,
    InsertBuilder,
    QueryBuilder,
    UpdateBuilder,
)
from volcano_sdk.durable import Durable
from volcano_sdk.functions import Functions
from volcano_sdk.locks import Locks
from volcano_sdk.logs import Logs
from volcano_sdk.realtime import Channel, Realtime
from volcano_sdk.storage import Storage, StorageBucket

if TYPE_CHECKING:
    from volcano_sdk import VolcanoClient


def direct_facades(client: VolcanoClient) -> None:
    _ = assert_type(Auth(client=client), Auth)
    _ = assert_type(Functions(client=client), Functions)
    _ = assert_type(Durable(client=client), Durable)
    _ = assert_type(Logs(client=client), Logs)
    _ = assert_type(Storage(client=client).from_("bucket"), StorageBucket)
    _ = assert_type(StorageBucket(_client=client, _name="bucket"), StorageBucket)
    _ = assert_type(Locks(client=client), Locks)
    _ = assert_type(
        Database(_client=client, _name="database").from_("items"), QueryBuilder
    )


def direct_query_builders(client: VolcanoClient) -> None:
    query = assert_type(
        QueryBuilder(_client=client, _database_name="database", _table="items"),
        QueryBuilder,
    )
    _ = assert_type(
        query.select("id").eq("id", 1).order("id").limit(2).offset(1), QueryBuilder
    )
    _ = assert_type(query.insert({"id": 1}), InsertBuilder)
    _ = assert_type(query.update({"id": 2}).eq("id", 1), UpdateBuilder)
    _ = assert_type(query.delete().eq("id", 1), DeleteBuilder)
    _ = assert_type(
        InsertBuilder(
            _client=client, _database_name="database", _table="items", _values={"id": 1}
        ),
        InsertBuilder,
    )
    _ = assert_type(
        UpdateBuilder(
            _client=client, _database_name="database", _table="items", _values={"id": 2}
        ).eq("id", 1),
        UpdateBuilder,
    )
    _ = assert_type(
        DeleteBuilder(_client=client, _database_name="database", _table="items").eq(
            "id", 1
        ),
        DeleteBuilder,
    )


async def direct_realtime(client: VolcanoClient) -> None:
    realtime = assert_type(
        Realtime(client=client, api_url="https://api.example.test"), Realtime
    )
    channel = assert_type(realtime.channel("room"), Channel)
    await channel.subscribe()
    await channel.send({"message": "hello"})
    await channel.unsubscribe()
    await realtime.remove_channel("room")
    await realtime.remove_all_channels()
    await realtime.disconnect()
