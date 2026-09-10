from __future__ import annotations

import asyncio
import time
from typing import Any

from behave import given, then, when
from contract_support import (
    CONTRACT_EXCEPTIONS,
    ContractWorld,
    Outcome,
    classify_error,
)

from volcano_sdk import VolcanoClient
from volcano_sdk._generated.models.create_frontend_custom_domain_request import (
    CreateFrontendCustomDomainRequest,
)
from volcano_sdk._generated.models.frontend_custom_domain_response import (
    FrontendCustomDomainResponse,
)
from volcano_sdk._generated.models.managed_frontend_custom_domain_tls_config import (
    ManagedFrontendCustomDomainTLSConfig,
)

ACCESS_TOKEN_CLOCK_TICK_SECONDS = 1.1


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


@given("a managed custom-domain TLS request")
def managed_tls_request(context: Any) -> None:
    _world(context).managed_tls_request = CreateFrontendCustomDomainRequest(
        domain="app.example.com",
        tls=ManagedFrontendCustomDomainTLSConfig(mode="managed"),
    )


@when("the client encodes the request and decodes a pending verification response")
def encode_managed_tls_request(context: Any) -> None:
    world = _world(context)
    world.managed_tls_wire_request = world.managed_tls_request.to_dict()
    world.managed_tls_response = FrontendCustomDomainResponse.from_dict(
        {
            "domain": "app.example.com",
            "tls_mode": "managed",
            "domain_status": "pending_verification",
            "verification_status": "pending",
            "verification_records": [
                {
                    "name": "_token.app.example.com",
                    "type": "CNAME",
                    "value": "_validation.volcano.dev",
                }
            ],
            "required_routing_record": {
                "record_type": "CNAME",
                "zone_apex_record_type": "ALIAS",
                "name": "app.example.com",
                "value": "frontend.frontends.volcano.dev",
            },
            "effective_urls": ["https://frontend.frontends.volcano.dev/"],
            "created_at": "2026-09-02T12:00:00Z",
            "updated_at": "2026-09-02T12:00:00Z",
        }
    )


@then("the request selects managed TLS without certificate material")
def managed_tls_request_has_no_certificate(context: Any) -> None:
    assert _world(context).managed_tls_wire_request == {
        "domain": "app.example.com",
        "tls": {"mode": "managed"},
    }


@then("the response exposes the managed lifecycle and DNS records")
def managed_tls_response_has_lifecycle(context: Any) -> None:
    response = _world(context).managed_tls_response
    assert response.domain == "app.example.com"
    assert response.tls_mode == "managed"
    assert response.domain_status == "pending_verification"
    assert response.verification_status == "pending"
    assert response.verification_records[0].to_dict() == {
        "name": "_token.app.example.com",
        "type": "CNAME",
        "value": "_validation.volcano.dev",
    }
    assert response.required_routing_record.to_dict() == {
        "record_type": "CNAME",
        "zone_apex_record_type": "ALIAS",
        "name": "app.example.com",
        "value": "frontend.frontends.volcano.dev",
    }
