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
    assert outcome.ok, f"SDK operation failed ({outcome.category}): {outcome.error}"


@then("the current session belongs to the contract user")
def session_belongs_to_contract_user(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value.user_id == world.fixture["user_id"]
    assert world.client.current_session is not None
    assert world.client.current_session.user_id == world.fixture["user_id"]


@given("an authenticated client")
def authenticated_client(context: Any) -> None:
    _world(context).authenticate()


@when('the client selects the contract table where "slug" equals the fixture slug')
def select_fixture_row(context: Any) -> None:
    world = _world(context)
    world.record(
        lambda: world.client.database(world.fixture["database_name"])
        .from_(world.fixture["table_name"])
        .select("*")
        .eq("slug", world.fixture["fixture_row"]["slug"])
        .execute()
    )


@then("exactly the fixture row is returned")
def fixture_row_returned(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value == [world.fixture["fixture_row"]]


@when("the client uploads and downloads the contract object")
def upload_and_download(context: Any) -> None:
    world = _world(context)

    def operation() -> bytes:
        bucket = world.client.storage.from_(world.fixture["bucket_name"])
        bucket.upload(world.storage_path, world.storage_bytes)
        return bucket.download(world.storage_path)

    world.record(operation)


@then("the downloaded bytes equal the uploaded bytes")
def downloaded_bytes_match(context: Any) -> None:
    world = _world(context)
    assert world.last_outcome is not None
    assert world.last_outcome.value == world.storage_bytes


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
