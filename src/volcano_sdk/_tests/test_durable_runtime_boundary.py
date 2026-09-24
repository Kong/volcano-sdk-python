"""The optional runtime must provide every adapter dependency."""

from __future__ import annotations

import re
from types import ModuleType
from typing import TYPE_CHECKING

import pytest

from volcano_sdk._durable_modules import (
    load_config,
    load_retries,
    load_root,
    load_waits,
)

if TYPE_CHECKING:
    from collections.abc import Callable


@pytest.mark.parametrize(
    ("load", "message"),
    [
        (
            load_config,
            "aws_durable_execution_sdk_python.config does not provide ConfigModule",
        ),
        (
            load_retries,
            "aws_durable_execution_sdk_python.retries does not provide RetriesModule",
        ),
        (load_root, "aws_durable_execution_sdk_python does not provide RootModule"),
        (
            load_waits,
            "aws_durable_execution_sdk_python.waits does not provide WaitsModule",
        ),
    ],
)
def test_incomplete_runtime_module_is_rejected(
    load: Callable[[], object], message: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    def incomplete(name: str) -> ModuleType:
        return ModuleType(name)

    monkeypatch.setattr(
        "volcano_sdk._durable_modules.importlib.import_module", incomplete
    )

    with pytest.raises(TypeError, match=f"^{re.escape(message)}$"):
        _ = load()
