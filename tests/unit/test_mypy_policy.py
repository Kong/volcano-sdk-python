from __future__ import annotations

from pathlib import Path

import pytest
from mypy import api

CONFIG = Path(__file__).parents[2] / "pyproject.toml"


def check_types(tmp_path: Path, source: str) -> tuple[str, str, int]:
    fixture = tmp_path / "fixture.py"
    _ = fixture.write_text(source)
    return api.run(["--config-file", str(CONFIG), "--no-incremental", str(fixture)])


def test_typed_program_passes(tmp_path: Path) -> None:
    output, errors, status = check_types(
        tmp_path,
        "def echo(value: str) -> str:\n    return value\n",
    )
    assert status == 0, output + errors


@pytest.mark.parametrize(
    ("source", "diagnostic"),
    [
        ("from typing import Any\nvalue: Any = 1\n", "explicit-any"),
        (
            "def unreachable() -> None:\n    return\n    print('dead code')\n",
            "unreachable",
        ),
        (
            (
                "from asyncio import Future\n"
                "def future() -> Future[None]:\n    return Future()\n"
                "def abandoned() -> None:\n    future()\n"
            ),
            "unused-awaitable",
        ),
        (
            "value: str = 1  # type: ignore\n",
            "ignore-without-code",
        ),
        (
            "value: str = 'ok'  # type: ignore[assignment]\n",
            "unused-ignore",
        ),
        (
            (
                "from _volcano_missing_module import Missing  "
                "# type: ignore[import-not-found]\n"
                "def unchecked(value: Missing) -> None:\n    pass\n"
            ),
            "no-any-unimported",
        ),
    ],
)
def test_unsafe_program_fails(
    tmp_path: Path,
    source: str,
    diagnostic: str,
) -> None:
    output, errors, status = check_types(tmp_path, source)
    assert status == 1, output + errors
    assert f"[{diagnostic}]" in output
