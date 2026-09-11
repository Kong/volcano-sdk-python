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

import pytest
from behave.step_registry import registry

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
        (
            "one client pauses delivery for 1 second "
            "and then resumes with the same handler"
        ),
        "a service-role client",
        "a fresh client adopts the current session",
        "a fresh client tries to refresh the signed-out session",
        "an authenticated client",
        "exactly the deleted contract row is returned",
        "exactly the fixture row is returned",
        "exactly the inserted contract row is returned",
        "exactly the updated contract row is returned",
        "one client subscribes and the other publishes the contract message",
        "the auth-state listener observes the signed-in contract user",
        "the SDK operation succeeds",
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
