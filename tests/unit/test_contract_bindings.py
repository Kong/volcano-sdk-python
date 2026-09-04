from __future__ import annotations

import hashlib
import importlib.util
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from behave.step_registry import registry

if TYPE_CHECKING:
    from types import ModuleType

ROOT = Path(__file__).parents[2]
FEATURE_SHA256 = {
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
