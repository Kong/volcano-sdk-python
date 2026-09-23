from __future__ import annotations

import json
import os
import stat
from pathlib import Path
from typing import TYPE_CHECKING, cast

from contract_fixture import ContractFixture, is_contract_fixture
from contract_support import ContractWorld

if TYPE_CHECKING:
    from behave.runner import Context

FIXTURE_MODE = 0o600
FIXTURE_ABSOLUTE_PATH_ERROR = "VOLCANO_SDK_CONTRACT_FIXTURE must be an absolute path"
FIXTURE_MODE_ERROR = "VOLCANO_SDK_CONTRACT_FIXTURE must have mode 0600"
FIXTURE_SHAPE_ERROR = (
    "VOLCANO_SDK_CONTRACT_FIXTURE must contain a complete contract fixture"
)
FIXTURE_REQUIRED_ERROR = "VOLCANO_SDK_CONTRACT_FIXTURE is required"


def load_fixture(path: Path) -> ContractFixture:
    if not path.is_absolute():
        raise ValueError(FIXTURE_ABSOLUTE_PATH_ERROR)
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode != FIXTURE_MODE:
        raise PermissionError(FIXTURE_MODE_ERROR)
    value = cast("object", json.loads(path.read_text(encoding="utf-8")))
    if not is_contract_fixture(value):
        raise TypeError(FIXTURE_SHAPE_ERROR)
    return value


def before_all(context: Context) -> None:
    fixture_path = os.environ.get("VOLCANO_SDK_CONTRACT_FIXTURE")
    if fixture_path is None:
        raise RuntimeError(FIXTURE_REQUIRED_ERROR)
    context.contract_fixture = load_fixture(Path(fixture_path))


def before_scenario(context: Context, scenario: object) -> None:
    del scenario
    fixture = cast("object", context.contract_fixture)
    if not is_contract_fixture(fixture):
        raise TypeError(FIXTURE_SHAPE_ERROR)
    context.contract = ContractWorld(fixture)


def after_scenario(context: Context, scenario: object) -> None:
    del scenario
    world = cast("object", context.contract)
    assert isinstance(world, ContractWorld)
    world.cleanup()
