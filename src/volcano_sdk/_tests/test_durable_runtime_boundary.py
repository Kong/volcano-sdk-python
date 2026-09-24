"""The optional runtime must provide every adapter dependency."""

from __future__ import annotations

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


@pytest.mark.parametrize("load", [load_config, load_retries, load_root, load_waits])
def test_incomplete_runtime_module_is_rejected(
    load: Callable[[], object], monkeypatch: pytest.MonkeyPatch
) -> None:
    def incomplete(name: str) -> ModuleType:
        return ModuleType(name)

    monkeypatch.setattr(
        "volcano_sdk._durable_modules.importlib.import_module", incomplete
    )

    with pytest.raises(TypeError, match="does not provide"):
        _ = load()
