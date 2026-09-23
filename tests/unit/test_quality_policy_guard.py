"""Prove that quality-policy changes fail the local gate."""

from __future__ import annotations

import copy
import tomllib
from pathlib import Path
from typing import cast

import pytest

from scripts.check_quality_policy import (
    configuration_errors,
    source_suppressions,
    suppression_errors,
    table,
    tracked_errors,
)

PROJECT = Path(__file__).parents[2] / "pyproject.toml"


def configuration() -> dict[str, object]:
    """Load the real native-tool configuration.

    Returns:
        A mutable copy for negative probes.

    """
    value = cast("object", tomllib.loads(PROJECT.read_text(encoding="utf-8")))
    return copy.deepcopy(table(value))


def test_current_policy_passes() -> None:
    assert configuration_errors(configuration()) == []


@pytest.mark.parametrize(
    ("path", "weakened"),
    [
        (("tool", "coverage", "report"), ("fail_under", 99)),
        (("tool", "coverage", "report"), ("exclude_lines", [".*"])),
        (("tool", "coverage", "run"), ("omit", ["src/volcano_sdk/*"])),
        (
            ("tool", "ruff"),
            (
                "extend-exclude",
                ["src/volcano_sdk/_generated", "src/volcano_sdk/new.py"],
            ),
        ),
        (("tool", "ruff", "lint", "mccabe"), ("max-complexity", 6)),
        (("tool", "mutmut"), ("only_mutate", ["src/volcano_sdk/locks.py"])),
        (("tool", "poe", "tasks"), ("quality", ["checks"])),
    ],
)
def test_weakened_native_settings_fail(
    path: tuple[str, ...], weakened: tuple[str, object]
) -> None:
    current = configuration()
    node = current
    for key in path:
        node = table(node[key])
    node[weakened[0]] = weakened[1]
    assert configuration_errors(current)


@pytest.mark.parametrize(
    "path",
    [
        Path("outside/new.py"),
        Path("outside/new.pyi"),
        Path("src/other/new.py"),
        Path("src/volcano_sdk/pyproject.toml"),
    ],
)
def test_excluded_new_source_or_nested_configuration_fails(path: Path) -> None:
    assert tracked_errors([path])


def test_unapproved_source_suppression_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    path = Path("scripts/probe.py")
    path.parent.mkdir()
    path.write_text("def probe():\n    pass  # ruff: ignore[S603]\n", encoding="utf-8")
    assert source_suppressions(path) == [(2, "# ruff: ignore[S603]")]
    assert suppression_errors([path], []) == [
        "Undocumented suppression: scripts/probe.py: # ruff: ignore[S603]"
    ]


def test_unused_exception_fails() -> None:
    record: object = {
        "scope": "scripts/probe.py:probe",
        "rule": "S603",
        "rationale": "Fixed command",
        "evidence": "Probe",
        "approved_by": "reviewer",
        "approved_at": "2026-09-23",
        "approval_evidence": "Review",
    }
    assert suppression_errors([], [record]) == [
        "Unused or duplicated quality exception: scripts/probe.py:probe:S603"
    ]


def test_exception_without_approval_evidence_fails() -> None:
    record: object = {"scope": "scripts/probe.py:probe", "rule": "S603"}
    with pytest.raises(TypeError, match="approval evidence"):
        suppression_errors([], [record])
