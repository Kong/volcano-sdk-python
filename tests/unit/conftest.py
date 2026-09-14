from __future__ import annotations

import pytest

from volcano_sdk import _function_resolution


@pytest.fixture(autouse=True)
def isolate_function_resolution_cache() -> None:
    """Function name resolutions are cached process-wide; keep tests independent."""
    _function_resolution.clear()
