"""Negative fixtures for the native quality configuration attestation."""

from __future__ import annotations

import copy
import json
import tomllib
from pathlib import Path
from typing import cast

import pytest

from scripts.check_quality_policy import (
    check_comments,
    check_config,
    check_inventory,
    check_lock_bytes,
)

ROOT = Path(__file__).parents[2]


def config_copy() -> dict[str, object]:
    """Load a mutable copy of native tool settings.

    Returns:
        A complete pyproject configuration tree.

    """
    return copy.deepcopy(
        cast("dict[str, object]", tomllib.loads((ROOT / "pyproject.toml").read_text()))
    )


def locked_config() -> dict[str, object]:
    """Load the separately pinned native-tool snapshot.

    Returns:
        The recorded configuration tree.

    """
    return cast(
        "dict[str, object]",
        json.loads((ROOT / "maintainers/quality-policy.lock.json").read_text()),
    )


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        (("coverage", "report", "fail_under"), 99),
        (("coverage", "report", "exclude_lines"), [".*"]),
        (("coverage", "report", "exclude_also"), ["def untested"]),
        (("mypy", "ignore_errors"), True),
        (("basedpyright", "reportAny"), False),
        (("basedpyright", "executionEnvironments"), []),
        (("ruff", "lint", "ignore"), ["ALL"]),
        (("ruff", "lint", "extend-ignore"), ["F821"]),
        (("ruff", "lint", "extend-per-file-ignores"), {"**/*.py": ["ALL"]}),
        (("pytest", "ini_options", "filterwarnings"), ["ignore"]),
        (("poe", "tasks", "checks"), ["policy"]),
        (("poe", "tasks", "coverage"), "true"),
    ],
)
def test_native_guardrail_change_fails(
    path: tuple[str, ...], replacement: object
) -> None:
    config = config_copy()
    section = cast("dict[str, object]", config["tool"])
    for key in path[:-1]:
        section = cast("dict[str, object]", section[key])
    section[path[-1]] = replacement

    assert f"tool.{'.'.join(path)}" in check_config(config, locked_config())


def test_lock_change_requires_reviewed_digest() -> None:
    data = (ROOT / "maintainers/quality-policy.lock.json").read_bytes()

    assert check_lock_bytes(data) == []
    assert check_lock_bytes(data + b" ") == ["quality policy lock digest changed"]


def test_nested_config_fails(tmp_path: Path) -> None:
    name = "tests/unit/pytest.toml"

    assert f"nested tool configuration: {name}" in check_inventory(
        tmp_path, {name}, set()
    )


@pytest.mark.parametrize(
    "name", ["src/volcano_sdk/new_module.py", "typings/external/new_module.pyi"]
)
def test_unlinted_python_file_fails(tmp_path: Path, name: str) -> None:
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    source.write_text("def untested() -> bool: return True\n", encoding="utf-8")

    assert f"Ruff omitted tracked Python file: {name}" in check_inventory(
        tmp_path, {name}, set()
    )


def test_unapproved_ruff_suppression_fails(tmp_path: Path) -> None:
    name = "src/volcano_sdk/new_module.py"
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    source.write_text(
        "def unsafe():\n    return True  # ruff: ignore[S603]\n", encoding="utf-8"
    )

    assert any(
        "unapproved S603" in error for error in check_comments(tmp_path, {name}, [])
    )


def test_type_ignore_outside_diagnostic_fixture_fails(tmp_path: Path) -> None:
    name = "tests/unit/test_new_behavior.py"
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    source.write_text("value: str = 1  # type: ignore[assignment]\n", encoding="utf-8")

    assert any(
        "type ignore outside diagnostic fixture" in error
        for error in check_comments(tmp_path, {name}, [])
    )


def test_type_fixture_cannot_hide_other_suppression(tmp_path: Path) -> None:
    name = "tests/unit/fixtures/invalid_arguments.py"
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    source.write_text("value = 1  # noqa: S101\n", encoding="utf-8")

    assert any(
        "forbidden suppression" in error
        for error in check_comments(tmp_path, {name}, [])
    )


def test_self_authorized_exception_fails(tmp_path: Path) -> None:
    exception = {
        "scope": "src/volcano_sdk/auth.py:login",
        "rule": "S603",
        "rationale": "self-authorized",
        "evidence": "none",
        "approved_by": "self",
        "approved_at": "2026-09-23",
        "approval_evidence": "none",
    }

    assert "unapproved quality exception record" in check_comments(
        tmp_path, set(), [exception]
    )


def test_unused_reviewed_exception_fails(tmp_path: Path) -> None:
    assert (
        "unused exception: scripts/generate_openapi.py:generate S603"
        in check_comments(tmp_path, set(), [])
    )
