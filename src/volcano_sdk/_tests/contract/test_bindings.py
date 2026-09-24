from __future__ import annotations

import asyncio
import hashlib
import importlib
import json
import os
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING, Protocol, cast, runtime_checkable
from unittest.mock import AsyncMock, Mock, call

import behave.step_registry as behave_step_registry
import broadcast_pause
import contract_fixture
import environment as contract_environment
import httpx
import logs_contract
import postgres_changes
import presence_membership
import pytest
from behave.runner import Context
from contract_support import ContractWorld, Outcome
from steps import sdk_contract_steps

from volcano_sdk import FunctionResponse, LogActivityResponse, Session, VolcanoClient
from volcano_sdk._tests.contract.fakes import (
    FailingBucket,
    FailingPresenceChannel,
    PausePublisher,
    PauseSubscriber,
)
from volcano_sdk._tests.session_fixtures import access_token
from volcano_sdk._transport import GeneratedTransport
from volcano_sdk.auth import Auth
from volcano_sdk.realtime import PostgresChange

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from volcano_sdk.models import JSONValue

ROOT = Path(__file__).parents[4]


class _Runner:
    config: object = object()


_RUNNER = _Runner()


@runtime_checkable
class _StepRegistry(Protocol):
    steps: object

    def clear(self) -> None: ...


@runtime_checkable
class _StepDefinition(Protocol):
    pattern: str


def _registry() -> _StepRegistry:
    value = cast("object", behave_step_registry.registry)
    assert isinstance(value, _StepRegistry)
    return value


def _bound_patterns() -> set[str]:
    steps = _registry().steps
    assert isinstance(steps, dict)
    entries = cast("dict[object, object]", steps)
    bound: set[str] = set()
    for definitions in entries.values():
        assert isinstance(definitions, list)
        for definition in cast("list[object]", definitions):
            assert isinstance(definition, _StepDefinition)
            assert isinstance(definition.pattern, str)
            bound.add(definition.pattern)
    return bound


def _fixture() -> contract_fixture.ContractFixture:
    decoded = cast(
        "object",
        json.loads((ROOT / "tests/fixtures/sdk-contract-dry-run.json").read_text()),
    )
    assert contract_fixture.is_contract_fixture(decoded)
    return decoded


def _context(world: ContractWorld) -> Context:
    context = Context(_RUNNER)
    context.contract = world
    return context


FEATURE_SHA256 = {
    "storage-lifecycle.feature": (
        "08d00ac825bc186929904dea75af28052df964e446e7aeb0e2266711536aa88f"
    ),
    "storage-range.feature": (
        "807424f26ccdf72e74b359eb52a807f3ae4657f95cdef0255f636a8f588e49cd"
    ),
    "storage-metadata.feature": (
        "8a99fab83abf3d73e41ab8557f681b8b1659299a942a1ceb18a2f85009f5af6e"
    ),
    "auth.feature": "c237deb0b3be98d64689699a0ffdcd272e7ef027a2b69439b1768195042ed493",
    "functions.feature": (
        "ee6d02540eb8c6216fc18b47f7ef91f5db9a45649749a2ed47d692ae42a1e4e0"
    ),
    "database-delete.feature": (
        "b328579ee9b33cbb313dd4d13eb899d53f64344c5e5beb00dbfb7eed2098e2c7"
    ),
    "database-insert.feature": (
        "46150600af9f54b690bc5c9b8f230c5ba4e3be755e50ad0921051faa95e45316"
    ),
    "database-update.feature": (
        "7a64470474f2ba842faf1b8352ccc2cd7efa8183212ab309c1321dffb9c093d3"
    ),
    "database-refresh.feature": (
        "76eb18c448899a6849e84015f1a276a984e1005eb494042b45247c67923cac89"
    ),
    "realtime-pause.feature": (
        "d4ff3e9cab94dfe1adabbe50e47c6ff46ca8fc48b357f1d9c425aea6d8519e33"
    ),
    "database.feature": (
        "4685b29357a621068b25984ff0de29cd4c504eebe5cfb597f0b999e29878a668"
    ),
    "durable.feature": (
        "416f7dfe1347086bf08af6f15c31467c58e21e14b278e3fd7482f7042dda06d7"
    ),
    "locks.feature": "76fa31f9a7c203e33b367e5ca1467b2334e7c85c960de8d5cab8638920137411",
    "realtime.feature": (
        "e65862e27656cdd0afa8e552cb5a628d9831568e3299711e572ccd4f6b750696"
    ),
    "storage.feature": (
        "0772d46691d2a158e752d19cea995ff79db960fc3774c799ebdf081e19424d82"
    ),
    "auth-profile-refresh.feature": (
        "df46f1c374fcbdeb790cde0781ff14f580e56c44ac9aa6445d97469a385f6f51"
    ),
    "auth-request-recovery.feature": (
        "9fa6f8d6cb3bca89501d32d950f06b8982ed34b888cce134465e0358b8261e8f"
    ),
    "auth-token-bootstrap.feature": (
        "7f2cef1489ce2cb5a9f3ba230d7f411197415a0f4a3c14f38361c5ce0522e0ac"
    ),
    "database-queries.feature": (
        "37d7f2e8fd4efb035cbc094c9c91a44a86f15fbcd689627e525e8d04f033a928"
    ),
    "functions-refresh.feature": (
        "34ca84c8a4cf7f06addf7ff6f4c01c9546fac131e99b3d1509ae54f896d1bd9e"
    ),
    "locks-recovery.feature": (
        "4f4b52caf587bdc61e72cbdcc39dcf5c9b06ea8573d8b99a183c2644e375ffab"
    ),
    "logs.feature": "5616e288fe1a68e13fa70416fe0323a5ce830c0edaa885a387efbf9e5bb2a269",
    "realtime-postgres.feature": (
        "794c2ecbb94fd262a37840f4c3fe3bd9f9ee58c22fda9df2a46de60f93e52c91"
    ),
    "realtime-presence.feature": (
        "b4429f6e3df60a6a98be4daf1d8517e2cd7cee651f9eb6463a1090ab49a102b5"
    ),
    "storage-refresh.feature": (
        "00257b455f9897791db7fd82c4166c7f34c7134b5b9f4ea92f509bba533751a1"
    ),
    "storage-sessions.feature": (
        "037c60a8da27ec4cc5777596ba0c669b8309181a54b27aa61882535ed2f6beb1"
    ),
}


def test_contract_features_match_shared_source() -> None:
    copied = ROOT / "features" / "contract"
    assert {path.name for path in copied.glob("*.feature")} == FEATURE_SHA256.keys()
    for name, expected in FEATURE_SHA256.items():
        assert hashlib.sha256((copied / name).read_bytes()).hexdigest() == expected


def test_contract_storage_feature_matches_shared_source() -> None:
    feature = ROOT / "features" / "contract" / "storage-refresh.feature"
    expected = "00257b455f9897791db7fd82c4166c7f34c7134b5b9f4ea92f509bba533751a1"
    assert hashlib.sha256(feature.read_bytes()).hexdigest() == expected


def test_contract_profile_feature_matches_shared_source() -> None:
    feature = ROOT / "features" / "contract" / "auth-profile-refresh.feature"
    expected = "df46f1c374fcbdeb790cde0781ff14f580e56c44ac9aa6445d97469a385f6f51"
    assert hashlib.sha256(feature.read_bytes()).hexdigest() == expected


def test_contract_lock_recovery_matches_shared_source() -> None:
    feature = ROOT / "features" / "contract" / "locks-recovery.feature"
    expected = "4f4b52caf587bdc61e72cbdcc39dcf5c9b06ea8573d8b99a183c2644e375ffab"
    assert hashlib.sha256(feature.read_bytes()).hexdigest() == expected


def test_contract_token_bootstrap_feature_matches_shared_source() -> None:
    feature = ROOT / "features" / "contract" / "auth-token-bootstrap.feature"
    expected = "7f2cef1489ce2cb5a9f3ba230d7f411197415a0f4a3c14f38361c5ce0522e0ac"
    assert hashlib.sha256(feature.read_bytes()).hexdigest() == expected


def test_contract_auth_request_feature_matches_shared_source() -> None:
    feature = ROOT / "features" / "contract" / "auth-request-recovery.feature"
    expected = "9fa6f8d6cb3bca89501d32d950f06b8982ed34b888cce134465e0358b8261e8f"
    assert hashlib.sha256(feature.read_bytes()).hexdigest() == expected


def test_contract_database_queries_match_shared_source() -> None:
    feature = ROOT / "features" / "contract" / "database-queries.feature"
    expected = "37d7f2e8fd4efb035cbc094c9c91a44a86f15fbcd689627e525e8d04f033a928"
    assert hashlib.sha256(feature.read_bytes()).hexdigest() == expected


def test_contract_storage_sessions_match_shared_source() -> None:
    feature = ROOT / "features" / "contract" / "storage-sessions.feature"
    expected = "037c60a8da27ec4cc5777596ba0c669b8309181a54b27aa61882535ed2f6beb1"
    assert hashlib.sha256(feature.read_bytes()).hexdigest() == expected


def test_every_contract_phrase_is_bound_verbatim() -> None:
    _registry().clear()
    _ = importlib.reload(sdk_contract_steps)
    bound = _bound_patterns()
    assert bound == {
        "the authenticated client invokes the contract function by name",
        "the function invocation replaces the rejected token for the same user",
        "the client selects a projected page of query fixture members",
        "the projected page contains only beta and gamma in that order",
        "the client selects query fixture rows with each comparison filter",
        "each comparison returns exactly the matching query fixture rows",
        (
            "the client selects query fixture rows with "
            "case-sensitive and insensitive patterns"
        ),
        "each pattern returns exactly the matching query fixture rows",
        "the client selects query fixture rows with null and boolean filters",
        "each identity filter returns exactly the matching query fixture rows",
        "the client uploads one part and resumes the contract upload",
        "upload progress describes exactly the first uploaded part",
        "the completed multipart object preserves its path, type, and bytes",
        "the client uploads one part and aborts the contract upload",
        "the aborted session and unfinished object are not found",
        "the client makes the contract object public and private again",
        "anonymous reads return the original bytes only while the object is public",
        "the client copies, moves, and removes a copy of the contract object",
        "the original, copied, and moved bytes equal the uploaded bytes",
        "moving the copy leaves only the original and moved paths",
        "removing the moved object leaves the original unchanged",
        "the client uploads the contract object and downloads bytes 2 through 7",
        "the downloaded bytes equal uploaded bytes 2 through 7 inclusive",
        (
            "the client uploads the contract object as text/plain "
            "and reads its stored metadata"
        ),
        "the uploaded and listed object content types are text/plain",
        "the client replaces its access token with a rejected token",
        "the database read replaces the rejected token for the same user",
        "the storage operation replaces the rejected token for the same user",
        "the profile read replaces the rejected token for the same user",
        "the session list replaces the rejected token for the same user",
        "the client lists its server sessions",
        "the session list contains the current session for the contract user",
        "the client loads its server-validated profile",
        "the returned and cached profiles belong to the contract user",
        (
            "a fresh client tries to refresh a supplied profile "
            "without a session identifier"
        ),
        "a fresh client starts with only the current access token",
        "a fresh client starts with a rejected access token",
        "the token-only session has no cached user",
        "the session retains only the supplied access token",
        (
            "one client pauses delivery for 1 second "
            "and then resumes with the same handler"
        ),
        "a service-role client",
        "a project-owner client",
        "the client starts the contract durable function",
        (
            "the client starts the contract durable function twice "
            "under one execution name"
        ),
        (
            "the started execution carries its id, function, name, region, "
            "and creation time"
        ),
        "the started execution is not terminal and carries no result",
        "both starts return the same execution",
        "the owner reads the execution until it is terminal",
        "the execution succeeded carrying the function's result",
        "the owner lists the durable function's executions",
        "the listed executions include the started execution",
        "the client invokes the contract function by name",
        "the function echoes the payload",
        "a fresh client adopts the current session",
        "a fresh client tries to refresh the signed-out session",
        "a fresh client loads a profile with the signed-out access token",
        "an authenticated client",
        "exactly the deleted contract row is returned",
        "exactly the fixture row is returned",
        "exactly the inserted contract row is returned",
        "exactly the updated contract row is returned",
        "one client subscribes and the other publishes the contract message",
        "the auth-state listener observes the signed-in contract user",
        "the SDK operation succeeds",
        "the client recovers the contract lock with caller-owned tokens",
        "recovery and renewal preserve the held lease until release",
        "the client acquires and force releases the contract lock",
        "the force-released lock is available",
        "the client reacquires the force-released contract lock",
        "the replacement owner receives a higher fencing token",
        "the SDK operation fails",
        "the client acquires and releases the contract lock",
        "the client deletes its contract row",
        "the client deletes a missing contract row",
        "the client updates a missing contract row",
        "the existing contract row is unchanged",
        "the mutation returns an empty row list",
        "the client inserts its contract row",
        'the client selects the contract table where "slug" equals the fixture slug',
        "the client reads the current session",
        "the client refreshes the current session",
        "the client listens for auth state changes",
        "the client signs out",
        "the client signs in with the contract user's credentials",
        "the client uploads and downloads the contract object",
        "the client updates its contract row",
        "the confirmed contract user",
        "the current session belongs to the contract user",
        "the current session exposes access and refresh tokens",
        "the current session is empty",
        "the downloaded bytes equal the uploaded bytes",
        "the refreshed session becomes current",
        "the released lease is no longer held",
        "the SDK operation fails with an authentication error",
        "the stored object path equals the contract path",
        "the subscriber receives the contract message within 10 seconds",
        "two authenticated realtime clients",
        "the clients observe an inserted and updated contract row",
        "automatic and lightweight notifications retain metadata and row identity",
        "a read-only project logs client",
        "the contract function emits three unique structured log events",
        "the contract function emits one unique structured log event",
        "the client searches and paginates those events within 240 seconds",
        "the client reads matching log activity within 120 seconds",
        "all three structured events retain their metadata without duplicates",
        "activity counts exactly that event in its function and level buckets",
        "one presence client joins and leaves while the other remains subscribed",
        (
            "both rosters identify the contract user "
            "and the original handler observes membership changes"
        ),
    }


@pytest.mark.parametrize("leak", [False, True])
def test_broadcast_pause_checks_silence(
    monkeypatch: pytest.MonkeyPatch, *, leak: bool
) -> None:
    world = ContractWorld(_fixture())
    subscriber = PauseSubscriber()
    monkeypatch.setattr(world, "subscriber", subscriber)
    monkeypatch.setattr(world, "publisher", PausePublisher(subscriber, leak=leak))
    world.realtime_message = {"event": "message", "value": "contract"}
    sleep = AsyncMock()
    monkeypatch.setattr(asyncio, "sleep", sleep)
    try:
        if leak:
            with pytest.raises(AssertionError, match="while paused"):
                _ = asyncio.run(broadcast_pause.verify_broadcast_pause(world))
        else:
            assert (
                asyncio.run(broadcast_pause.verify_broadcast_pause(world))
                == world.realtime_message
            )
        assert subscriber.on_count == 1
        sleep.assert_awaited_once_with(1)
    finally:
        world.cleanup()


def test_durable_idempotency_binding_starts_twice_and_records_both_handles(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _registry().clear()
    _ = importlib.reload(sdk_contract_steps)
    steps = sdk_contract_steps
    first = SimpleNamespace(id="execution", name="contract")
    second = SimpleNamespace(id="execution", name="contract")
    fixture = _fixture()
    world = ContractWorld(fixture)
    start = Mock(side_effect=[first, second])
    monkeypatch.setattr(world, "start_durable_execution", start)
    try:
        steps.start_durable_execution_twice(_context(world))

        assert start.call_args_list == [call(), call()]
        assert world.last_outcome is not None
        assert world.last_outcome.ok is True
        assert world.last_outcome.value == (first, second)
    finally:
        world.cleanup()


def test_realtime_contract_pair_authenticates_and_owns_both_clients(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _registry().clear()
    _ = importlib.reload(sdk_contract_steps)
    steps = sdk_contract_steps
    fixture = _fixture()
    world = ContractWorld(fixture)
    signed_in: list[tuple[str, str]] = []

    def sign_in(_auth: object, *, email: str, password: str) -> None:
        signed_in.append((email, password))

    async def subscribe_pair(_subscriber: object, _publisher: object) -> None:
        pass

    monkeypatch.setattr(Auth, "sign_in", sign_in)
    monkeypatch.setattr(steps, "_subscribe_pair", subscribe_pair)
    try:
        steps.two_realtime_clients(_context(world))
        subscriber, publisher = world.subscriber, world.publisher
        assert subscriber is not None
        assert publisher is not None
        assert len(world.realtime_clients) == 2
        assert world.subscriber is subscriber
        assert world.publisher is publisher
        channel_name = f"broadcast:{world.realtime_channel}"
        assert subscriber.name == publisher.name == channel_name
        assert signed_in == [(fixture["user_email"], fixture["user_password"])] * 2
    finally:
        world.cleanup()


def test_lifecycle_cleanup_attempts_all_paths_after_a_deletion_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _registry().clear()
    _ = importlib.reload(sdk_contract_steps)
    steps = sdk_contract_steps
    paths = ["contract.txt", "contract.txt.copy", "contract.txt.moved"]
    bucket = FailingBucket(paths)
    fixture = _fixture()
    world = ContractWorld(fixture)

    def bucket_for(_name: str) -> FailingBucket:
        return bucket

    def record(_operation: Callable[[], object]) -> Outcome:
        return Outcome(ok=True)

    monkeypatch.setattr(world.client.storage, "from_", bucket_for)
    world.fixture["bucket_name"] = "assets"
    world.storage_path = paths[0]
    monkeypatch.setattr(world, "record", record)
    steps.copy_move_and_remove(_context(world))

    with pytest.raises(ExceptionGroup, match="Python contract cleanup failed"):
        world.cleanup()

    assert bucket.removed == list(reversed(paths))
    assert world.loop.is_closed()


def test_fixture_loader_requires_absolute_private_file(tmp_path: Path) -> None:
    environment = contract_environment
    fixture = tmp_path / "fixture.json"
    _ = fixture.write_text(
        (ROOT / "tests/fixtures/sdk-contract-dry-run.json").read_text(),
        encoding="utf-8",
    )

    fixture.chmod(0o644)
    with pytest.raises(PermissionError, match="0600"):
        _ = environment.load_fixture(fixture)

    fixture.chmod(0o600)
    assert environment.load_fixture(fixture)["project_id"] == "dry-run-project"

    previous = Path.cwd()
    os.chdir(tmp_path)
    try:
        with pytest.raises(ValueError, match="absolute"):
            _ = environment.load_fixture(Path("fixture.json"))
    finally:
        os.chdir(previous)


def test_fixture_loader_rejects_incomplete_or_malformed_contract_data(
    tmp_path: Path,
) -> None:
    environment = contract_environment
    fixture = tmp_path / "fixture.json"
    _ = fixture.write_text(
        (ROOT / "tests/fixtures/sdk-contract-dry-run.json").read_text(),
        encoding="utf-8",
    )
    fixture.chmod(0o600)
    valid = environment.load_fixture(fixture)
    invalid_cases: tuple[dict[str, object], ...] = (
        {},
        {**valid, "project_id": 3},
        {**valid, "fixture_row": {"slug": 3, "value": "value"}},
        {**valid, "mutation_rows": {**valid["mutation_rows"], "insert": {}}},
    )
    for invalid in invalid_cases:
        _ = fixture.write_text(json.dumps(invalid), encoding="utf-8")
        fixture.chmod(0o600)
        with pytest.raises(TypeError, match="complete contract fixture"):
            _ = environment.load_fixture(fixture)


def test_contract_fixture_validator_checks_every_declared_string_field() -> None:
    fixture_module = contract_fixture
    assert set(fixture_module.STRING_FIELDS) == set(
        fixture_module.ContractFixture.__annotations__
    ) - {"fixture_row", "mutation_rows"}


@pytest.mark.parametrize("revoked", [False, True])
def test_bootstrap_cleanup_is_disarmed_only_after_successful_revocation(
    monkeypatch: pytest.MonkeyPatch, *, revoked: bool
) -> None:
    _registry().clear()
    _ = importlib.reload(sdk_contract_steps)
    steps = sdk_contract_steps
    world = ContractWorld(_fixture())
    source = world.client
    _ = source.auth.set_session(Session("captured-access", "refresh", "user"))
    sign_out_calls = 0

    def sign_out() -> None:
        nonlocal sign_out_calls
        sign_out_calls += 1

    def record(_operation: Callable[[], object]) -> Outcome:
        return Outcome(ok=revoked)

    monkeypatch.setattr(source.auth, "sign_out", sign_out)
    monkeypatch.setattr(world, "record", record)
    try:
        steps.bootstrap_access_token(_context(world))
        steps.sign_out(_context(world))
    finally:
        world.cleanup()
    assert sign_out_calls == (0 if revoked else 1)


def test_rejected_token_binding_preserves_refreshable_session_identity() -> None:
    _registry().clear()
    _ = importlib.reload(sdk_contract_steps)
    steps = sdk_contract_steps
    user = "00000000-0000-4000-8000-000000000001"
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "access_token": access_token("renewed"),
                "refresh_token": "rotated",
                "token_type": "bearer",
                "expires_in": 3600,
                "user": {"id": user, "email": "u@example.com", "status": "active"},
            },
        )

    client = VolcanoClient(
        anon_key="anon",
        _transport=GeneratedTransport(
            api_url="https://api.test", httpx_transport=httpx.MockTransport(handle)
        ),
    )
    _ = client.auth.set_session(Session(access_token(), "refresh", user))
    fixture = _fixture()
    world = ContractWorld(fixture)
    world.client = client
    world.fixture["user_id"] = user
    context = _context(world)
    try:
        steps.replace_access_token(context)
        assert client.current_session is not None
        assert client.current_session.access_token != access_token()
        assert (
            client.current_session.access_token.split(".")[:2]
            == access_token().split(".")[:2]
        )
        _ = client.auth.refresh_session()
        steps.read_replaced_token(context)
        assert len(requests) == 1
        assert requests[0].url.path == "/auth/refresh"
    finally:
        world.cleanup()


@pytest.mark.parametrize("leaking_response", [None, 0, 1])
def test_visibility_assertion_rejects_private_payload_leaks(
    leaking_response: int | None,
) -> None:
    _registry().clear()
    _ = importlib.reload(sdk_contract_steps)
    steps = sdk_contract_steps
    content = b"private contract content"
    private_bytes = [b"not found", b"not found"]
    if leaking_response is not None:
        private_bytes[leaking_response] = b"prefix: " + content
    fixture = _fixture()
    world = ContractWorld(fixture)
    world.storage_bytes = content
    world.last_outcome = Outcome(
        ok=True,
        value={
            "statuses": [404, 200, 404],
            "bytes": content,
            "visibility": [True, False],
            "private_bytes": private_bytes,
        },
    )
    context = _context(world)
    try:
        if leaking_response is None:
            steps.anonymous_visibility_matches(context)
        else:
            with pytest.raises(AssertionError):
                steps.anonymous_visibility_matches(context)
    finally:
        world.cleanup()


def test_contract_logs_feature_matches_shared_source() -> None:
    feature = ROOT / "features" / "contract" / "logs.feature"
    expected = "5616e288fe1a68e13fa70416fe0323a5ce830c0edaa885a387efbf9e5bb2a269"
    assert hashlib.sha256(feature.read_bytes()).hexdigest() == expected


def test_log_contract_rejects_duplicate_and_wrong_resource_events() -> None:
    world = ContractWorld(_fixture())
    world.fixture["function_id"] = "function-id"
    contract = logs_contract.LogContract(world)
    events: list[Mapping[str, JSONValue]] = [
        {
            "id": f"event-{ordinal}",
            "timestamp": f"2026-09-18T12:00:0{2 - ordinal}Z",
            "body": {"marker": contract.marker, "ordinal": ordinal},
            "resource": {"type": "function", "id": "function-id"},
            "level": "info",
        }
        for ordinal in range(3)
    ]
    try:
        contract.verify_events(events)
        with pytest.raises(AssertionError):
            contract.verify_events([events[0], events[0], events[2]])
        events[1] = {
            **events[1],
            "resource": {"type": "function", "id": "another-function"},
        }
        with pytest.raises(AssertionError):
            contract.verify_events(events)
        malformed_event: dict[str, JSONValue] = {**events[1], "resource": None}
        with pytest.raises(AssertionError):
            contract.verify_events([events[0], malformed_event, events[2]])
    finally:
        world.cleanup()


def test_log_activity_contract_rejects_wrong_resource_counts() -> None:
    world = ContractWorld(_fixture())
    world.fixture["function_id"] = "function-id"
    contract = logs_contract.LogContract(world)

    def activity(resource_ids: JSONValue) -> LogActivityResponse:
        return LogActivityResponse(
            total=1,
            data=(
                {
                    "total": 1,
                    "counts": {"resource_ids": resource_ids, "levels": {"info": 1}},
                },
                {"total": 0, "counts": {"resource_ids": {}, "levels": {}}},
            ),
        )

    try:
        contract.verify_activity(activity({"function-id": 1}))
        with pytest.raises(AssertionError):
            contract.verify_activity(activity({"another-function": 1}))
        with pytest.raises(AssertionError):
            contract.verify_activity(activity(None))
    finally:
        world.cleanup()


@pytest.mark.parametrize("server_skew_seconds", [-120, 120])
def test_log_bounds_allow_server_clock_skew(
    monkeypatch: pytest.MonkeyPatch, server_skew_seconds: int
) -> None:
    world = ContractWorld(_fixture())

    def invoke(_name: str, _payload: JSONValue) -> FunctionResponse:
        return FunctionResponse(
            data={"echoed": "contract"}, status=200, headers={}, version=None
        )

    monkeypatch.setattr(
        world.service_client.functions,
        "invoke",
        invoke,
    )
    contract = logs_contract.LogContract(world)
    server_time = datetime.now(UTC) + timedelta(seconds=server_skew_seconds)
    try:
        contract.emit(1)
        start = contract.request["start_time"]
        end = contract.request["end_time"]
        assert isinstance(start, str)
        assert isinstance(end, str)
        assert datetime.fromisoformat(start) < server_time
        assert server_time < datetime.fromisoformat(end)
    finally:
        world.cleanup()


def test_contract_presence_feature_matches_shared_source() -> None:
    feature = ROOT / "features" / "contract" / "realtime-presence.feature"
    expected = "b4429f6e3df60a6a98be4daf1d8517e2cd7cee651f9eb6463a1090ab49a102b5"
    assert hashlib.sha256(feature.read_bytes()).hexdigest() == expected


@pytest.mark.parametrize(
    ("snapshots", "expected"),
    [
        ([{"first"}, {"first", "second"}, {"first"}], True),
        ([{"first"}, {"first", "second"}], False),
        ([{"first", "second"}, {"first"}], False),
    ],
)
def test_presence_requires_original_handler_membership_sequence(
    snapshots: list[set[str]], *, expected: bool
) -> None:
    module = presence_membership
    assert (
        module.observed_membership(snapshots, {"first"}, {"first", "second"})
        is expected
    )


def test_contract_postgres_feature_matches_shared_source() -> None:
    feature = ROOT / "features" / "contract" / "realtime-postgres.feature"
    expected = "794c2ecbb94fd262a37840f4c3fe3bd9f9ee58c22fda9df2a46de60f93e52c91"
    assert hashlib.sha256(feature.read_bytes()).hexdigest() == expected


def _wrong_change(event: PostgresChange, field: str) -> PostgresChange:
    if field == "record":
        return replace(event, record={"id": "wrong-value"})
    if field == "id":
        return replace(event, id="wrong-value")
    if field == "table":
        return replace(event, table="wrong-value")
    if field == "mode":
        return replace(event, mode="lightweight")
    raise ValueError(field)


@pytest.mark.parametrize(
    ("automatic", "wrong_field"),
    [(True, "record"), (False, "id"), (True, "table"), (True, "id"), (True, "mode")],
)
def test_postgres_notification_checks_reject_wrong_identity(
    *, automatic: bool, wrong_field: str
) -> None:
    row: dict[str, JSONValue] = {"id": "row", "value": "inserted", "owner_id": "user"}
    event = PostgresChange(
        type="INSERT",
        schema="public",
        table="records",
        timestamp="2026-09-18T12:00:00Z",
        record=row if automatic else None,
        id=None if automatic else "row",
        mode=None if automatic else "lightweight",
    )
    postgres_changes.verify_change(event, "INSERT", "records", row, automatic=automatic)
    changed = _wrong_change(event, wrong_field)
    with pytest.raises(AssertionError):
        postgres_changes.verify_change(
            changed, "INSERT", "records", row, automatic=automatic
        )


@pytest.mark.parametrize("automatic", [True, False])
def test_postgres_observer_ignores_other_rows(
    monkeypatch: pytest.MonkeyPatch, *, automatic: bool
) -> None:
    client = VolcanoClient(api_url="https://api.test", anon_key="anon")
    channel = client.realtime.channel("contract-postgres")
    callbacks: list[Callable[[PostgresChange], None]] = []

    def on_postgres_changes(
        _event: str,
        *,
        schema: str,
        table: str,
        callback: Callable[[PostgresChange], None],
    ) -> Callable[[], None]:
        assert schema == "public"
        assert table in {"records", "records_other"}
        callbacks.append(callback)
        return lambda: None

    monkeypatch.setattr(channel, "on_postgres_changes", on_postgres_changes)
    observer = postgres_changes.ChangeObserver(channel, "records", "row")
    other = PostgresChange(
        type="INSERT",
        schema="public",
        table="records",
        record={"id": "other"} if automatic else None,
        id=None if automatic else "other",
    )
    for callback in callbacks:
        callback(other)
    assert not observer.events
    assert not observer.inserts
    assert not observer.wrong_table
    own = PostgresChange(
        type="INSERT",
        schema="public",
        table="records",
        record={"id": "row"} if automatic else None,
        id=None if automatic else "row",
    )
    callbacks[0](own)
    callbacks[1](own)
    assert asyncio.run(observer.next()) is own
    assert observer.inserts == [own]
    observer.close()


def test_presence_retains_channel_name_at_platform_length_boundary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stop = RuntimeError("valid channel")

    def channel(name: str, *, channel_type: str) -> FailingPresenceChannel:
        assert len(name) <= 64
        assert channel_type == "presence"
        return FailingPresenceChannel(stop)

    world = ContractWorld(_fixture())
    world.realtime_channel = "x" * 64
    world.fixture["user_id"] = "user"
    other = VolcanoClient(api_url="https://api.test", anon_key="anon")
    world.realtime_clients = [world.client, other]
    monkeypatch.setattr(world.client.realtime, "channel", channel)
    monkeypatch.setattr(other.realtime, "channel", channel)
    try:
        with pytest.raises(RuntimeError, match="valid channel") as error:
            _ = asyncio.run(presence_membership.verify_presence_membership(world))
    finally:
        world.cleanup()
    assert error.value is stop
