from __future__ import annotations

import asyncio

import pytest

from volcano_sdk import PostgresChange, Session, VolcanoClient
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
from volcano_sdk.realtime import Realtime
from volcano_sdk.storage import Storage, StorageBucket

from .test_durable import EXECUTION_ID, PROJECT_ID, FakeDurableTransport
from .test_facade import FakeTransport, anon_key_with_project_id, signed_in_client
from .test_functions import FakeFunctionsTransport
from .test_logs import FakeLogsTransport
from .test_realtime import (
    FakeCentrifugeClient,
    FakeCentrifugeFactory,
    RealtimeDatabaseTransport,
)


def client_session(access_token: str) -> Session:
    return Session(
        access_token=access_token, refresh_token="refresh-token", user_id="user-1"
    )


def test_direct_auth_updates_the_original_client_session() -> None:
    transport = FakeTransport()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    auth = Auth(client=client)

    session = auth.sign_in(email="user@example.com", password="secret")

    assert auth.get_session() is session
    assert client.auth.get_session() is session
    assert transport.calls == [
        (
            "authSignin",
            {
                "authorization": "anon-key",
                "email": "user@example.com",
                "password": "secret",
            },
        )
    ]


@pytest.mark.parametrize("session_token", [None, "access-token"])
def test_direct_functions_reads_current_client_credentials(
    session_token: str | None,
) -> None:
    transport = FakeFunctionsTransport()
    client = VolcanoClient(
        anon_key="anon-key", service_key="service-key", _transport=transport
    )
    functions = Functions(client=client)
    if session_token is not None:
        _ = client.auth.set_session(client_session(session_token))

    response = functions.invoke("direct-function", {"message": "hello"})

    assert response.data == {"message": "hello", "items": (1, 2)}
    assert transport.calls[-1][1] == {
        "authorization": session_token or "service-key",
        "function_id": "00000000-0000-4000-8000-000000000040",
        "payload": {"message": "hello"},
    }


def test_direct_durable_uses_live_invocation_and_session_credentials() -> None:
    transport = FakeDurableTransport()
    client = VolcanoClient(
        anon_key="anon-key", service_key="service-key", _transport=transport
    )
    durable = Durable(client=client)

    assert durable.start("pipeline").id == EXECUTION_ID
    _ = client.auth.set_session(client_session("platform-token"))
    assert durable.get(PROJECT_ID, "pipeline", EXECUTION_ID).status == "succeeded"
    assert durable.list(PROJECT_ID, "pipeline").total == 2
    assert durable.stop(PROJECT_ID, "pipeline", EXECUTION_ID).id == EXECUTION_ID
    assert [arguments["authorization"] for _, arguments in transport.calls] == [
        "service-key",
        "platform-token",
        "platform-token",
        "platform-token",
    ]


def test_direct_logs_reads_a_session_set_after_construction() -> None:
    transport = FakeLogsTransport()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    logs = Logs(client=client)
    _ = client.auth.set_session(client_session("access-token"))

    page = logs.search("project-1", {"resource": {"type": "function"}})
    activity = logs.activity("project-1", {"resource": {"type": "function"}})

    assert page.next_cursor == "cursor-2"
    assert activity.total == 2
    assert [arguments["authorization"] for _, arguments in transport.calls] == [
        "access-token",
        "access-token",
    ]


def test_direct_storage_and_bucket_preserve_scope_and_binary_results() -> None:
    transport = FakeTransport()
    client = VolcanoClient(
        anon_key=anon_key_with_project_id("project-1"),
        api_url="https://api.example.test",
        _transport=transport,
    )
    storage = Storage(client=client)
    bucket = StorageBucket(_client=client, _name="direct-bucket")
    _ = client.auth.set_session(client_session("access-token"))

    assert storage.from_("nested-bucket").download("message.txt") == b"hello"
    assert bucket.download("message.txt") == b"hello"
    assert bucket.get_public_url("folder/message.txt") == (
        "https://api.example.test/public/project-1/direct-bucket/folder/message.txt"
    )
    assert [arguments["bucket_name"] for _, arguments in transport.calls] == [
        "nested-bucket",
        "direct-bucket",
    ]
    assert all(
        arguments["authorization"] == "access-token" for _, arguments in transport.calls
    )


def test_direct_locks_retains_service_credentials_and_lease_ownership() -> None:
    transport = FakeTransport()
    client = VolcanoClient(
        anon_key="anon-key", service_key="service-key", _transport=transport
    )
    locks = Locks(client=client)
    _ = client.auth.set_session(client_session("user-token"))

    lease = locks.acquire("direct-lock", ttl=30)
    locks.release("direct-lock", lease)

    assert lease.fencing_token == 7
    assert transport.calls[-1][1]["token"] == lease.token
    assert [arguments["authorization"] for _, arguments in transport.calls] == [
        "service-key",
        "service-key",
    ]


def test_direct_database_and_query_builder_preserve_follow_on_state() -> None:
    transport = FakeTransport()
    client = signed_in_client(transport)
    database = Database(_client=client, _name="direct-db")
    query = QueryBuilder(_client=client, _database_name="direct-db", _table="items")

    assert database.from_("items").execute() == [{"slug": "a"}]
    assert query.select("slug").eq("id", 1).order("slug").limit(5).offset(
        2
    ).execute() == [{"slug": "a"}]
    assert transport.calls[-1] == (
        "queryDatabaseSelect",
        {
            "authorization": "access-token",
            "database_name": "direct-db",
            "body": {
                "table": "items",
                "select": ["slug"],
                "filters": [{"column": "id", "operator": "eq", "value": 1}],
                "order": [{"column": "slug", "ascending": True}],
                "limit": 5,
                "offset": 2,
            },
        },
    )


def test_direct_write_builders_accept_client_and_keep_filters() -> None:
    transport = FakeTransport()
    client = signed_in_client(transport)
    insert = InsertBuilder(client, "direct-db", "items", {"slug": "new"})
    update = UpdateBuilder(client, "direct-db", "items", {"slug": "updated"})
    delete = DeleteBuilder(client, "direct-db", "items")

    assert insert.execute() == [{"slug": "new"}]
    assert update.eq("id", 1).execute() == [{"slug": "updated"}]
    assert delete.eq("id", 1).execute() == [{"slug": "updated"}]
    assert transport.calls[-1][1] == {
        "authorization": "access-token",
        "database_name": "direct-db",
        "body": {
            "table": "items",
            "filters": [{"column": "id", "operator": "eq", "value": 1}],
        },
    }


def test_direct_query_follow_on_writes_preserve_the_original_client() -> None:
    transport = FakeTransport()
    client = signed_in_client(transport)
    query = QueryBuilder(client, "direct-db", "items").eq("id", 1)

    assert query.insert({"slug": "new"}).execute() == [{"slug": "new"}]
    assert query.update({"slug": "updated"}).execute() == [{"slug": "updated"}]
    assert query.delete().execute() == [{"slug": "updated"}]
    assert [operation for operation, _ in transport.calls[1:]] == [
        "queryDatabaseInsert",
        "queryDatabaseUpdate",
        "queryDatabaseDelete",
    ]


async def test_direct_realtime_supports_channel_lifecycle() -> None:
    official = FakeCentrifugeClient()
    client = signed_in_client(FakeTransport())
    realtime = Realtime(
        client=client,
        api_url="https://api.example.test",
        client_factory=FakeCentrifugeFactory(official),
    )
    channel = realtime.channel("direct-room")
    try:
        await channel.subscribe()
        await channel.send({"message": "hello"})
        subscription = official.subscription
        assert subscription is not None
        assert subscription.calls == [
            ("subscribe", None),
            ("publish", {"message": "hello"}),
        ]
        await channel.unsubscribe()
    finally:
        await realtime.disconnect()

    assert official.calls == ["connect", f"channel:{channel.name}", "disconnect"]
    assert not official.subscriptions


async def test_direct_realtime_fetches_rows_through_async_client_transport() -> None:
    transport = RealtimeDatabaseTransport([{"id": 42, "body": "fetched"}])
    official = FakeCentrifugeClient()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)
    realtime = Realtime(
        client,
        api_url="https://api.example.test",
        client_factory=FakeCentrifugeFactory(official),
    )
    _ = client.auth.sign_in(email="user@example.com", password="secret")
    realtime.set_database_name("direct-db")
    channel = realtime.channel("public:messages", channel_type="postgres")
    delivered = asyncio.Event()
    changes: list[PostgresChange] = []

    def receive(change: PostgresChange) -> None:
        changes.append(change)
        delivered.set()

    _ = channel.on_postgres_changes(
        "INSERT", schema="public", table="messages", callback=receive
    )
    try:
        await channel.subscribe()
        subscription = official.subscription
        assert subscription is not None
        await subscription.emit(
            {
                "type": "INSERT",
                "schema": "public",
                "table": "messages",
                "id": 42,
                "mode": "lightweight",
                "timestamp": "2026-09-03T12:00:00Z",
            }
        )
        _ = await asyncio.wait_for(delivered.wait(), timeout=1)
    finally:
        await realtime.disconnect()

    assert changes[0].record == {"id": 42, "body": "fetched"}
    assert transport.queries[0]["authorization"] == "access-1"
    assert transport.queries[0]["database_name"] == "direct-db"
