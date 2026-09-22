from __future__ import annotations

import asyncio
import time
from contextlib import suppress
from dataclasses import replace
from typing import TYPE_CHECKING, Any
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

from volcano_sdk import NotFoundError, Session, VolcanoClient

if TYPE_CHECKING:
    from collections.abc import Callable

    from behave.runner import Context

    from volcano_sdk.storage import StorageBucket

ACCESS_TOKEN_CLOCK_TICK_SECONDS = 1.1
HTTP_OK = 200
MULTIPART_PART_COUNT = 2
REJECTED_BEARER = "sdk-contract-rejected-access-token"


def _world(context: Context) -> ContractWorld:
    world = context.contract
    assert isinstance(world, ContractWorld)
    return world


def _outcome(context: Context) -> Outcome:
    outcome = _world(context).last_outcome
    assert outcome is not None
    return outcome


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
    world.record(
        lambda: world.client.auth.sign_in(
            email=world.fixture["user_email"],
            password=world.fixture["user_password"],
        )
    )


@when("the client reads the current session")
def read_current_session(context: Context) -> None:
    world = _world(context)
    world.record(world.client.auth.get_session)


@when("a fresh client adopts the current session")
def adopt_current_session(context: Context) -> None:
    world = _world(context)
    source = world.client.auth.get_session()
    assert source is not None
    target = VolcanoClient(
        api_url=world.fixture["api_url"],
        anon_key=world.fixture["anon_key"],
    )
    world.record(lambda: target.auth.set_session(source))
    world.client = target


@when("the client refreshes the current session")
def refresh_current_session(context: Context) -> None:
    world = _world(context)
    world.previous_session = world.client.auth.get_session()
    assert world.previous_session is not None
    time.sleep(ACCESS_TOKEN_CLOCK_TICK_SECONDS)
    world.record(world.client.auth.refresh_session)


@when("a fresh client tries to refresh a supplied profile without a session identifier")
def refresh_supplied_profile_without_sid(context: Context) -> None:
    world = _world(context)
    source = world.client.auth.get_session()
    assert source is not None
    target = VolcanoClient(
        api_url=world.fixture["api_url"], anon_key=world.fixture["anon_key"]
    )
    supplied = target.auth.set_session(replace(source, access_token=REJECTED_BEARER))
    world.record(target.auth.refresh_session)
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
    world.record(world.client.auth.get_session)


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
    world.record(world.client.auth.get_session)


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
    assert world.last_outcome.value is not world.previous_session
    assert world.last_outcome.value.access_token != world.previous_session.access_token
    assert world.client.auth.get_session() is world.last_outcome.value


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
    world.record(target.auth.get_user)


@when("a fresh client tries to refresh the signed-out session")
def refresh_signed_out_session(context: Context) -> None:
    world = _world(context)
    assert world.signed_out_session is not None
    target = VolcanoClient(
        api_url=world.fixture["api_url"],
        anon_key=world.fixture["anon_key"],
    )
    target.auth.set_session(world.signed_out_session)
    world.client = target
    world.record(target.auth.refresh_session)


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
    assert world.last_outcome.value.user_id == world.fixture["user_id"]
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
    world.record(lambda: world.client.auth.list_sessions(page=1, limit=100))


@then("the session list contains the current session for the contract user")
def listed_sessions_belong_to_contract_user(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    page = world.last_outcome.value
    assert page.page == 1
    assert page.total >= len(page.sessions) > 0
    assert all(session.user_id == world.fixture["user_id"] for session in page.sessions)
    assert sum(session.is_current for session in page.sessions) == 1


@when("the client loads its server-validated profile")
def load_server_profile(context: Context) -> None:
    world = _world(context)
    world.record(world.client.auth.get_user)


@then("the returned and cached profiles belong to the contract user")
def profiles_belong_to_contract_user(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value.id == world.fixture["user_id"]
    session = world.client.current_session
    assert session is not None
    assert session.user is not None
    assert session.user["id"] == world.fixture["user_id"]


@when("one client pauses delivery for 1 second and then resumes with the same handler")
def pause_and_resume(context: Context) -> None:
    world = _world(context)
    if world.last_outcome is not None and not world.last_outcome.ok:
        return
    world.record(lambda: world.run(verify_broadcast_pause(world)))


@when('the client selects the contract table where "slug" equals the fixture slug')
def select_fixture_row(context: Context) -> None:
    world = _world(context)
    world.record(
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
    world.record(
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


def _query_filters(world: ContractWorld, filters: list[tuple[str, str, Any]]) -> None:
    def operation() -> dict[str, list[dict[str, Any]]]:
        table = world.client.database(world.fixture["database_name"]).from_(
            world.fixture["query_table_name"]
        )
        return {
            f"{operator}:{value}": getattr(table.select("slug"), operator)(
                column, value
            )
            .order("rank")
            .execute()
            for operator, column, value in filters
        }

    world.record(operation)


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

    def operation() -> list[dict[str, Any]]:
        def cleanup() -> None:
            table.delete().eq("slug", row["slug"]).execute()

        world.cleanup_callbacks.append(cleanup)
        return table.insert(row).execute()

    world.record(operation)


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

    def operation() -> list[dict[str, Any]]:
        def cleanup() -> None:
            (
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

    world.record(operation)


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

    def operation() -> list[dict[str, Any]]:
        def cleanup() -> None:
            table.delete().eq("slug", row["slug"]).execute()
            table.insert(row).execute()

        world.cleanup_callbacks.append(cleanup)
        return table.delete().eq("slug", row["slug"]).execute()

    world.record(operation)


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
    world.record(
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
    world.record(lambda: table.delete().eq("slug", missing_slug).execute())


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

    def operation() -> dict[str, Any]:
        bucket = world.client.storage.from_(world.fixture["bucket_name"])
        uploaded = bucket.upload(world.storage_path, world.storage_bytes)
        return {
            "bytes": bucket.download(world.storage_path),
            "path": uploaded["name"],
        }

    world.record(operation)


@then("the downloaded bytes equal the uploaded bytes")
def downloaded_bytes_match(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value["bytes"] == world.storage_bytes


@when(
    "the client uploads the contract object as text/plain and reads its stored metadata"
)
def upload_and_read_metadata(context: Context) -> None:
    world = _world(context)

    def operation() -> dict[str, Any]:
        bucket = world.client.storage.from_(world.fixture["bucket_name"])
        uploaded = bucket.upload(
            world.storage_path, world.storage_bytes, content_type="text/plain"
        )

        def remove_object() -> None:
            bucket.remove(world.storage_path)

        world.cleanup_callbacks.append(remove_object)
        listed = bucket.list(world.storage_path)
        return {
            "path": uploaded["name"],
            "bytes": bucket.download(world.storage_path),
            "content_type": uploaded["mime_type"],
            "listed": [
                {"name": item.name, "mime_type": item.mime_type}
                for item in listed.objects
            ],
        }

    world.record(operation)


@then("the uploaded and listed object content types are text/plain")
def stored_content_types_match(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value["content_type"] == "text/plain"
    assert world.last_outcome.value["listed"] == [
        {"name": world.storage_path, "mime_type": "text/plain"}
    ]


@when("the client uploads the contract object and downloads bytes 2 through 7")
def upload_and_download_range(context: Context) -> None:
    world = _world(context)

    def operation() -> dict[str, Any]:
        bucket = world.client.storage.from_(world.fixture["bucket_name"])
        uploaded = bucket.upload(world.storage_path, world.storage_bytes)

        def remove_object() -> None:
            bucket.remove(world.storage_path)

        world.cleanup_callbacks.append(remove_object)
        return {
            "bytes": bucket.download(world.storage_path, byte_range="bytes=2-7"),
            "path": uploaded["name"],
        }

    world.record(operation)


@then("the downloaded bytes equal uploaded bytes 2 through 7 inclusive")
def downloaded_range_matches(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value["bytes"] == world.storage_bytes[2:8]


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
                bucket.remove(object_path)

        world.cleanup_callbacks.append(cleanup)

    def operation() -> dict[str, Any]:
        bucket.upload(source, world.storage_bytes)
        bucket.copy(source, copied)
        original_bytes = bucket.download(source)
        copied_bytes = bucket.download(copied)
        bucket.move(copied, moved)
        moved_bytes = bucket.download(moved)
        after_move = sorted(item.name for item in bucket.list(source).objects)
        bucket.remove(moved)
        after_remove = sorted(item.name for item in bucket.list(source).objects)
        remaining_bytes = bucket.download(source)
        return {
            "bytes": [original_bytes, copied_bytes, moved_bytes, remaining_bytes],
            "after_move": after_move,
            "after_remove": after_remove,
        }

    world.record(operation)


@then("the original, copied, and moved bytes equal the uploaded bytes")
def lifecycle_bytes_match(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert all(
        value == world.storage_bytes for value in world.last_outcome.value["bytes"]
    )


@then("moving the copy leaves only the original and moved paths")
def moved_paths_match(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value["after_move"] == sorted(
        [world.storage_path, f"{world.storage_path}.moved"]
    )


@then("removing the moved object leaves the original unchanged")
def removed_path_is_absent(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value["after_remove"] == [world.storage_path]
    assert world.last_outcome.value["bytes"][3] == world.storage_bytes


def _storage_bucket(world: ContractWorld) -> StorageBucket:
    return world.client.storage.from_(world.fixture["bucket_name"])


def _clean_storage_object(world: ContractWorld) -> None:
    bucket = _storage_bucket(world)
    if any(
        item.name == world.storage_path
        for item in bucket.list(world.storage_path).objects
    ):
        bucket.remove(world.storage_path)


def _partial_upload(world: ContractWorld) -> dict[str, Any]:
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

    def operation() -> dict[str, Any]:
        value = _partial_upload(world)
        bucket = _storage_bucket(world)
        session = value["session"]
        value["progress"] = bucket.get_upload_session(
            world.storage_path, session_id=session.session_id
        )
        bucket.upload_part(
            world.storage_path,
            session_id=session.session_id,
            part_number=2,
            data=value["bytes"][session.part_size :],
        )
        value["object"] = bucket.complete_upload_session(
            world.storage_path, session_id=session.session_id
        )
        value["download"] = bucket.download(world.storage_path)
        return value

    world.record(operation)


@then("upload progress describes exactly the first uploaded part")
def partial_upload_progress(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    value = world.last_outcome.value
    progress, session, part = value["progress"], value["session"], value["part"]
    assert progress.session_id == session.session_id
    assert progress.path == world.storage_path
    assert progress.content_type == "application/octet-stream"
    assert progress.status == "uploading"
    assert progress.total_size == len(value["bytes"])
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
    value = world.last_outcome.value
    assert value["object"].name == world.storage_path
    assert value["object"].mime_type == "application/octet-stream"
    assert value["object"].size == len(value["bytes"])
    assert value["download"] == value["bytes"]


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
                read()
            except NotFoundError:
                outcomes[name] = "not found"
            else:
                outcomes[name] = "unexpected success"
        return outcomes

    world.record(operation)


@then("the aborted session and unfinished object are not found")
def aborted_upload_is_gone(context: Context) -> None:
    assert _outcome(context).value == {
        "session": "not found",
        "object": "not found",
    }


@when("the client makes the contract object public and private again")
def change_contract_visibility(context: Context) -> None:
    world = _world(context)

    def operation() -> dict[str, Any]:
        bucket = _storage_bucket(world)
        world.cleanup_callbacks.append(lambda: _clean_storage_object(world))
        bucket.upload(world.storage_path, world.storage_bytes)
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

    world.record(operation)


@then("anonymous reads return the original bytes only while the object is public")
def anonymous_visibility_matches(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    value = world.last_outcome.value
    assert all(world.storage_bytes not in body for body in value["private_bytes"])
    assert {key: value[key] for key in ("statuses", "bytes", "visibility")} == {
        "statuses": [404, 200, 404],
        "bytes": world.storage_bytes,
        "visibility": [True, False],
    }


@then("the stored object path equals the contract path")
def stored_object_path_matches(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value["path"] == world.storage_path


@given("a service-role client")
def service_role_client(context: Context) -> None:
    assert _world(context).fixture["service_key"]


@when("the client acquires and releases the contract lock")
def acquire_and_release_lock(context: Context) -> None:
    world = _world(context)

    def operation() -> dict[str, Any]:
        lease = world.service_client.locks.acquire(world.lock_key, ttl=10)
        cleanup = world.register_lock_cleanup(world.lock_key, lease)
        world.service_client.locks.release(world.lock_key, lease)
        world.cleanup_callbacks.remove(cleanup)

        replacement = world.service_client.locks.acquire(world.lock_key, ttl=10)
        replacement_cleanup = world.register_lock_cleanup(world.lock_key, replacement)
        world.service_client.locks.release(world.lock_key, replacement)
        world.cleanup_callbacks.remove(replacement_cleanup)
        return {"lease": lease, "released": replacement.token != lease.token}

    world.record(operation)


@then("the released lease is no longer held")
def released_lease_not_held(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value["released"] is True


@given("a project-owner client")
def project_owner_client(context: Context) -> None:
    assert _world(context).fixture["platform_token"]


@when("the client starts the contract durable function")
def start_durable_execution(context: Context) -> None:
    world = _world(context)
    world.record(world.start_durable_execution)


@when("the client starts the contract durable function twice under one execution name")
def start_durable_execution_twice(context: Context) -> None:
    world = _world(context)

    def operation() -> tuple[Any, Any]:
        return world.start_durable_execution(), world.start_durable_execution()

    world.record(operation)


@when("the client recovers the contract lock with caller-owned tokens")
def recover_lock(context: Context) -> None:
    world = _world(context)

    def operation() -> dict[str, Any]:
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

    world.record(operation)


@then("the started execution carries its id, function, name, region, and creation time")
def started_execution_is_addressable(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    execution = world.last_outcome.value
    assert execution.id
    assert execution.function_id
    assert execution.name == world.durable_execution_name
    assert execution.region
    assert execution.created_at is not None


@then("the started execution is not terminal and carries no result")
def started_execution_is_a_handle(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value.is_terminal is False
    assert world.last_outcome.value.result is None


@then("both starts return the same execution")
def both_starts_return_one_execution(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    first, second = world.last_outcome.value
    assert second.id == first.id
    assert second.name == first.name


@when("the owner reads the execution until it is terminal")
def read_execution_until_terminal(context: Context) -> None:
    world = _world(context)
    if world.last_outcome is not None and not world.last_outcome.ok:
        return
    assert world.started_execution is not None
    execution_id = world.started_execution.id
    world.record(lambda: world.follow_durable_execution(execution_id))


@then("the execution succeeded carrying the function's result")
def execution_succeeded_with_result(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value.status == "succeeded"
    assert world.last_outcome.value.result == {"echoed": world.durable_payload["value"]}


@when("the owner lists the durable function's executions")
def list_durable_executions(context: Context) -> None:
    world = _world(context)
    if world.last_outcome is not None and not world.last_outcome.ok:
        return
    world.record(world.list_durable_executions)


@then("the listed executions include the started execution")
def listed_executions_include_the_started_one(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.started_execution is not None
    listed = {execution.id for execution in world.last_outcome.value.executions}
    assert world.started_execution.id in listed


@then("recovery and renewal preserve the held lease until release")
def recovered_lock_lifecycle(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    value = world.last_outcome.value
    assert value["held"].held is True
    assert value["available"].held is False
    world.cleanup_callbacks.remove(value["cleanup"])
    assert (
        value["token"]
        == value["lease"].token
        == value["recovered"].token
        == value["renewed"].token
    )
    assert value["lease"].fencing_token is not None
    assert (
        value["lease"].fencing_token
        == value["recovered"].fencing_token
        == value["held"].fencing_token
        == value["renewed"].fencing_token
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

    world.record(operation)


@then("the force-released lock is available")
def force_released_lock_available(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value["available"].held is False
    world.cleanup_callbacks.remove(world.last_outcome.value["cleanup"])


@when("the client reacquires the force-released contract lock")
def reacquire_force_released_lock(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    original = world.last_outcome.value["lease"]

    def operation() -> object:
        replacement = world.service_client.locks.acquire(world.lock_key, ttl=30)
        world.register_lock_cleanup(world.lock_key, replacement)
        return {"original": original, "replacement": replacement}

    world.record(operation)


@then("the replacement owner receives a higher fencing token")
def replacement_lock_fence_increases(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    original = world.last_outcome.value["original"]
    replacement = world.last_outcome.value["replacement"]
    assert replacement.token != original.token
    assert original.fencing_token is not None
    assert replacement.fencing_token > original.fencing_token


@given("two authenticated realtime clients")
def two_realtime_clients(context: Context) -> None:
    world = _world(context)
    try:
        clients = [
            world.client,
            type(world.client)(
                api_url=world.fixture["api_url"],
                anon_key=world.fixture["anon_key"],
            ),
        ]
        for client in clients:
            client.auth.sign_in(
                email=world.fixture["user_email"],
                password=world.fixture["user_password"],
            )
        world.realtime_clients = clients
        subscriber = clients[0].realtime.channel(world.realtime_channel)
        publisher = clients[1].realtime.channel(world.realtime_channel)
        world.subscriber = subscriber
        world.publisher = publisher

        async def subscribe() -> None:
            await asyncio.gather(
                subscriber.subscribe(),
                publisher.subscribe(),
            )

        world.run(subscribe())
    except CONTRACT_EXCEPTIONS as error:
        world.last_outcome = Outcome(
            ok=False,
            category=classify_error(error),
            error=error,
        )


async def publish_contract_message(world: ContractWorld) -> Any:
    assert world.subscriber is not None
    assert world.publisher is not None
    received = world.loop.create_future()

    def on_message(message: Any) -> None:
        if not received.done():
            received.set_result(message)

    world.subscriber.on("message", on_message)
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
    world.record(
        lambda: world.client.functions.invoke(
            world.fixture["function_name"], {"value": "contract"}
        )
    )


@when("the client invokes the contract function by name")
def invoke_contract_function(context: Context) -> None:
    world = _world(context)

    def operation() -> Any:
        return world.service_client.functions.invoke(
            world.fixture["function_name"], {"value": "contract"}
        )

    world.record(operation)


@then("the function echoes the payload")
def function_echoed_payload(context: Context) -> None:
    # The function is reachable only at the endpoint the platform resolved, on a
    # domain the API URL does not name, so an echo coming back is what proves
    # the SDK sent the request there rather than somewhere it guessed.
    world = _world(context)
    assert world.last_outcome is not None
    response = world.last_outcome.value
    assert response.status == HTTP_OK, response
    assert response.data == {"echoed": "contract"}, response.data


@given("a read-only project logs client")
def project_logs_client(context: Context) -> None:
    context.logs_contract = LogContract(_world(context))


@when("the contract function emits three unique structured log events")
def emit_three_logs(context: Context) -> None:
    context.logs_contract.emit(3)


@when("the contract function emits one unique structured log event")
def emit_one_log(context: Context) -> None:
    context.logs_contract.emit(1)


@when("the client searches and paginates those events within 240 seconds")
def search_contract_logs(context: Context) -> None:
    _world(context).record(context.logs_contract.search)


@when("the client reads matching log activity within 120 seconds")
def read_contract_log_activity(context: Context) -> None:
    _world(context).record(context.logs_contract.activity)


@then("all three structured events retain their metadata without duplicates")
def verify_contract_logs(context: Context) -> None:
    context.logs_contract.verify_events(_outcome(context).value)


@then("activity counts exactly that event in its function and level buckets")
def verify_contract_log_activity(context: Context) -> None:
    context.logs_contract.verify_activity(_outcome(context).value)


@when("one presence client joins and leaves while the other remains subscribed")
def observe_presence_membership(context: Context) -> None:
    world = _world(context)
    if world.last_outcome is not None and not world.last_outcome.ok:
        return
    world.record(lambda: world.run(verify_presence_membership(world)))


@then(
    "both rosters identify the contract user "
    "and the original handler observes membership changes"
)
def verify_presence_rosters(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value == [1, 2, 1]


@when("the clients observe an inserted and updated contract row")
def observe_postgres_changes(context: Context) -> None:
    world = _world(context)
    if world.last_outcome is not None and not world.last_outcome.ok:
        return
    world.record(lambda: world.run(verify_postgres_changes(world)))


@then("automatic and lightweight notifications retain metadata and row identity")
def verify_postgres_rows(context: Context) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value == ["INSERT", "UPDATE"]
