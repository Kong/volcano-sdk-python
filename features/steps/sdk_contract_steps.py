from __future__ import annotations

import asyncio
from typing import Any

from behave import given, then, when
from contract_support import (
    CONTRACT_EXCEPTIONS,
    ContractWorld,
    Outcome,
    classify_error,
)

_INVALID_AUTH_CREDENTIAL = "invalid-contract-refresh-token"


def _world(context: Any) -> ContractWorld:
    return context.contract


@given("the confirmed contract user")
def confirmed_contract_user(context: Any) -> None:
    assert _world(context).fixture["user_id"]


@when("the client signs in with the contract user's credentials")
def sign_in(context: Any) -> None:
    world = _world(context)
    world.record(
        lambda: world.client.auth.sign_in(
            email=world.fixture["user_email"],
            password=world.fixture["user_password"],
        )
    )


@then("the SDK operation succeeds")
def operation_succeeds(context: Any) -> None:
    outcome = _world(context).last_outcome
    assert outcome is not None
    assert outcome.ok, f"SDK operation failed ({outcome.category})"


@then("the SDK operation fails")
def operation_fails(context: Any) -> None:
    outcome = _world(context).last_outcome
    assert outcome is not None
    assert not outcome.ok


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


@given("a unique unconfirmed contract user")
def unique_unconfirmed_user(context: Any) -> None:
    world = _world(context)
    assert world.unique_email.endswith("@example.com")


@when("the client signs up with the new user's credentials")
def sign_up_unique_user(context: Any) -> None:
    world = _world(context)
    world.record(
        lambda: world.client.auth.sign_up(
            email=world.unique_email,
            password=world.unique_password,
        )
    )


@then("sign-up is acknowledged without a session")
def signup_is_sessionless(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value.session is None


@then("the current session is empty")
def current_session_is_empty(context: Any) -> None:
    assert _world(context).client.current_session is None


@given("the client is signed in as the confirmed contract user")
def signed_in_contract_user(context: Any) -> None:
    _world(context).authenticate()


@when("the client retrieves the current user")
def retrieve_current_user(context: Any) -> None:
    world = _world(context)
    world.record(world.client.auth.get_user)


@then("the current user belongs to the contract user")
def current_user_matches_fixture(context: Any) -> None:
    world = _world(context)
    assert world.client.current_user is not None
    assert world.client.current_user.id == world.fixture["user_id"]


@when("the client updates the current user's metadata")
def update_current_user_metadata(context: Any) -> None:
    world = _world(context)
    world.record(
        lambda: world.client.auth.update_user(
            user_metadata={"contract_marker": world.metadata_marker}
        )
    )


@then("the current user contains the updated metadata")
def current_user_has_metadata(context: Any) -> None:
    world = _world(context)
    assert world.client.current_user is not None
    assert world.client.current_user.user_metadata is not None
    assert (
        world.client.current_user.user_metadata["contract_marker"]
        == world.metadata_marker
    )


@when("the client refreshes the current session")
def refresh_current_session(context: Any) -> None:
    world = _world(context)
    session = world.client.current_session
    assert session is not None
    world.previous_access_token = session.access_token
    world.previous_refresh_token = session.refresh_token
    world.record(world.client.auth.refresh_session)


@then("the current session exposes rotated access and refresh tokens")
def session_tokens_are_rotated(context: Any) -> None:
    world = _world(context)
    session = world.client.current_session
    assert session is not None
    assert session.access_token != world.previous_access_token
    assert session.refresh_token
    assert session.refresh_token != world.previous_refresh_token


@when("the client refreshes with an invalid refresh token")
def refresh_with_invalid_token(context: Any) -> None:
    world = _world(context)
    session = world.client.current_session
    assert session is not None
    world.client = type(world.client)(
        api_url=world.fixture["api_url"],
        anon_key=world.fixture["anon_key"],
        access_token=session.access_token,
        refresh_token=_INVALID_AUTH_CREDENTIAL,
    )
    world.record(world.client.auth.refresh_session)


@when("the client signs out")
def sign_out(context: Any) -> None:
    world = _world(context)
    world.record(world.client.auth.sign_out)


@when("the client subscribes to auth-state changes")
def subscribe_auth_state(context: Any) -> None:
    world = _world(context)
    world.unsubscribe_auth = world.client.auth.on_auth_state_change(
        lambda user: world.listener_events.append(user.id if user is not None else None)
    )


@then("the listener immediately observes the current user")
def listener_observes_current_user(context: Any) -> None:
    world = _world(context)
    assert world.listener_events == [world.fixture["user_id"]]


@then("the listener observes the signed-out state")
def listener_observes_signout(context: Any) -> None:
    world = _world(context)
    assert world.listener_events[-1] is None


@when("the client unsubscribes from auth-state changes")
def unsubscribe_auth_state(context: Any) -> None:
    world = _world(context)
    assert world.unsubscribe_auth is not None
    world.unsubscribe_auth()
    world.listener_event_count = len(world.listener_events)


@then("the listener receives no additional events")
def listener_receives_no_events(context: Any) -> None:
    world = _world(context)
    assert len(world.listener_events) == world.listener_event_count


@given("a unique anonymous contract user")
def unique_anonymous_user(context: Any) -> None:
    world = _world(context)
    assert world.unique_email.endswith("@example.com")


@when("the client signs up anonymously")
def sign_up_anonymously(context: Any) -> None:
    world = _world(context)
    outcome = world.record(world.client.auth.sign_up_anonymous)
    if outcome.ok:
        world.anonymous_user_id = outcome.value.user_id


@then("the current session belongs to the anonymous user")
def session_belongs_to_anonymous_user(context: Any) -> None:
    world = _world(context)
    assert world.client.current_session is not None
    assert world.client.current_session.user_id == world.anonymous_user_id


@when("the client converts the anonymous user with credentials")
def convert_anonymous_user(context: Any) -> None:
    world = _world(context)
    world.record(
        lambda: world.client.auth.convert_anonymous(
            email=world.unique_email,
            password=world.unique_password,
        )
    )


@then("the converted user keeps the anonymous user identity")
def converted_user_keeps_identity(context: Any) -> None:
    world = _world(context)
    assert world.client.current_user is not None
    assert world.client.current_user.id == world.anonymous_user_id


@given("the client is signed in as the confirmed contract user on multiple sessions")
def signed_in_on_multiple_sessions(context: Any) -> None:
    world = _world(context)
    world.authenticate()
    world.secondary_client = type(world.client)(
        api_url=world.fixture["api_url"],
        anon_key=world.fixture["anon_key"],
    )
    world.secondary_client.auth.sign_in(
        email=world.fixture["user_email"],
        password=world.fixture["user_password"],
    )


@when("the client lists the current user's sessions")
def list_current_user_sessions(context: Any) -> None:
    world = _world(context)
    world.record(world.client.auth.get_sessions)


@then("the session list contains the current session")
def session_list_contains_current(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert any(session.is_current for session in world.last_outcome.value.sessions)


@when("the client deletes another current-user session")
def delete_other_session(context: Any) -> None:
    world = _world(context)
    page = world.client.auth.get_sessions()
    other = next(session for session in page.sessions if not session.is_current)
    world.deleted_session_id = other.id

    def operation() -> Any:
        world.client.auth.delete_session(session_id=other.id)
        return world.client.auth.get_sessions()

    world.record(operation)


@then("the deleted session is absent from the session list")
def deleted_session_is_absent(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert all(
        session.id != world.deleted_session_id
        for session in world.last_outcome.value.sessions
    )


@when("the client deletes all current-user sessions")
def delete_all_current_user_sessions(context: Any) -> None:
    world = _world(context)

    def operation() -> None:
        world.client.auth.delete_all_other_sessions()
        world.client.auth.sign_out()

    world.record(operation)


@given("an authenticated client")
def authenticated_client(context: Any) -> None:
    _world(context).authenticate()


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
