"""Mutation reports must separate useful kills from other outcomes."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import cast

import pytest

from scripts.mutation_results import main

PROJECT = Path(__file__).parents[2]


def test_scoped_mutation_excludes_prefix_sibling_module(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "src/volcano_sdk/durable.py"
    source.parent.mkdir(parents=True)
    _ = source.write_text("def durable() -> bool: return True\n", encoding="utf-8")
    sibling = source.with_name("durable_authoring.py")
    _ = sibling.write_text("def authoring() -> bool: return True\n", encoding="utf-8")
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    _ = (scripts / "mutation.sh").write_bytes(
        (PROJECT / "scripts/mutation.sh").read_bytes()
    )
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    stubs = {
        "git": """#!/bin/sh
case "$1" in
  merge-base) printf 'base\\n' ;;
  diff) printf 'src/volcano_sdk/durable.py\\0' ;;
esac
""",
        "mutmut": "#!/bin/sh\nprintf '%s\\n' \"$@\" > mutation-args.txt\n",
        "python": "#!/bin/sh\nexit 0\n",
    }
    for name, content in stubs.items():
        stub = bin_dir / name
        _ = stub.write_text(content, encoding="utf-8")
        stub.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:{os.environ['PATH']}")

    result = subprocess.run(
        ["/bin/bash", "scripts/mutation.sh"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    arguments = (tmp_path / "mutation-args.txt").read_text(encoding="utf-8")
    assert "volcano_sdk.durable.x*" in arguments.splitlines()
    assert "volcano_sdk.durable*" not in arguments.splitlines()


def fixture_report(tmp_path: Path, code: int | None) -> tuple[Path, Path]:
    """Write a single generated mutant and the shell target inputs.

    Returns:
        Target and harness-failure path files.

    """
    source = Path("src/volcano_sdk/probe.py")
    source.parent.mkdir(parents=True)
    _ = source.write_text("def probe() -> bool:\n    return True\n", encoding="utf-8")
    meta = Path("mutants/src/volcano_sdk/probe.py.meta")
    meta.parent.mkdir(parents=True)
    _ = meta.write_text(
        json.dumps({"exit_code_by_key": {"probe__mutmut_1": code}}),
        encoding="utf-8",
    )
    targets = tmp_path / "targets.bin"
    _ = targets.write_bytes(f"{source}\0".encode())
    failed = tmp_path / "failed.bin"
    _ = failed.write_bytes(b"")
    return targets, failed


@pytest.mark.parametrize(
    ("code", "outcome"),
    [
        (0, "survived"),
        (3, "crashed"),
        (5, "uncovered"),
        (36, "timed_out"),
        (None, "incomplete"),
    ],
)
def test_non_kills_fail_separately(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    code: int | None,
    outcome: str,
) -> None:
    monkeypatch.chdir(tmp_path)
    targets, failed = fixture_report(tmp_path, code)
    assert main(targets, failed) == 1
    report = cast(
        "object", json.loads(Path("reports/mutation.json").read_text(encoding="utf-8"))
    )
    assert isinstance(report, dict)
    assert report["outcomes"] == {outcome: 1}


def test_killed_mutant_passes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    targets, failed = fixture_report(tmp_path, 1)
    assert main(targets, failed) == 0


def test_statically_invalid_mutant_is_reported_separately(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    targets, failed = fixture_report(tmp_path, 37)

    assert main(targets, failed) == 0
    report = cast(
        "object", json.loads(Path("reports/mutation.json").read_text(encoding="utf-8"))
    )
    assert report == {
        "modules": ["src/volcano_sdk/probe.py"],
        "outcomes": {"type_checked": 1},
        "unmutatable_modules": [],
        "failures": [],
    }


def test_missing_mutation_report_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    targets, failed = fixture_report(tmp_path, 1)
    Path("mutants/src/volcano_sdk/probe.py.meta").unlink()
    assert main(targets, failed) == 1
    report = Path("reports/mutation.json").read_text(encoding="utf-8")
    assert "Missing mutmut report" in report


def test_harness_failure_does_not_pass(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    targets, failed = fixture_report(tmp_path, 1)
    _ = failed.write_bytes(b"src/volcano_sdk/probe.py\0")
    assert main(targets, failed) == 1
