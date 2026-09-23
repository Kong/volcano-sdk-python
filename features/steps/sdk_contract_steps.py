from __future__ import annotations

import asyncio
import time
from collections.abc import Mapping
from contextlib import suppress
from dataclasses import replace
from datetime import datetime
from typing import TYPE_CHECKING, TypedDict, TypeGuard, TypeVar, cast
from uuid import uuid4

import httpx
from behave import given, then, when
from broadcast_pause import verify_broadcast_pause
from contract_support import (
    CONTRACT_EXCEPTIONS,
    ContractWorld,
    Outcome,
    classify_error,
)
from logs_contract import LogContract
from postgres_changes import verify_postgres_changes
from presence_membership import verify_presence_membership

from volcano_sdk import (
    DurableExecution,
    DurableExecutionPage,
    FunctionResponse,
    LockLease,
    LockState,
    LogActivityResponse,
    NotFoundError,
    Session,
    SessionPage,
    User,
    VolcanoClient,
)
from volcano_sdk.models import (
    StorageObject,
    UploadPart,
    UploadSession,
    UploadSessionStatus,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from behave.runner import Context

    from volcano_sdk.database import QueryBuilder
    from volcano_sdk.models import JSONValue
    from volcano_sdk.realtime import Channel
    from volcano_sdk.storage import StorageBucket

ACCESS_TOKEN_CLOCK_TICK_SECONDS = 1.1
HTTP_OK = 200
MULTIPART_PART_COUNT = 2
DURABLE_START_COUNT = 2
STORAGE_LIFECYCLE_DOWNLOAD_COUNT = 4
REJECTED_BEARER = "sdk-contract-rejected-access-token"
PRESENCE_ROSTERS_SUFFIX = "and the original handler observes membership changes"
_ValueT = TypeVar("_ValueT")


class PartialUpload(TypedDict):
    session: UploadSession
    part: UploadPart
    bytes: bytes


class ResumedUpload(PartialUpload):
    progress: UploadSessionStatus
    object: StorageObject
    download: bytes


class StorageDownloadResult(TypedDict):
    bytes: bytes
    path: str


class StorageMetadataResult(StorageDownloadResult):
    content_type: str
    listed: list[dict[str, str]]


class StorageLifecycleResult(TypedDict):
    bytes: list[bytes]
    after_move: list[str]
    after_remove: list[str]


class StorageVisibilityResult(TypedDict):
    statuses: list[int]
    bytes: bytes
    visibility: list[bool]
    private_bytes: list[bytes]


class LockReleaseResult(TypedDict):
    lease: LockLease
    released: bool


class LockRecoveryResult(TypedDict):
    token: str
    cleanup: Callable[[], None]
    lease: LockLease
    recovered: LockLease
    held: LockState
    renewed: LockLease
    available: LockState


def uploaded_text_field(uploaded: dict[str, object], field: str) -> str:
    value = uploaded[field]
    assert isinstance(value, str)
    return value


def _world(context: Context) -> ContractWorld:
    world = cast("object", context.contract)
    assert isinstance(world, ContractWorld)
    return world


def _logs_contract(context: Context) -> LogContract:
    logs_contract = cast("object", context.logs_contract)
    assert isinstance(logs_contract, LogContract)
    return logs_contract


def _outcome(context: Context) -> Outcome:
    outcome = _world(context).last_outcome
    assert outcome is not None
    return outcome


def _value(context: Context, expected: type[_ValueT]) -> _ValueT:
    value = _outcome(context).value
    assert isinstance(value, expected)
    return value


def _value_dict(context: Context) -> dict[str, object]:
    value = _outcome(context).value
    assert isinstance(value, dict)
    entries = cast("dict[object, object]", value)
    result: dict[str, object] = {}
    for key, item in entries.items():
        assert isinstance(key, str)
        result[key] = item
    return result


def _object_list(value: object) -> list[object]:
    assert isinstance(value, list)
    return cast("list[object]", value)


def _is_json_value(value: object) -> TypeGuard[JSONValue]:
    if value is None or isinstance(value, (str, int, float, bool)):
        return True
    if isinstance(value, (list, tuple)):
        items = cast("list[object] | tuple[object, ...]", value)
        return all(_is_json_value(item) for item in items)
    if isinstance(value, Mapping):
        entries = cast("Mapping[object, object]", value)
        return all(
            isinstance(key, str) and _is_json_value(item)
            for key, item in entries.items()
        )
    return False


def _log_events(value: object) -> list[Mapping[str, JSONValue]]:
    assert isinstance(value, list)
    events = cast("list[object]", value)
    assert all(_is_json_value(event) and isinstance(event, Mapping) for event in events)
    return cast("list[Mapping[str, JSONValue]]", value)


def _remove_cleanup(world: ContractWorld, candidate: object) -> None:
    for callback in world.cleanup_callbacks:
        if callback is candidate:
            world.cleanup_callbacks.remove(callback)
            return
    msg = "Expected registered contract cleanup callback"
    raise AssertionError(msg)


@given("the confirmed contract user")
def confirmed_contract_user(context: Context) -> None:
    assert _world(context).fixture["user_id"]


@given("the client listens for auth state changes")
def listen_for_auth_state_changes(context: Context) -> None:
    world = _world(context)
    subscription = world.client.auth.on_auth_state_change(
        lambda event, session: world.auth_state_events.append((event, session))
    )
    world.cleanup_callbacks.append(subscription.unsubscribe)


@when("the client signs in with the contract user's credentials")
def sign_in(context: Context) -> None:
    world = _world(context)
    _ = world.record(
        lambda: world.client.auth.sign_in(
            email=world.fixture["user_email"],
            password=world.fixture["user_password"],
        )
    )


@when("the client reads the current session")
def read_current_session(context: Context) -> None:
    world = _world(context)
    _ = world.record(world.client.auth.get_session)


@when("a fresh client adopts the current session")
def adopt_current_session(context: Context) -> None:
    world = _world(context)
    source = world.client.auth.get_session()
    assert source is not None
    target = VolcanoClient(
        api_url=world.fixture["api_url"],
        anon_key=world.fixture["anon_key"],
    )
    _ = world.record(lambda: target.auth.set_session(source))
    world.client = target


@when("the client refreshes the current session")
def refresh_current_session(context: Context) -> None:
    world = _world(context)
    world.previous_session = world.client.auth.get_session()
    assert world.previous_session is not None
    time.sleep(ACCESS_TOKEN_CLOCK_TICK_SECONDS)
    _ = world.record(world.client.auth.refresh_session)


@when("a fresh client tries to refresh a supplied profile without a session identifier")
def refresh_supplied_profile_without_sid(context: Context) -> None:
    world = _world(context)
    source = world.client.auth.get_session()
    assert source is not None
    target = VolcanoClient(
        api_url=world.fixture["api_url"], anon_key=world.fixture["anon_key"]
    )
    supplied = target.auth.set_session(replace(source, access_token=REJECTED_BEARER))
    _ = world.record(target.auth.refresh_session)
    assert target.auth.get_session() == supplied


@when("a fresh client starts with only the current access token")
def bootstrap_access_token(context: Context) -> None:
    world = _world(context)
    source = world.client
    world.previous_session = source.auth.get_session()
    assert world.previous_session is not None
    world.bootstrap_cleanup = source.auth.sign_out
    world.cleanup_callbacks.append(world.bootstrap_cleanup)
    world.client = VolcanoClient(
        api_url=world.fixture["api_url"],
        anon_key=world.fixture["anon_key"],
        access_token=world.previous_session.access_token,
    )
    _ = world.record(world.client.auth.get_session)


@then("the token-only session has no cached user")
def token_session_has_no_user(context: Context) -> None:
    session = _world(context).client.current_session
    assert session is not None
    assert session.user_id is None
    assert session.user is None


@when("a fresh client starts with a rejected access token")
def bootstrap_rejected_token(context: Context) -> None:
    world = _world(context)
    world.client = VolcanoClient(
        api_url=world.fixture["api_url"],
        anon_key=world.fixture["anon_key"],
        access_token=REJECTED_BEARER,
    )
    world.previous_session = world.client.current_session
    _ = world.record(world.client.auth.get_session)


@then("the session retains only the supplied access token")
def token_session_retains_access(context: Context) -> None:
    world = _world(context)
    session = world.client.current_session
    assert session is not None
    assert world.previous_session is not None
    assert session.access_token == world.previous_session.access_token
    assert session.refresh_token is None


@then("the refreshed session becomes current")
def refreshed_session_becomes_current(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.previous_session is not None
    refreshed = _value(context, Session)
    assert refreshed is not world.previous_session
    assert refreshed.access_token != world.previous_session.access_token
    assert world.client.auth.get_session() is refreshed


@when("the client signs out")
def sign_out(context: Context) -> None:
    world = _world(context)
    world.signed_out_session = world.client.auth.get_session()
    assert world.signed_out_session is not None
    outcome = world.record(world.client.auth.sign_out)
    if outcome.ok and world.bootstrap_cleanup is not None:
        world.cleanup_callbacks.remove(world.bootstrap_cleanup)
        world.bootstrap_cleanup = None


@then("the current session is empty")
def current_session_is_empty(context: Context) -> None:
    assert _world(context).client.auth.get_session() is None


@when("a fresh client loads a profile with the signed-out access token")
def load_signed_out_profile(context: Context) -> None:
    world = _world(context)
    assert world.signed_out_session is not None
    target = VolcanoClient(
        api_url=world.fixture["api_url"],
        anon_key=world.fixture["anon_key"],
        access_token=world.signed_out_session.access_token,
    )
    _ = world.record(target.auth.get_user)


@when("a fresh client tries to refresh the signed-out session")
def refresh_signed_out_session(context: Context) -> None:
    world = _world(context)
    assert world.signed_out_session is not None
    target = VolcanoClient(
        api_url=world.fixture["api_url"],
        anon_key=world.fixture["anon_key"],
    )
    _ = target.auth.set_session(world.signed_out_session)
    world.client = target
    _ = world.record(target.auth.refresh_session)


@then("the SDK operation fails with an authentication error")
def operation_fails_with_authentication_error(context: Context) -> None:
    outcome = _world(context).last_outcome
    assert outcome is not None
    assert not outcome.ok
    assert outcome.category == "authentication error"


@then("the SDK operation succeeds")
def operation_succeeds(context: Context) -> None:
    outcome = _world(context).last_outcome
    assert outcome is not None
    assert outcome.ok, f"SDK operation failed ({outcome.category}): {outcome.error}"


@then("the SDK operation fails")
def operation_fails(context: Context) -> None:
    outcome = _world(context).last_outcome
    assert outcome is not None
    assert not outcome.ok


@then("the current session belongs to the contract user")
def session_belongs_to_contract_user(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert _value(context, Session).user_id == world.fixture["user_id"]
    assert world.client.current_session is not None
    assert world.client.current_session.user_id == world.fixture["user_id"]


@then("the current session exposes access and refresh tokens")
def session_exposes_tokens(context: Context) -> None:
    world = _world(context)
    session = world.client.current_session
    assert session is not None
    assert session.access_token
    assert session.refresh_token


@then("the auth-state listener observes the signed-in contract user")
def auth_state_listener_observes_signed_in_user(context: Context) -> None:
    world = _world(context)
    assert any(
        event == "SIGNED_IN"
        and session is not None
        and session.user_id == world.fixture["user_id"]
        for event, session in world.auth_state_events
    )


@given("an authenticated client")
def authenticated_client(context: Context) -> None:
    _world(context).authenticate()


@given("the client replaces its access token with a rejected token")
def replace_access_token(context: Context) -> None:
    world = _world(context)
    client = world.client
    session = client.auth.get_session()
    assert session is not None
    header, payload, _signature = session.access_token.split(".")
    world.previous_session = client.auth.set_session(
        Session(
            access_token=f"{header}.{payload}.sdk-contract-rejected-signature",
            refresh_token=session.refresh_token,
            user_id=session.user_id,
        )
    )


@then("the function invocation replaces the rejected token for the same user")
@then("the session list replaces the rejected token for the same user")
@then("the profile read replaces the rejected token for the same user")
@then("the storage operation replaces the rejected token for the same user")
@then("the database read replaces the rejected token for the same user")
def read_replaced_token(context: Context) -> None:
    world = _world(context)
    session = world.client.auth.get_session()
    assert session is not None
    assert session.access_token
    assert world.previous_session is not None
    assert session.access_token != world.previous_session.access_token
    assert session.refresh_token
    assert session.user_id == world.fixture["user_id"]


@when("the client lists its server sessions")
def list_server_sessions(context: Context) -> None:
    world = _world(context)
    _ = world.record(lambda: world.client.auth.list_sessions(page=1, limit=100))


@then("the session list contains the current session for the contract user")
def listed_sessions_belong_to_contract_user(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    page = _value(context, SessionPage)
    assert page.page == 1
    assert page.total >= len(page.sessions) > 0
    assert all(session.user_id == world.fixture["user_id"] for session in page.sessions)
    assert sum(session.is_current for session in page.sessions) == 1


@when("the client loads its server-validated profile")
def load_server_profile(context: Context) -> None:
    world = _world(context)
    _ = world.record(world.client.auth.get_user)


@then("the returned and cached profiles belong to the contract user")
def profiles_belong_to_contract_user(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert _value(context, User).id == world.fixture["user_id"]
    session = world.client.current_session
    assert session is not None
    assert session.user is not None
    assert session.user["id"] == world.fixture["user_id"]


@when("one client pauses delivery for 1 second and then resumes with the same handler")
def pause_and_resume(context: Context) -> None:
    world = _world(context)
    if world.last_outcome is not None and not world.last_outcome.ok:
        return
    _ = world.record(lambda: world.run(verify_broadcast_pause(world)))


@when('the client selects the contract table where "slug" equals the fixture slug')
def select_fixture_row(context: Context) -> None:
    world = _world(context)
    _ = world.record(
        lambda: (
            world.client.database(world.fixture["database_name"])
            .from_(world.fixture["table_name"])
            .select("*")
            .eq("slug", world.fixture["fixture_row"]["slug"])
            .execute()
        )
    )


@then("exactly the fixture row is returned")
def fixture_row_returned(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value == [world.fixture["fixture_row"]]


@when("the client selects a projected page of query fixture members")
def select_projected_query_page(context: Context) -> None:
    world = _world(context)
    _ = world.record(
        lambda: (
            world.client.database(world.fixture["database_name"])
            .from_(world.fixture["query_table_name"])
            .select("slug", "rank")
            .in_("slug", ["alpha", "beta", "gamma", "delta"])
            .order("enabled")
            .order("rank", ascending=False)
            .offset(1)
            .limit(2)
            .execute()
        )
    )


@then("the projected page contains only beta and gamma in that order")
def projected_query_page_returned(context: Context) -> None:
    assert _outcome(context).value == [
        {"slug": "beta", "rank": 20},
        {"slug": "gamma", "rank": 30},
    ]


def _query_filters(
    world: ContractWorld, filters: list[tuple[str, str, object]]
) -> None:
    def operation() -> dict[str, list[dict[str, object]]]:
        table = world.client.database(world.fixture["database_name"]).from_(
            world.fixture["query_table_name"]
        )
        results: dict[str, list[dict[str, object]]] = {}
        for operator, column, value in filters:
            query = table.select("slug")
            value_filters: dict[str, Callable[[str, object], QueryBuilder]] = {
                "neq": query.neq,
                "gt": query.gt,
                "gte": query.gte,
                "lt": query.lt,
                "lte": query.lte,
                "is_": query.is_,
            }
            if operator in value_filters:
                filtered = value_filters[operator](column, value)
            else:
                assert isinstance(value, str)
                pattern_filters: dict[str, Callable[[str, str], QueryBuilder]] = {
                    "like": query.like,
                    "ilike": query.ilike,
                }
                filtered = pattern_filters[operator](column, value)
            results[f"{operator}:{value}"] = filtered.order("rank").execute()
        return results

    _ = world.record(operation)


@when("the client selects query fixture rows with each comparison filter")
def select_query_comparisons(context: Context) -> None:
    _query_filters(
        _world(context),
        [
            (op, "rank", value)
            for op, value in [
                ("neq", 20),
                ("gt", 20),
                ("gte", 20),
                ("lt", 30),
                ("lte", 30),
            ]
        ],
    )


@then("each comparison returns exactly the matching query fixture rows")
def comparison_query_rows_returned(context: Context) -> None:
    expected = {
        "neq:20": ["alpha", "gamma", "delta", "epsilon"],
        "gt:20": ["gamma", "delta", "epsilon"],
        "gte:20": ["beta", "gamma", "delta", "epsilon"],
        "lt:30": ["alpha", "beta"],
        "lte:30": ["alpha", "beta", "gamma"],
    }
    assert _outcome(context).value == {
        key: [{"slug": slug} for slug in slugs] for key, slugs in expected.items()
    }


@when(
    "the client selects query fixture rows with case-sensitive and insensitive patterns"
)
def select_query_patterns(context: Context) -> None:
    _query_filters(
        _world(context), [("like", "label", "Case_%"), ("ilike", "label", "case_%")]
    )


@then("each pattern returns exactly the matching query fixture rows")
def pattern_query_rows_returned(context: Context) -> None:
    assert _outcome(context).value == {
        "like:Case_%": [{"slug": "alpha"}, {"slug": "epsilon"}],
        "ilike:case_%": [{"slug": "alpha"}, {"slug": "beta"}, {"slug": "epsilon"}],
    }


@when("the client selects query fixture rows with null and boolean filters")
def select_query_identities(context: Context) -> None:
    _query_filters(
        _world(context),
        [("is_", "label", None), ("is_", "enabled", True), ("is_", "enabled", False)],
    )


@then("each identity filter returns exactly the matching query fixture rows")
def identity_query_rows_returned(context: Context) -> None:
    assert _outcome(context).value == {
        "is_:None": [{"slug": "gamma"}],
        "is_:True": [{"slug": "alpha"}, {"slug": "gamma"}, {"slug": "epsilon"}],
        "is_:False": [{"slug": "beta"}, {"slug": "delta"}],
    }


@when("the client inserts its contract row")
def insert_contract_row(context: Context) -> None:
    world = _world(context)
    row = world.fixture["mutation_rows"]["insert"]
    table = world.client.database(world.fixture["database_name"]).from_(
        world.fixture["table_name"]
    )

    def operation() -> list[dict[str, object]]:
        def cleanup() -> None:
            _ = table.delete().eq("slug", row["slug"]).execute()

        world.cleanup_callbacks.append(cleanup)
        return table.insert(row).execute()

    _ = world.record(operation)


@then("exactly the inserted contract row is returned")
def inserted_contract_row_returned(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    expected = world.fixture["mutation_rows"]["insert"]
    assert world.last_outcome.value == [expected]


@when("the client updates its contract row")
def update_contract_row(context: Context) -> None:
    world = _world(context)
    row = world.fixture["mutation_rows"]["update"]
    table = world.client.database(world.fixture["database_name"]).from_(
        world.fixture["table_name"]
    )

    def operation() -> list[dict[str, object]]:
        def cleanup() -> None:
            _ = (
                table.update({"value": row["before"]["value"]})
                .eq("slug", row["before"]["slug"])
                .execute()
            )

        world.cleanup_callbacks.append(cleanup)
        return (
            table.update({"value": row["after"]["value"]})
            .eq("slug", row["before"]["slug"])
            .execute()
        )

    _ = world.record(operation)


@then("exactly the updated contract row is returned")
def updated_contract_row_returned(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    expected = world.fixture["mutation_rows"]["update"]["after"]
    assert world.last_outcome.value == [expected]


@when("the client deletes its contract row")
def delete_contract_row(context: Context) -> None:
    world = _world(context)
    row = world.fixture["mutation_rows"]["delete"]
    table = world.client.database(world.fixture["database_name"]).from_(
        world.fixture["table_name"]
    )

    def operation() -> list[dict[str, object]]:
        def cleanup() -> None:
            _ = table.delete().eq("slug", row["slug"]).execute()
            _ = table.insert(row).execute()

        world.cleanup_callbacks.append(cleanup)
        return table.delete().eq("slug", row["slug"]).execute()

    _ = world.record(operation)


@then("exactly the deleted contract row is returned")
def deleted_contract_row_returned(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    expected = world.fixture["mutation_rows"]["delete"]
    assert world.last_outcome.value == [expected]


@when("the client updates a missing contract row")
def update_missing_contract_row(context: Context) -> None:
    world = _world(context)
    table = world.client.database(world.fixture["database_name"]).from_(
        world.fixture["table_name"]
    )
    missing_slug = f"{world.fixture['fixture_row']['slug']}-missing"
    _ = world.record(
        lambda: (
            table.update({"value": "must-not-be-written"})
            .eq("slug", missing_slug)
            .execute()
        )
    )


@when("the client deletes a missing contract row")
def delete_missing_contract_row(context: Context) -> None:
    world = _world(context)
    table = world.client.database(world.fixture["database_name"]).from_(
        world.fixture["table_name"]
    )
    missing_slug = f"{world.fixture['fixture_row']['slug']}-missing"
    _ = world.record(lambda: table.delete().eq("slug", missing_slug).execute())


@then("the mutation returns an empty row list")
def mutation_returns_empty_list(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value == []


@then("the existing contract row is unchanged")
def existing_contract_row_unchanged(context: Context) -> None:
    world = _world(context)
    row = world.fixture["fixture_row"]
    result = (
        world.client.database(world.fixture["database_name"])
        .from_(world.fixture["table_name"])
        .select("*")
        .eq("slug", row["slug"])
        .execute()
    )
    assert result == [row]


@when("the client uploads and downloads the contract object")
def upload_and_download(context: Context) -> None:
    world = _world(context)

    def operation() -> StorageDownloadResult:
        bucket = world.client.storage.from_(world.fixture["bucket_name"])
        uploaded = bucket.upload(world.storage_path, world.storage_bytes)
        return {
            "bytes": bucket.download(world.storage_path),
            "path": uploaded_text_field(uploaded, "name"),
        }

    _ = world.record(operation)


@then("the downloaded bytes equal the uploaded bytes")
def downloaded_bytes_match(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert _value_dict(context)["bytes"] == world.storage_bytes


@when(
    "the client uploads the contract object as text/plain and reads its stored metadata"
)
def upload_and_read_metadata(context: Context) -> None:
    world = _world(context)

    def operation() -> StorageMetadataResult:
        bucket = world.client.storage.from_(world.fixture["bucket_name"])
        uploaded = bucket.upload(
            world.storage_path, world.storage_bytes, content_type="text/plain"
        )

        def remove_object() -> None:
            _ = bucket.remove(world.storage_path)

        world.cleanup_callbacks.append(remove_object)
        listed = bucket.list(world.storage_path)
        return {
            "path": uploaded_text_field(uploaded, "name"),
            "bytes": bucket.download(world.storage_path),
            "content_type": uploaded_text_field(uploaded, "mime_type"),
            "listed": [
                {"name": item.name, "mime_type": item.mime_type}
                for item in listed.objects
            ],
        }

    _ = world.record(operation)


@then("the uploaded and listed object content types are text/plain")
def stored_content_types_match(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    value = _value_dict(context)
    assert value["content_type"] == "text/plain"
    assert value["listed"] == [{"name": world.storage_path, "mime_type": "text/plain"}]


@when("the client uploads the contract object and downloads bytes 2 through 7")
def upload_and_download_range(context: Context) -> None:
    world = _world(context)

    def operation() -> StorageDownloadResult:
        bucket = world.client.storage.from_(world.fixture["bucket_name"])
        uploaded = bucket.upload(world.storage_path, world.storage_bytes)

        def remove_object() -> None:
            _ = bucket.remove(world.storage_path)

        world.cleanup_callbacks.append(remove_object)
        return {
            "bytes": bucket.download(world.storage_path, byte_range="bytes=2-7"),
            "path": uploaded_text_field(uploaded, "name"),
        }

    _ = world.record(operation)


@then("the downloaded bytes equal uploaded bytes 2 through 7 inclusive")
def downloaded_range_matches(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert _value_dict(context)["bytes"] == world.storage_bytes[2:8]


@when("the client copies, moves, and removes a copy of the contract object")
def copy_move_and_remove(context: Context) -> None:
    world = _world(context)
    bucket = world.client.storage.from_(world.fixture["bucket_name"])
    source = world.storage_path
    copied = f"{source}.copy"
    moved = f"{source}.moved"

    for path in (source, copied, moved):

        def cleanup(object_path: str = path) -> None:
            if any(
                item.name == object_path for item in bucket.list(object_path).objects
            ):
                _ = bucket.remove(object_path)

        world.cleanup_callbacks.append(cleanup)

    def operation() -> StorageLifecycleResult:
        _ = bucket.upload(source, world.storage_bytes)
        _ = bucket.copy(source, copied)
        original_bytes = bucket.download(source)
        copied_bytes = bucket.download(copied)
        _ = bucket.move(copied, moved)
        moved_bytes = bucket.download(moved)
        after_move = sorted(item.name for item in bucket.list(source).objects)
        _ = bucket.remove(moved)
        after_remove = sorted(item.name for item in bucket.list(source).objects)
        remaining_bytes = bucket.download(source)
        return {
            "bytes": [original_bytes, copied_bytes, moved_bytes, remaining_bytes],
            "after_move": after_move,
            "after_remove": after_remove,
        }

    _ = world.record(operation)


@then("the original, copied, and moved bytes equal the uploaded bytes")
def lifecycle_bytes_match(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    values = _object_list(_value_dict(context)["bytes"])
    assert all(
        isinstance(value, bytes) and value == world.storage_bytes for value in values
    )


@then("moving the copy leaves only the original and moved paths")
def moved_paths_match(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert _value_dict(context)["after_move"] == sorted(
        [world.storage_path, f"{world.storage_path}.moved"]
    )


@then("removing the moved object leaves the original unchanged")
def removed_path_is_absent(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    value = _value_dict(context)
    assert value["after_remove"] == [world.storage_path]
    values = _object_list(value["bytes"])
    assert len(values) == STORAGE_LIFECYCLE_DOWNLOAD_COUNT
    assert values[3] == world.storage_bytes


def _storage_bucket(world: ContractWorld) -> StorageBucket:
    return world.client.storage.from_(world.fixture["bucket_name"])


def _clean_storage_object(world: ContractWorld) -> None:
    bucket = _storage_bucket(world)
    if any(
        item.name == world.storage_path
        for item in bucket.list(world.storage_path).objects
    ):
        _ = bucket.remove(world.storage_path)


def _partial_upload(world: ContractWorld) -> PartialUpload:
    bucket = _storage_bucket(world)
    body = b"x" * (5 * 1024 * 1024) + world.storage_bytes
    session = bucket.create_upload_session(
        world.storage_path,
        total_size=len(body),
        part_size=5 * 1024 * 1024,
        content_type="application/octet-stream",
    )

    def abort() -> None:
        with suppress(NotFoundError):
            bucket.abort_upload_session(
                world.storage_path, session_id=session.session_id
            )

    world.cleanup_callbacks.append(abort)
    world.cleanup_callbacks.append(lambda: _clean_storage_object(world))
    part = bucket.upload_part(
        world.storage_path,
        session_id=session.session_id,
        part_number=1,
        data=body[: session.part_size],
    )
    return {"session": session, "part": part, "bytes": body}


@when("the client uploads one part and resumes the contract upload")
def resume_contract_upload(context: Context) -> None:
    world = _world(context)

    def operation() -> ResumedUpload:
        value = _partial_upload(world)
        bucket = _storage_bucket(world)
        session = value["session"]
        progress = bucket.get_upload_session(
            world.storage_path, session_id=session.session_id
        )
        _ = bucket.upload_part(
            world.storage_path,
            session_id=session.session_id,
            part_number=2,
            data=value["bytes"][session.part_size :],
        )
        stored_object = bucket.complete_upload_session(
            world.storage_path, session_id=session.session_id
        )
        download = bucket.download(world.storage_path)
        return {
            **value,
            "progress": progress,
            "object": stored_object,
            "download": download,
        }

    _ = world.record(operation)


@then("upload progress describes exactly the first uploaded part")
def partial_upload_progress(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    value = _value_dict(context)
    progress, session, part = value["progress"], value["session"], value["part"]
    assert isinstance(progress, UploadSessionStatus)
    assert isinstance(session, UploadSession)
    assert isinstance(part, UploadPart)
    upload_bytes = value["bytes"]
    assert isinstance(upload_bytes, bytes)
    assert progress.session_id == session.session_id
    assert progress.path == world.storage_path
    assert progress.content_type == "application/octet-stream"
    assert progress.status == "uploading"
    assert progress.total_size == len(upload_bytes)
    assert progress.part_size == session.part_size == 5 * 1024 * 1024
    assert progress.total_parts == session.total_parts == MULTIPART_PART_COUNT
    assert progress.parts_uploaded == 1
    assert progress.bytes_uploaded == part.size == session.part_size
    assert part.part_number == 1
    assert part.etag
    assert progress.parts == (part,)


@then("the completed multipart object preserves its path, type, and bytes")
def completed_upload_matches(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    value = _value_dict(context)
    stored = value["object"]
    upload_bytes = value["bytes"]
    assert isinstance(stored, StorageObject)
    assert isinstance(upload_bytes, bytes)
    assert stored.name == world.storage_path
    assert stored.mime_type == "application/octet-stream"
    assert stored.size == len(upload_bytes)
    assert value["download"] == upload_bytes


@when("the client uploads one part and aborts the contract upload")
def abort_contract_upload(context: Context) -> None:
    world = _world(context)

    def operation() -> dict[str, str]:
        value = _partial_upload(world)
        bucket = _storage_bucket(world)
        session_id = value["session"].session_id
        bucket.abort_upload_session(world.storage_path, session_id=session_id)
        outcomes: dict[str, str] = {}
        reads: dict[str, Callable[[], object]] = {
            "session": lambda: bucket.get_upload_session(
                world.storage_path, session_id=session_id
            ),
            "object": lambda: bucket.download(world.storage_path),
        }
        for name, read in reads.items():
            try:
                _ = read()
            except NotFoundError:
                outcomes[name] = "not found"
            else:
                outcomes[name] = "unexpected success"
        return outcomes

    _ = world.record(operation)


@then("the aborted session and unfinished object are not found")
def aborted_upload_is_gone(context: Context) -> None:
    assert _outcome(context).value == {
        "session": "not found",
        "object": "not found",
    }


@when("the client makes the contract object public and private again")
def change_contract_visibility(context: Context) -> None:
    world = _world(context)

    def operation() -> StorageVisibilityResult:
        bucket = _storage_bucket(world)
        world.cleanup_callbacks.append(lambda: _clean_storage_object(world))
        _ = bucket.upload(world.storage_path, world.storage_bytes)
        url = bucket.get_public_url(world.storage_path)
        before = httpx.get(url, timeout=10)
        public = bucket.update_visibility(world.storage_path, is_public=True)
        visible = httpx.get(url, timeout=10)
        private = bucket.update_visibility(world.storage_path, is_public=False)
        after = httpx.get(url, timeout=10)
        return {
            "statuses": [before.status_code, visible.status_code, after.status_code],
            "bytes": visible.content,
            "visibility": [public.is_public, private.is_public],
            "private_bytes": [before.content, after.content],
        }

    _ = world.record(operation)


@then("anonymous reads return the original bytes only while the object is public")
def anonymous_visibility_matches(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    value = _value_dict(context)
    private_bytes = _object_list(value["private_bytes"])
    assert all(
        isinstance(body, bytes) and world.storage_bytes not in body
        for body in private_bytes
    )
    assert {key: value[key] for key in ("statuses", "bytes", "visibility")} == {
        "statuses": [404, 200, 404],
        "bytes": world.storage_bytes,
        "visibility": [True, False],
    }


@then("the stored object path equals the contract path")
def stored_object_path_matches(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert _value_dict(context)["path"] == world.storage_path


@given("a service-role client")
def service_role_client(context: Context) -> None:
    assert _world(context).fixture["service_key"]


@when("the client acquires and releases the contract lock")
def acquire_and_release_lock(context: Context) -> None:
    world = _world(context)

    def operation() -> LockReleaseResult:
        lease = world.service_client.locks.acquire(world.lock_key, ttl=10)
        cleanup = world.register_lock_cleanup(world.lock_key, lease)
        world.service_client.locks.release(world.lock_key, lease)
        world.cleanup_callbacks.remove(cleanup)

        replacement = world.service_client.locks.acquire(world.lock_key, ttl=10)
        replacement_cleanup = world.register_lock_cleanup(world.lock_key, replacement)
        world.service_client.locks.release(world.lock_key, replacement)
        world.cleanup_callbacks.remove(replacement_cleanup)
        return {"lease": lease, "released": replacement.token != lease.token}

    _ = world.record(operation)


@then("the released lease is no longer held")
def released_lease_not_held(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert _value_dict(context)["released"] is True


@given("a project-owner client")
def project_owner_client(context: Context) -> None:
    assert _world(context).fixture["platform_token"]


@when("the client starts the contract durable function")
def start_durable_execution(context: Context) -> None:
    world = _world(context)
    _ = world.record(world.start_durable_execution)


@when("the client starts the contract durable function twice under one execution name")
def start_durable_execution_twice(context: Context) -> None:
    world = _world(context)

    def operation() -> tuple[DurableExecution, DurableExecution]:
        return world.start_durable_execution(), world.start_durable_execution()

    _ = world.record(operation)


@when("the client recovers the contract lock with caller-owned tokens")
def recover_lock(context: Context) -> None:
    world = _world(context)

    def operation() -> LockRecoveryResult:
        locks, key = world.service_client.locks, world.lock_key
        token, request_id = str(uuid4()), str(uuid4())
        lease = locks.acquire(key, ttl=30, token=token, request_id=request_id)
        cleanup = world.register_lock_cleanup(key, lease)
        recovered = locks.acquire(key, ttl=30, token=token, request_id=request_id)
        held = locks.get(key, request_id=str(uuid4()))
        renewed = locks.renew(key, recovered, ttl=60, request_id=str(uuid4()))
        locks.release(key, renewed, request_id=str(uuid4()))
        available = locks.get(key, request_id=str(uuid4()))
        return {
            "token": token,
            "cleanup": cleanup,
            "lease": lease,
            "recovered": recovered,
            "held": held,
            "renewed": renewed,
            "available": available,
        }

    _ = world.record(operation)


@then("the started execution carries its id, function, name, region, and creation time")
def started_execution_is_addressable(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    execution = _value(context, DurableExecution)
    assert execution.id
    assert execution.function_id
    assert execution.name == world.durable_execution_name
    assert execution.region
    assert isinstance(execution.created_at, datetime)


@then("the started execution is not terminal and carries no result")
def started_execution_is_a_handle(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    execution = _value(context, DurableExecution)
    assert execution.is_terminal is False
    assert execution.result is None


@then("both starts return the same execution")
def both_starts_return_one_execution(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    raw_executions = _outcome(context).value
    assert isinstance(raw_executions, tuple)
    executions = cast("tuple[object, ...]", raw_executions)
    assert len(executions) == DURABLE_START_COUNT
    first, second = executions
    assert isinstance(first, DurableExecution)
    assert isinstance(second, DurableExecution)
    assert second.id == first.id
    assert second.name == first.name


@when("the owner reads the execution until it is terminal")
def read_execution_until_terminal(context: Context) -> None:
    world = _world(context)
    if world.last_outcome is not None and not world.last_outcome.ok:
        return
    assert world.started_execution is not None
    execution_id = world.started_execution.id
    _ = world.record(lambda: world.follow_durable_execution(execution_id))


@then("the execution succeeded carrying the function's result")
def execution_succeeded_with_result(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    execution = _value(context, DurableExecution)
    assert execution.status == "succeeded"
    assert execution.result == {"echoed": world.durable_payload["value"]}


@when("the owner lists the durable function's executions")
def list_durable_executions(context: Context) -> None:
    world = _world(context)
    if world.last_outcome is not None and not world.last_outcome.ok:
        return
    _ = world.record(world.list_durable_executions)


@then("the listed executions include the started execution")
def listed_executions_include_the_started_one(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.started_execution is not None
    page = _value(context, DurableExecutionPage)
    listed = {execution.id for execution in page.executions}
    assert world.started_execution.id in listed


@then("recovery and renewal preserve the held lease until release")
def recovered_lock_lifecycle(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    value = _value_dict(context)
    held = value["held"]
    available = value["available"]
    cleanup = value["cleanup"]
    token = value["token"]
    lease = value["lease"]
    recovered = value["recovered"]
    renewed = value["renewed"]
    assert isinstance(held, LockState)
    assert isinstance(available, LockState)
    assert callable(cleanup)
    assert isinstance(token, str)
    assert isinstance(lease, LockLease)
    assert isinstance(recovered, LockLease)
    assert isinstance(renewed, LockLease)
    assert held.held is True
    assert available.held is False
    _remove_cleanup(world, cleanup)
    assert token == lease.token == recovered.token == renewed.token
    assert lease.fencing_token is not None
    assert (
        lease.fencing_token
        == recovered.fencing_token
        == held.fencing_token
        == renewed.fencing_token
    )


@when("the client acquires and force releases the contract lock")
def force_release_lock(context: Context) -> None:
    world = _world(context)

    def operation() -> object:
        locks, key = world.service_client.locks, world.lock_key
        lease = locks.acquire(key, ttl=30)
        cleanup = world.register_lock_cleanup(key, lease)
        locks.force_release(key, request_id=str(uuid4()))
        return {"lease": lease, "cleanup": cleanup, "available": locks.get(key)}

    _ = world.record(operation)


@then("the force-released lock is available")
def force_released_lock_available(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    value = _value_dict(context)
    available = value["available"]
    cleanup = value["cleanup"]
    assert isinstance(available, LockState)
    assert callable(cleanup)
    assert available.held is False
    _remove_cleanup(world, cleanup)


@when("the client reacquires the force-released contract lock")
def reacquire_force_released_lock(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    original = _value_dict(context)["lease"]
    assert isinstance(original, LockLease)

    def operation() -> object:
        replacement = world.service_client.locks.acquire(world.lock_key, ttl=30)
        _ = world.register_lock_cleanup(world.lock_key, replacement)
        return {"original": original, "replacement": replacement}

    _ = world.record(operation)


@then("the replacement owner receives a higher fencing token")
def replacement_lock_fence_increases(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    value = _value_dict(context)
    original = value["original"]
    replacement = value["replacement"]
    assert isinstance(original, LockLease)
    assert isinstance(replacement, LockLease)
    assert replacement.token != original.token
    assert original.fencing_token is not None
    assert replacement.fencing_token is not None
    assert replacement.fencing_token > original.fencing_token


@given("two authenticated realtime clients")
def two_realtime_clients(context: Context) -> None:
    world = _world(context)
    try:
        subscriber, publisher = _realtime_pair(world)
        world.run(_subscribe_pair(subscriber, publisher))
    except CONTRACT_EXCEPTIONS as error:
        world.last_outcome = Outcome(
            ok=False,
            category=classify_error(error),
            error=error,
        )


def _realtime_pair(world: ContractWorld) -> tuple[Channel, Channel]:
    clients = [
        world.client,
        type(world.client)(
            api_url=world.fixture["api_url"],
            anon_key=world.fixture["anon_key"],
        ),
    ]
    for client in clients:
        _ = client.auth.sign_in(
            email=world.fixture["user_email"],
            password=world.fixture["user_password"],
        )
    world.realtime_clients = clients
    subscriber = clients[0].realtime.channel(world.realtime_channel)
    publisher = clients[1].realtime.channel(world.realtime_channel)
    world.subscriber = subscriber
    world.publisher = publisher
    return subscriber, publisher


async def _subscribe_pair(subscriber: Channel, publisher: Channel) -> None:
    _ = await asyncio.gather(subscriber.subscribe(), publisher.subscribe())


async def publish_contract_message(world: ContractWorld) -> object:
    assert world.subscriber is not None
    assert world.publisher is not None
    received: asyncio.Future[object] = world.loop.create_future()

    def on_message(message: object) -> None:
        if not received.done():
            received.set_result(message)

    _ = world.subscriber.on("message", on_message)
    await world.publisher.send(world.realtime_message)
    return await asyncio.wait_for(received, timeout=10)


@when("one client subscribes and the other publishes the contract message")
def subscribe_and_publish(context: Context) -> None:
    world = _world(context)
    if world.last_outcome is not None and not world.last_outcome.ok:
        return

    try:
        world.last_outcome = Outcome(
            ok=True, value=world.run(publish_contract_message(world))
        )
    except CONTRACT_EXCEPTIONS as error:
        world.last_outcome = Outcome(
            ok=False,
            category=classify_error(error),
            error=error,
        )


@then("the subscriber receives the contract message within 10 seconds")
def subscriber_received_message(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value == world.realtime_message


@when("the authenticated client invokes the contract function by name")
def invoke_authenticated_contract_function(context: Context) -> None:
    world = _world(context)
    _ = world.record(
        lambda: world.client.functions.invoke(
            world.fixture["function_name"], {"value": "contract"}
        )
    )


@when("the client invokes the contract function by name")
def invoke_contract_function(context: Context) -> None:
    world = _world(context)

    def operation() -> FunctionResponse:
        return world.service_client.functions.invoke(
            world.fixture["function_name"], {"value": "contract"}
        )

    _ = world.record(operation)


@then("the function echoes the payload")
def function_echoed_payload(context: Context) -> None:
    # The function is reachable only at the endpoint the platform resolved, on a
    # domain the API URL does not name, so an echo coming back is what proves
    # the SDK sent the request there rather than somewhere it guessed.
    world = _world(context)
    assert world.last_outcome is not None
    response = _value(context, FunctionResponse)
    assert response.status == HTTP_OK, response
    assert response.data == {"echoed": "contract"}, response.data


@given("a read-only project logs client")
def project_logs_client(context: Context) -> None:
    context.logs_contract = LogContract(_world(context))


@when("the contract function emits three unique structured log events")
def emit_three_logs(context: Context) -> None:
    _logs_contract(context).emit(3)


@when("the contract function emits one unique structured log event")
def emit_one_log(context: Context) -> None:
    _logs_contract(context).emit(1)


@when("the client searches and paginates those events within 240 seconds")
def search_contract_logs(context: Context) -> None:
    _ = _world(context).record(_logs_contract(context).search)


@when("the client reads matching log activity within 120 seconds")
def read_contract_log_activity(context: Context) -> None:
    _ = _world(context).record(_logs_contract(context).activity)


@then("all three structured events retain their metadata without duplicates")
def verify_contract_logs(context: Context) -> None:
    _logs_contract(context).verify_events(_log_events(_outcome(context).value))


@then("activity counts exactly that event in its function and level buckets")
def verify_contract_log_activity(context: Context) -> None:
    _logs_contract(context).verify_activity(_value(context, LogActivityResponse))


@when("one presence client joins and leaves while the other remains subscribed")
def observe_presence_membership(context: Context) -> None:
    world = _world(context)
    if world.last_outcome is not None and not world.last_outcome.ok:
        return
    _ = world.record(lambda: world.run(verify_presence_membership(world)))


@then(f"both rosters identify the contract user {PRESENCE_ROSTERS_SUFFIX}")
def verify_presence_rosters(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value == [1, 2, 1]


@when("the clients observe an inserted and updated contract row")
def observe_postgres_changes(context: Context) -> None:
    world = _world(context)
    if world.last_outcome is not None and not world.last_outcome.ok:
        return
    _ = world.record(lambda: world.run(verify_postgres_changes(world)))


@then("automatic and lightweight notifications retain metadata and row identity")
def verify_postgres_rows(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value == ["INSERT", "UPDATE"]
