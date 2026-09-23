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
        (("tool", "poe", "tasks"), ("types", ["mypy"])),
        (("tool", "mypy"), ("strict", False)),
        (("tool", "basedpyright"), ("typeCheckingMode", "basic")),
        (("tool", "ruff", "lint"), ("ignore", ["ALL"])),
        (
            ("tool", "ruff", "lint"),
            ("per-file-ignores", {"src/volcano_sdk/*.py": ["ALL"]}),
        ),
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


@pytest.mark.parametrize(
    ("directive", "rule"),
    [
        ("# type: ignore[return-value]", "return-value"),
        ("# pyright: ignore[reportPrivateUsage]", "reportPrivateUsage"),
    ],
)
def test_approved_native_type_suppressions_are_recognized(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    directive: str,
    rule: str,
) -> None:
    monkeypatch.chdir(tmp_path)
    path = Path("scripts/probe.py")
    path.parent.mkdir()
    path.write_text(f"def probe():\n    pass  {directive}\n", encoding="utf-8")
    record: object = {
        "scope": "scripts/probe.py:probe",
        "rule": rule,
        "rationale": "Verified tool limitation",
        "evidence": "Fixture",
        "approved_by": "reviewer",
        "approved_at": "2026-09-23",
        "approval_evidence": "Review",
    }
    assert suppression_errors([path], [record]) == []


@pytest.mark.parametrize(
    ("path", "source", "directive"),
    [
        (
            Path("typings/probe.pyi"),
            "def probe() -> int: ...  # type: ignore[return-value]\n",
            "# type: ignore[return-value]",
        ),
        (
            Path("scripts/probe.py"),
            "# ruff: noqa: D100, F401\ndef probe(): pass\n",
            "# ruff: noqa: D100, F401",
        ),
    ],
)
def test_stub_and_file_level_suppressions_need_approval(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    path: Path,
    source: str,
    directive: str,
) -> None:
    monkeypatch.chdir(tmp_path)
    path.parent.mkdir()
    path.write_text(source, encoding="utf-8")
    assert suppression_errors([path], []) == [
        f"Undocumented suppression: {path}: {directive}"
    ]


def test_deleted_worktree_source_is_skipped(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    assert suppression_errors([Path("src/volcano_sdk/deleted.py")], []) == []


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
