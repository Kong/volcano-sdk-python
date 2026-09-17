from __future__ import annotations

import asyncio
import time
from typing import Any
from uuid import uuid4

from behave import given, then, when
from broadcast_pause import verify_broadcast_pause
from contract_support import (
    CONTRACT_EXCEPTIONS,
    ContractWorld,
    Outcome,
    classify_error,
)

from volcano_sdk import Session, VolcanoClient

ACCESS_TOKEN_CLOCK_TICK_SECONDS = 1.1
HTTP_OK = 200
REJECTED_BEARER = "sdk-contract-rejected-access-token"


def _world(context: Any) -> ContractWorld:
    return context.contract


@given("the confirmed contract user")
def confirmed_contract_user(context: Any) -> None:
    assert _world(context).fixture["user_id"]


@given("the client listens for auth state changes")
def listen_for_auth_state_changes(context: Any) -> None:
    world = _world(context)
    subscription = world.client.auth.on_auth_state_change(
        lambda event, session: world.auth_state_events.append((event, session))
    )
    world.cleanup_callbacks.append(subscription.unsubscribe)


@when("the client signs in with the contract user's credentials")
def sign_in(context: Any) -> None:
    world = _world(context)
    world.record(
        lambda: world.client.auth.sign_in(
            email=world.fixture["user_email"],
            password=world.fixture["user_password"],
        )
    )


@when("the client reads the current session")
def read_current_session(context: Any) -> None:
    world = _world(context)
    world.record(world.client.auth.get_session)


@when("a fresh client adopts the current session")
def adopt_current_session(context: Any) -> None:
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
def refresh_current_session(context: Any) -> None:
    world = _world(context)
    world.previous_session = world.client.auth.get_session()
    assert world.previous_session is not None
    time.sleep(ACCESS_TOKEN_CLOCK_TICK_SECONDS)
    world.record(world.client.auth.refresh_session)


@when("a fresh client starts with only the current access token")
def bootstrap_access_token(context: Any) -> None:
    world = _world(context)
    source = world.client
    world.previous_session = source.auth.get_session()
    assert world.previous_session is not None
    world.cleanup_callbacks.append(source.auth.sign_out)
    world.client = VolcanoClient(
        api_url=world.fixture["api_url"],
        anon_key=world.fixture["anon_key"],
        access_token=world.previous_session.access_token,
    )
    world.record(world.client.auth.get_session)


@then("the token-only session has no cached user")
def token_session_has_no_user(context: Any) -> None:
    session = _world(context).client.current_session
    assert session is not None
    assert session.user_id is None
    assert session.user is None


@then("the session retains only the supplied access token")
def token_session_retains_access(context: Any) -> None:
    world = _world(context)
    session = world.client.current_session
    assert session is not None
    assert world.previous_session is not None
    assert session.access_token == world.previous_session.access_token
    assert session.refresh_token is None


@then("the refreshed session becomes current")
def refreshed_session_becomes_current(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value is not world.previous_session
    assert world.last_outcome.value.access_token != world.previous_session.access_token
    assert world.client.auth.get_session() is world.last_outcome.value


@when("the client signs out")
def sign_out(context: Any) -> None:
    world = _world(context)
    world.signed_out_session = world.client.auth.get_session()
    assert world.signed_out_session is not None
    world.record(world.client.auth.sign_out)


@then("the current session is empty")
def current_session_is_empty(context: Any) -> None:
    assert _world(context).client.auth.get_session() is None


@when("a fresh client tries to refresh the signed-out session")
def refresh_signed_out_session(context: Any) -> None:
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
def operation_fails_with_authentication_error(context: Any) -> None:
    outcome = _world(context).last_outcome
    assert outcome is not None
    assert not outcome.ok
    assert outcome.category == "authentication error"


@then("the SDK operation succeeds")
def operation_succeeds(context: Any) -> None:
    outcome = _world(context).last_outcome
    assert outcome is not None
    assert outcome.ok, f"SDK operation failed ({outcome.category}): {outcome.error}"


@then("the current session belongs to the contract user")
def session_belongs_to_contract_user(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value.user_id == world.fixture["user_id"]
    assert world.client.current_session is not None
    assert world.client.current_session.user_id == world.fixture["user_id"]


@then("the current session exposes access and refresh tokens")
def session_exposes_tokens(context: Any) -> None:
    world = _world(context)
    session = world.client.current_session
    assert session is not None
    assert session.access_token
    assert session.refresh_token


@then("the auth-state listener observes the signed-in contract user")
def auth_state_listener_observes_signed_in_user(context: Any) -> None:
    world = _world(context)
    assert any(
        event == "SIGNED_IN"
        and session is not None
        and session.user_id == world.fixture["user_id"]
        for event, session in world.auth_state_events
    )


@given("an authenticated client")
def authenticated_client(context: Any) -> None:
    _world(context).authenticate()


@given("the client replaces its access token with a rejected token")
def replace_access_token(context: Any) -> None:
    client = _world(context).client
    session = client.auth.get_session()
    assert session is not None
    client.auth.set_session(
        Session(
            access_token=REJECTED_BEARER,
            refresh_token=session.refresh_token,
            user_id=session.user_id,
        )
    )


@then("the profile read replaces the rejected token for the same user")
@then("the storage operation replaces the rejected token for the same user")
@then("the database read replaces the rejected token for the same user")
def read_replaced_token(context: Any) -> None:
    world = _world(context)
    session = world.client.auth.get_session()
    assert session is not None
    assert session.access_token
    assert session.access_token != REJECTED_BEARER
    assert session.refresh_token
    assert session.user_id == world.fixture["user_id"]


@when("the client loads its server-validated profile")
def load_server_profile(context: Any) -> None:
    world = _world(context)
    world.record(world.client.auth.get_user)


@then("the returned and cached profiles belong to the contract user")
def profiles_belong_to_contract_user(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value.id == world.fixture["user_id"]
    session = world.client.current_session
    assert session is not None
    assert session.user is not None
    assert session.user["id"] == world.fixture["user_id"]


@when("one client pauses delivery for 1 second and then resumes with the same handler")
def pause_and_resume(context: Any) -> None:
    world = _world(context)
    if world.last_outcome is not None and not world.last_outcome.ok:
        return
    world.record(lambda: world.run(verify_broadcast_pause(world)))


@when('the client selects the contract table where "slug" equals the fixture slug')
def select_fixture_row(context: Any) -> None:
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
def fixture_row_returned(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value == [world.fixture["fixture_row"]]


@when("the client inserts its contract row")
def insert_contract_row(context: Any) -> None:
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
def inserted_contract_row_returned(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    expected = world.fixture["mutation_rows"]["insert"]
    assert world.last_outcome.value == [expected]


@when("the client updates its contract row")
def update_contract_row(context: Any) -> None:
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
def updated_contract_row_returned(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    expected = world.fixture["mutation_rows"]["update"]["after"]
    assert world.last_outcome.value == [expected]


@when("the client deletes its contract row")
def delete_contract_row(context: Any) -> None:
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
def deleted_contract_row_returned(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    expected = world.fixture["mutation_rows"]["delete"]
    assert world.last_outcome.value == [expected]


@when("the client updates a missing contract row")
def update_missing_contract_row(context: Any) -> None:
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
def delete_missing_contract_row(context: Any) -> None:
    world = _world(context)
    table = world.client.database(world.fixture["database_name"]).from_(
        world.fixture["table_name"]
    )
    missing_slug = f"{world.fixture['fixture_row']['slug']}-missing"
    world.record(lambda: table.delete().eq("slug", missing_slug).execute())


@then("the mutation returns an empty row list")
def mutation_returns_empty_list(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value == []


@then("the existing contract row is unchanged")
def existing_contract_row_unchanged(context: Any) -> None:
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
def upload_and_download(context: Any) -> None:
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
def downloaded_bytes_match(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value["bytes"] == world.storage_bytes


@when(
    "the client uploads the contract object as text/plain and reads its stored metadata"
)
def upload_and_read_metadata(context: Any) -> None:
    world = _world(context)

    def operation() -> dict[str, Any]:
        bucket = world.client.storage.from_(world.fixture["bucket_name"])
        uploaded = bucket.upload(
            world.storage_path, world.storage_bytes, content_type="text/plain"
        )
        world.cleanup_callbacks.append(lambda: bucket.remove(world.storage_path))
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
def stored_content_types_match(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value["content_type"] == "text/plain"
    assert world.last_outcome.value["listed"] == [
        {"name": world.storage_path, "mime_type": "text/plain"}
    ]


@when("the client uploads the contract object and downloads bytes 2 through 7")
def upload_and_download_range(context: Any) -> None:
    world = _world(context)

    def operation() -> dict[str, Any]:
        bucket = world.client.storage.from_(world.fixture["bucket_name"])
        uploaded = bucket.upload(world.storage_path, world.storage_bytes)
        world.cleanup_callbacks.append(lambda: bucket.remove(world.storage_path))
        return {
            "bytes": bucket.download(world.storage_path, byte_range="bytes=2-7"),
            "path": uploaded["name"],
        }

    world.record(operation)


@then("the downloaded bytes equal uploaded bytes 2 through 7 inclusive")
def downloaded_range_matches(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value["bytes"] == world.storage_bytes[2:8]


@when("the client copies, moves, and removes a copy of the contract object")
def copy_move_and_remove(context: Any) -> None:
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
def lifecycle_bytes_match(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert all(
        value == world.storage_bytes for value in world.last_outcome.value["bytes"]
    )


@then("moving the copy leaves only the original and moved paths")
def moved_paths_match(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value["after_move"] == sorted(
        [world.storage_path, f"{world.storage_path}.moved"]
    )


@then("removing the moved object leaves the original unchanged")
def removed_path_is_absent(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value["after_remove"] == [world.storage_path]
    assert world.last_outcome.value["bytes"][3] == world.storage_bytes


@then("the stored object path equals the contract path")
def stored_object_path_matches(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value["path"] == world.storage_path


@given("a service-role client")
def service_role_client(context: Any) -> None:
    assert _world(context).fixture["service_key"]


@when("the client acquires and releases the contract lock")
def acquire_and_release_lock(context: Any) -> None:
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
def released_lease_not_held(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value["released"] is True


@when("the client recovers the contract lock with caller-owned tokens")
def recover_lock(context: Any) -> None:
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


@then("recovery and renewal preserve the held lease until release")
def recovered_lock_lifecycle(context: Any) -> None:
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
def force_release_lock(context: Any) -> None:
    world = _world(context)

    def operation() -> object:
        locks, key = world.service_client.locks, world.lock_key
        lease = locks.acquire(key, ttl=30)
        cleanup = world.register_lock_cleanup(key, lease)
        locks.force_release(key, request_id=str(uuid4()))
        return {"lease": lease, "cleanup": cleanup, "available": locks.get(key)}

    world.record(operation)


@then("the force-released lock is available")
def force_released_lock_available(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value["available"].held is False
    world.cleanup_callbacks.remove(world.last_outcome.value["cleanup"])


@when("the client reacquires the force-released contract lock")
def reacquire_force_released_lock(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    original = world.last_outcome.value["lease"]

    def operation() -> object:
        replacement = world.service_client.locks.acquire(world.lock_key, ttl=30)
        world.register_lock_cleanup(world.lock_key, replacement)
        return {"original": original, "replacement": replacement}

    world.record(operation)


@then("the replacement owner receives a higher fencing token")
def replacement_lock_fence_increases(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    original = world.last_outcome.value["original"]
    replacement = world.last_outcome.value["replacement"]
    assert replacement.token != original.token
    assert original.fencing_token is not None
    assert replacement.fencing_token > original.fencing_token


@given("two authenticated realtime clients")
def two_realtime_clients(context: Any) -> None:
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
        world.subscriber = clients[0].realtime.channel(world.realtime_channel)
        world.publisher = clients[1].realtime.channel(world.realtime_channel)

        async def subscribe() -> None:
            await asyncio.gather(
                world.subscriber.subscribe(),
                world.publisher.subscribe(),
            )

        world.run(subscribe())
    except CONTRACT_EXCEPTIONS as error:
        world.last_outcome = Outcome(
            ok=False,
            category=classify_error(error),
            error=error,
        )


@when("one client subscribes and the other publishes the contract message")
def subscribe_and_publish(context: Any) -> None:
    world = _world(context)
    if world.last_outcome is not None and not world.last_outcome.ok:
        return

    async def operation() -> Any:
        assert world.subscriber is not None
        assert world.publisher is not None
        received = world.loop.create_future()

        def on_message(message: Any) -> None:
            if not received.done():
                received.set_result(message)

        world.subscriber.on("message", on_message)
        await world.publisher.send(world.realtime_message)
        return await asyncio.wait_for(received, timeout=10)

    try:
        world.last_outcome = Outcome(ok=True, value=world.run(operation()))
    except CONTRACT_EXCEPTIONS as error:
        world.last_outcome = Outcome(
            ok=False,
            category=classify_error(error),
            error=error,
        )


@then("the subscriber receives the contract message within 10 seconds")
def subscriber_received_message(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value == world.realtime_message


@when("the client invokes the contract function by name")
def invoke_contract_function(context: Any) -> None:
    world = _world(context)

    def operation() -> Any:
        return world.service_client.functions.invoke(
            world.fixture["function_name"], {"value": "contract"}
        )

    world.record(operation)


@then("the function echoes the payload")
def function_echoed_payload(context: Any) -> None:
    # The function is reachable only at the endpoint the platform resolved, on a
    # domain the API URL does not name, so an echo coming back is what proves
    # the SDK sent the request there rather than somewhere it guessed.
    world = _world(context)
    assert world.last_outcome is not None
    response = world.last_outcome.value
    assert response.status == HTTP_OK, response
    assert response.data == {"echoed": "contract"}, response.data
