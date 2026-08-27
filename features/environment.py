from __future__ import annotations

import json
import os
import stat
from pathlib import Path
from typing import Any

from contract_support import ContractWorld

FIXTURE_MODE = 0o600
FIXTURE_ABSOLUTE_PATH_ERROR = "VOLCANO_SDK_CONTRACT_FIXTURE must be an absolute path"
FIXTURE_MODE_ERROR = "VOLCANO_SDK_CONTRACT_FIXTURE must have mode 0600"
FIXTURE_OBJECT_ERROR = "VOLCANO_SDK_CONTRACT_FIXTURE must contain a JSON object"
FIXTURE_REQUIRED_ERROR = "VOLCANO_SDK_CONTRACT_FIXTURE is required"


def load_fixture(path: Path) -> dict[str, Any]:
    if not path.is_absolute():
        raise ValueError(FIXTURE_ABSOLUTE_PATH_ERROR)
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode != FIXTURE_MODE:
        raise PermissionError(FIXTURE_MODE_ERROR)
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(FIXTURE_OBJECT_ERROR)
    return value


def before_all(context: Any) -> None:
    fixture_path = os.environ.get("VOLCANO_SDK_CONTRACT_FIXTURE")
    if fixture_path is None:
        raise RuntimeError(FIXTURE_REQUIRED_ERROR)
    context.contract_fixture = load_fixture(Path(fixture_path))


def before_scenario(context: Any, scenario: Any) -> None:
    del scenario
    context.contract = ContractWorld(context.contract_fixture)


def after_scenario(context: Any, scenario: Any) -> None:
    del scenario
    context.contract.cleanup()
