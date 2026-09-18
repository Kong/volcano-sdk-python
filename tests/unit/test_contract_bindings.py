from __future__ import annotations

import asyncio
import hashlib
import importlib.util
import os
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, Mock, call

import httpx
import pytest
from behave.step_registry import registry
from session_fixtures import access_token

from volcano_sdk import Session, VolcanoClient
from volcano_sdk._transport import GeneratedTransport

if TYPE_CHECKING:
    from types import ModuleType

ROOT = Path(__file__).parents[2]
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
    "locks.feature": "76fa31f9a7c203e33b367e5ca1467b2334e7c85c960de8d5cab8638920137411",
    "realtime.feature": (
        "e65862e27656cdd0afa8e552cb5a628d9831568e3299711e572ccd4f6b750696"
    ),
    "storage.feature": (
        "0772d46691d2a158e752d19cea995ff79db960fc3774c799ebdf081e19424d82"
    ),
}


def _load_module(name: str, path: Path) -> ModuleType:
    features_path = str(ROOT / "features")
    if features_path not in sys.path:
        sys.path.insert(0, features_path)
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_contract_features_match_shared_source() -> None:
    copied = ROOT / "features" / "contract"
    assert {path.name for path in copied.glob("*.feature")} == FEATURE_SHA256.keys()
    for name, expected in FEATURE_SHA256.items():
        assert hashlib.sha256((copied / name).read_bytes()).hexdigest() == expected


def test_staged_storage_feature_matches_proposed_shared_source() -> None:
    staged = ROOT / "features" / "staged" / "storage-refresh.feature"
    expected = "00257b455f9897791db7fd82c4166c7f34c7134b5b9f4ea92f509bba533751a1"
    assert hashlib.sha256(staged.read_bytes()).hexdigest() == expected


def test_staged_profile_feature_matches_proposed_shared_source() -> None:
    staged = ROOT / "features" / "staged" / "auth-profile-refresh.feature"
    expected = "df46f1c374fcbdeb790cde0781ff14f580e56c44ac9aa6445d97469a385f6f51"
    assert hashlib.sha256(staged.read_bytes()).hexdigest() == expected


def test_staged_lock_recovery_matches_proposed_shared_source() -> None:
    staged = ROOT / "features" / "staged" / "locks-recovery.feature"
    expected = "4f4b52caf587bdc61e72cbdcc39dcf5c9b06ea8573d8b99a183c2644e375ffab"
    assert hashlib.sha256(staged.read_bytes()).hexdigest() == expected


def test_staged_token_bootstrap_feature_matches_proposed_shared_source() -> None:
    staged = ROOT / "features" / "staged" / "auth-token-bootstrap.feature"
    expected = "7f2cef1489ce2cb5a9f3ba230d7f411197415a0f4a3c14f38361c5ce0522e0ac"
    assert hashlib.sha256(staged.read_bytes()).hexdigest() == expected


def test_staged_auth_request_feature_matches_proposed_shared_source() -> None:
    staged = ROOT / "features" / "staged" / "auth-request-recovery.feature"
    expected = "9fa6f8d6cb3bca89501d32d950f06b8982ed34b888cce134465e0358b8261e8f"
    assert hashlib.sha256(staged.read_bytes()).hexdigest() == expected


def test_staged_database_queries_match_proposed_shared_source() -> None:
    staged = ROOT / "features" / "staged" / "database-queries.feature"
    expected = "37d7f2e8fd4efb035cbc094c9c91a44a86f15fbcd689627e525e8d04f033a928"
    assert hashlib.sha256(staged.read_bytes()).hexdigest() == expected


def test_staged_storage_sessions_match_proposed_shared_source() -> None:
    staged = ROOT / "features" / "staged" / "storage-sessions.feature"
    expected = "037c60a8da27ec4cc5777596ba0c669b8309181a54b27aa61882535ed2f6beb1"
    assert hashlib.sha256(staged.read_bytes()).hexdigest() == expected


def test_every_contract_phrase_is_bound_verbatim() -> None:
    registry.clear()
    _load_module(
        "contract_steps", ROOT / "features" / "steps" / "sdk_contract_steps.py"
    )
    bound = {
        definition.pattern
        for definitions in registry.steps.values()
        for definition in definitions
    }
    assert bound == {
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
        "a read-only project logs client",
        "the contract function emits three unique structured log events",
        "the contract function emits one unique structured log event",
        "the client searches and paginates those events within 240 seconds",
        "the client reads matching log activity within 120 seconds",
        "all three structured events retain their metadata without duplicates",
        "activity counts exactly that event in its function and level buckets",
    }


@pytest.mark.parametrize("leak", [False, True])
def test_broadcast_pause_checks_silence(
    monkeypatch: pytest.MonkeyPatch, *, leak: bool
) -> None:
    pause = _load_module(
        "contract_broadcast_pause", ROOT / "features" / "broadcast_pause.py"
    )
    subscriber = SimpleNamespace(
        on=Mock(), subscribe=AsyncMock(), unsubscribe=AsyncMock()
    )

    async def publish(message: object) -> None:
        paused = subscriber.unsubscribe.await_count > subscriber.subscribe.await_count
        if leak or not paused:
            subscriber.on.call_args.args[1](message)

    world = SimpleNamespace(
        subscriber=subscriber,
        publisher=SimpleNamespace(send=AsyncMock(side_effect=publish)),
        realtime_message={"event": "message", "value": "contract"},
    )
    monkeypatch.setattr(pause.asyncio, "sleep", AsyncMock())
    if leak:
        with pytest.raises(AssertionError, match="while paused"):
            asyncio.run(pause.verify_broadcast_pause(world))
    else:
        assert (
            asyncio.run(pause.verify_broadcast_pause(world)) == world.realtime_message
        )
    subscriber.on.assert_called_once()
    pause.asyncio.sleep.assert_awaited_once_with(1)


def test_lifecycle_cleanup_attempts_all_paths_after_a_deletion_failure() -> None:
    registry.clear()
    steps = _load_module(
        "contract_steps", ROOT / "features" / "steps" / "sdk_contract_steps.py"
    )
    paths = ["contract.txt", "contract.txt.copy", "contract.txt.moved"]
    bucket = Mock()
    bucket.list.return_value.objects = [SimpleNamespace(name=path) for path in paths]
    bucket.remove.side_effect = [RuntimeError("delete failed"), None, None]
    world = SimpleNamespace(
        client=SimpleNamespace(
            storage=SimpleNamespace(from_=Mock(return_value=bucket))
        ),
        fixture={"bucket_name": "assets"},
        storage_path=paths[0],
        cleanup_callbacks=[],
        realtime_clients=[],
        loop=Mock(),
        record=Mock(),
    )
    steps.copy_move_and_remove(SimpleNamespace(contract=world))

    with pytest.raises(ExceptionGroup, match="Python contract cleanup failed"):
        steps.ContractWorld.cleanup(world)

    assert bucket.remove.call_args_list == [call(path) for path in reversed(paths)]
    world.loop.close.assert_called_once()


def test_fixture_loader_requires_absolute_private_file(tmp_path: Path) -> None:
    environment = _load_module(
        "contract_environment", ROOT / "features" / "environment.py"
    )
    fixture = tmp_path / "fixture.json"
    fixture.write_text("{}", encoding="utf-8")

    fixture.chmod(0o644)
    with pytest.raises(PermissionError, match="0600"):
        environment.load_fixture(fixture)

    fixture.chmod(0o600)
    assert environment.load_fixture(fixture) == {}

    previous = Path.cwd()
    os.chdir(tmp_path)
    try:
        with pytest.raises(ValueError, match="absolute"):
            environment.load_fixture(Path("fixture.json"))
    finally:
        os.chdir(previous)


@pytest.mark.parametrize("revoked", [False, True])
def test_bootstrap_cleanup_is_disarmed_only_after_successful_revocation(
    monkeypatch: pytest.MonkeyPatch, *, revoked: bool
) -> None:
    registry.clear()
    steps = _load_module(
        "contract_steps", ROOT / "features" / "steps" / "sdk_contract_steps.py"
    )
    source = Mock()
    source.auth.get_session.return_value = SimpleNamespace(
        access_token="captured-access"
    )
    target = Mock()
    world = SimpleNamespace(
        client=source,
        fixture={"api_url": "https://api.test", "anon_key": "anon"},
        cleanup_callbacks=[],
        realtime_clients=[],
        loop=Mock(),
        bootstrap_cleanup=None,
        record=Mock(return_value=SimpleNamespace(ok=revoked)),
    )
    with monkeypatch.context() as patch:
        patch.setattr(steps, "VolcanoClient", Mock(return_value=target))
        steps.bootstrap_access_token(SimpleNamespace(contract=world))
        steps.sign_out(SimpleNamespace(contract=world))
        steps.ContractWorld.cleanup(world)
    assert source.auth.sign_out.call_count == (0 if revoked else 1)


def test_rejected_token_binding_preserves_refreshable_session_identity() -> None:
    registry.clear()
    steps = _load_module(
        "contract_steps", ROOT / "features/steps/sdk_contract_steps.py"
    )
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
    client.auth.set_session(Session(access_token(), "refresh", user))
    world = SimpleNamespace(client=client, fixture={"user_id": user})
    context = SimpleNamespace(contract=world)
    steps.replace_access_token(context)
    assert client.current_session is not None
    assert client.current_session.access_token != access_token()
    assert (
        client.current_session.access_token.split(".")[:2]
        == access_token().split(".")[:2]
    )
    client.auth.refresh_session()
    steps.read_replaced_token(context)
    assert len(requests) == 1
    assert requests[0].url.path == "/auth/refresh"


@pytest.mark.parametrize("leaking_response", [None, 0, 1])
def test_visibility_assertion_rejects_private_payload_leaks(
    leaking_response: int | None,
) -> None:
    registry.clear()
    steps = _load_module(
        "contract_steps", ROOT / "features" / "steps" / "sdk_contract_steps.py"
    )
    content = b"private contract content"
    private_bytes = [b"not found", b"not found"]
    if leaking_response is not None:
        private_bytes[leaking_response] = b"prefix: " + content
    world = SimpleNamespace(
        storage_bytes=content,
        last_outcome=SimpleNamespace(
            value={
                "statuses": [404, 200, 404],
                "bytes": content,
                "visibility": [True, False],
                "private_bytes": private_bytes,
            }
        ),
    )
    context = SimpleNamespace(contract=world)
    if leaking_response is None:
        steps.anonymous_visibility_matches(context)
    else:
        with pytest.raises(AssertionError):
            steps.anonymous_visibility_matches(context)


def test_staged_logs_feature_matches_proposed_shared_source() -> None:
    staged = ROOT / "features" / "staged" / "logs.feature"
    expected = "5616e288fe1a68e13fa70416fe0323a5ce830c0edaa885a387efbf9e5bb2a269"
    assert hashlib.sha256(staged.read_bytes()).hexdigest() == expected


def test_log_contract_rejects_duplicate_and_wrong_resource_events() -> None:
    module = _load_module("logs_contract", ROOT / "features" / "logs_contract.py")
    world = SimpleNamespace(
        fixture={
            "api_url": "https://api.test",
            "anon_key": "anon",
            "logs_access_token": "project-token",
            "function_id": "function-id",
        }
    )
    contract = module.LogContract(world)
    events = [
        {
            "id": f"event-{ordinal}",
            "timestamp": f"2026-09-18T12:00:0{2 - ordinal}Z",
            "body": {"marker": contract.marker, "ordinal": ordinal},
            "resource": {"type": "function", "id": "function-id"},
            "level": "info",
        }
        for ordinal in range(3)
    ]
    contract.verify_events(events)
    with pytest.raises(AssertionError):
        contract.verify_events([events[0], events[0], events[2]])
    events[1] = {
        **events[1],
        "resource": {"type": "function", "id": "another-function"},
    }
    with pytest.raises(AssertionError):
        contract.verify_events(events)


def test_log_activity_contract_rejects_wrong_resource_counts() -> None:
    module = _load_module("logs_contract", ROOT / "features" / "logs_contract.py")
    contract = module.LogContract(
        SimpleNamespace(
            fixture={
                "api_url": "https://api.test",
                "anon_key": "anon",
                "logs_access_token": "project-token",
                "function_id": "function-id",
            }
        )
    )
    response = SimpleNamespace(
        total=1,
        data=[
            {
                "total": 1,
                "counts": {"resource_ids": {"function-id": 1}, "levels": {"info": 1}},
            },
            {"total": 0, "counts": {"resource_ids": {}, "levels": {}}},
        ],
    )
    contract.verify_activity(response)
    response.data[0]["counts"]["resource_ids"] = {"another-function": 1}
    with pytest.raises(AssertionError):
        contract.verify_activity(response)
