"""Negative fixtures for the repository quality-policy boundary."""

from __future__ import annotations

import copy
import tomllib
from pathlib import Path
from typing import cast

from scripts.check_quality_policy import check_comments, check_config, check_inventory

CONFIG = Path(__file__).parents[2] / "pyproject.toml"


def config_copy() -> dict[str, object]:
    """Load an independent copy of the maintained tool configuration.

    Returns:
        A mutable configuration tree.

    """
    return copy.deepcopy(cast("dict[str, object]", tomllib.loads(CONFIG.read_text())))


def test_lowered_coverage_threshold_fails() -> None:
    config = config_copy()
    tool = cast("dict[str, object]", config["tool"])
    coverage = cast("dict[str, object]", tool["coverage"])
    report = cast("dict[str, object]", coverage["report"])
    report["fail_under"] = 99

    assert "policy setting changed: coverage.report.fail_under" in check_config(config)


def test_removed_quality_check_fails() -> None:
    config = config_copy()
    tool = cast("dict[str, object]", config["tool"])
    poe = cast("dict[str, object]", tool["poe"])
    tasks = cast("dict[str, object]", poe["tasks"])
    checks = cast("list[str]", tasks["checks"])
    tasks["checks"] = [check for check in checks if check != "coverage"]

    assert "policy setting changed: poe.tasks.checks" in check_config(config)


def test_extra_coverage_exclusion_fails() -> None:
    config = config_copy()
    tool = cast("dict[str, object]", config["tool"])
    coverage = cast("dict[str, object]", tool["coverage"])
    report = cast("dict[str, object]", coverage["report"])
    report["exclude_also"] = ["def untested"]

    assert "Additional type or coverage exclusions" in check_config(config)


def test_nested_config_fails(tmp_path: Path) -> None:
    nested = "tests/unit/pytest.toml"
    assert f"nested tool configuration: {nested}" in check_inventory(
        tmp_path, {nested}, set()
    )


def test_unlinted_new_runtime_file_fails(tmp_path: Path) -> None:
    name = "src/volcano_sdk/new_module.py"
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    source.write_text("def untested():\n    return True\n", encoding="utf-8")

    assert f"Ruff omitted tracked Python file: {name}" in check_inventory(
        tmp_path, {name}, set()
    )


def test_unlinted_new_typing_stub_fails(tmp_path: Path) -> None:
    name = "typings/external/new_module.pyi"
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    source.write_text("def call() -> bool: ...\n", encoding="utf-8")

    assert f"Ruff omitted tracked Python file: {name}" in check_inventory(
        tmp_path, {name}, set()
    )


def test_unapproved_suppression_fails(tmp_path: Path) -> None:
    name = "src/volcano_sdk/new_module.py"
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    source.write_text(
        "def unsafe():\n    return True  # ruff: ignore[S603]\n",
        encoding="utf-8",
    )

    assert any(
        "unapproved S603" in item for item in check_comments(tmp_path, {name}, [])
    )


def test_type_ignore_outside_diagnostic_fixture_fails(tmp_path: Path) -> None:
    name = "tests/unit/test_new_behavior.py"
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    source.write_text("value: str = 1  # type: ignore[assignment]\n", encoding="utf-8")

    assert any(
        "type ignore outside diagnostic fixture" in item
        for item in check_comments(tmp_path, {name}, [])
    )


def test_type_fixture_cannot_hide_non_type_suppression(tmp_path: Path) -> None:
    name = "tests/unit/fixtures/invalid_arguments.py"
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    source.write_text("value = 1  # noqa: S101\n", encoding="utf-8")

    assert any(
        "forbidden suppression" in item for item in check_comments(tmp_path, {name}, [])
    )


def test_unused_exception_fails(tmp_path: Path) -> None:
    exception = {
        "scope": "scripts/generate_openapi.py:generate",
        "rule": "S603",
        "rationale": "Reviewed fixed command",
        "evidence": "Exact command",
        "approved_by": "reviewer",
        "approved_at": "2026-09-23",
        "approval_evidence": "PR review",
    }

    assert (
        "unused exception: scripts/generate_openapi.py:generate S603"
        in check_comments(tmp_path, set(), [exception])
    )


def test_duplicate_exception_fails(tmp_path: Path) -> None:
    exception = {
        "scope": "scripts/generate_openapi.py:generate",
        "rule": "S603",
        "rationale": "Reviewed fixed command",
        "evidence": "Exact command",
        "approved_by": "reviewer",
        "approved_at": "2026-09-23",
        "approval_evidence": "PR review",
    }

    assert "duplicate quality exception record" in check_comments(
        tmp_path, set(), [exception, exception]
    )
