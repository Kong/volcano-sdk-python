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
        (("tool", "tox", "env", "package-types"), ("commands", list[list[str]]())),
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
        Path(".mypy.ini"),
        Path("setup.cfg"),
    ],
)
def test_excluded_new_source_or_nested_configuration_fails(path: Path) -> None:
    assert tracked_errors([path])


def test_unapproved_source_suppression_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    path = Path("scripts/probe.py")
    path.parent.mkdir(parents=True)
    path.write_text("def probe():\n    pass  # ruff: ignore[S603]\n", encoding="utf-8")
    assert source_suppressions(path) == [(2, "# ruff: ignore[S603]")]
    assert suppression_errors([path], []) == [
        "Undocumented suppression: scripts/probe.py: # ruff: ignore[S603]"
    ]


def test_unapproved_unit_test_suppression_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    path = Path("tests/unit/test_probe.py")
    path.parent.mkdir(parents=True)
    path.write_text("def probe():\n    pass  # noqa: S603\n", encoding="utf-8")
    assert suppression_errors([path], []) == [
        "Undocumented suppression: tests/unit/test_probe.py: # noqa: S603"
    ]


def test_deliberately_invalid_type_fixtures_are_separate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    path = Path("tests/unit/fixtures/invalid_arguments.py")
    path.parent.mkdir(parents=True)
    path.write_text(
        "def probe():\n    pass  # type: ignore[arg-type]\n", encoding="utf-8"
    )
    assert suppression_errors([path], []) == []

    unlisted = Path("tests/unit/fixtures/invalid_probe.py")
    unlisted.write_text("def probe():\n    pass  # noqa: S603\n", encoding="utf-8")
    assert suppression_errors([unlisted], []) == [
        "Undocumented suppression: tests/unit/fixtures/invalid_probe.py: # noqa: S603"
    ]


def test_approved_method_scope_does_not_authorize_another_class(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    path = Path("scripts/probe.py")
    path.parent.mkdir()
    path.write_text(
        "class A:\n    def run(self):\n        pass  # noqa: S603\n"
        "class B:\n    def run(self):\n        pass  # noqa: S603\n",
        encoding="utf-8",
    )
    record: object = {
        "scope": "scripts/probe.py:A.run",
        "rule": "S603",
        "rationale": "Verified tool limitation",
        "evidence": "Fixture",
        "approved_by": "reviewer",
        "approved_at": "2026-09-23",
        "approval_evidence": "Review",
    }
    assert suppression_errors([path], [record]) == [
        "Undocumented suppression: scripts/probe.py: # noqa: S603"
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
        (
            Path("tests/unit/test_probe.py"),
            "# mypy: disable-error-code=attr-defined\ndef probe(): pass\n",
            "# mypy: disable-error-code=attr-defined",
        ),
        (
            Path("tests/unit/test_probe.py"),
            "# pyright: basic\ndef probe(): pass\n",
            "# pyright: basic",
        ),
        (
            Path("tests/unit/test_probe.py"),
            "def probe():\n    pass  # pragma: no branch\n",
            "# pragma: no branch",
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
    path.parent.mkdir(parents=True)
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
