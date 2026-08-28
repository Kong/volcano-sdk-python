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
    "auth.feature": "0f251b2b39d66a1bf35043b25fd7d4cf750b3e1b2790911c7d26364f82852f9b",
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
        "a unique anonymous contract user",
        "a unique unconfirmed contract user",
        "an authenticated client",
        "exactly the fixture row is returned",
        "one client subscribes and the other publishes the contract message",
        "sign-up is acknowledged without a session",
        "the client converts the anonymous user with credentials",
        "the client deletes all current-user sessions",
        "the client deletes another current-user session",
        "the client is signed in as the confirmed contract user",
        "the client is signed in as the confirmed contract user on multiple sessions",
        "the client lists the current user's sessions",
        "the client refreshes the current session",
        "the client refreshes with an invalid refresh token",
        "the client retrieves the current user",
        "the client signs out",
        "the client signs up anonymously",
        "the client signs up with the new user's credentials",
        "the client subscribes to auth-state changes",
        "the client unsubscribes from auth-state changes",
        "the client updates the current user's metadata",
        "the converted user keeps the anonymous user identity",
        "the current session belongs to the anonymous user",
        "the SDK operation succeeds",
        "the SDK operation fails",
        "the client acquires and releases the contract lock",
        'the client selects the contract table where "slug" equals the fixture slug',
        "the client signs in with the contract user's credentials",
        "the client uploads and downloads the contract object",
        "the confirmed contract user",
        "the current session belongs to the contract user",
        "the current session exposes rotated access and refresh tokens",
        "the current session is empty",
        "the current session exposes access and refresh tokens",
        "the current user belongs to the contract user",
        "the current user contains the updated metadata",
        "the deleted session is absent from the session list",
        "the downloaded bytes equal the uploaded bytes",
        "the released lease is no longer held",
        "the listener immediately observes the current user",
        "the listener observes the signed-out state",
        "the listener receives no additional events",
        "the session list contains the current session",
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
