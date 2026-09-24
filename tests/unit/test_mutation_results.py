"""Mutation reports must separate useful kills from other outcomes."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import cast

import pytest
from mutmut.utils.format_utils import get_mutant_name

from scripts.mutation_results import main

PROJECT = Path(__file__).parents[2]


def mutation_harness(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, modules: list[str]
) -> None:
    """Install shell stubs for testing the native Mutmut selector."""
    for module in modules:
        source = tmp_path / module
        source.parent.mkdir(parents=True, exist_ok=True)
        _ = source.write_text("def probe() -> bool: return True\n", encoding="utf-8")
    _ = (tmp_path / "git-paths.bin").write_bytes(
        b"\0".join(module.encode() for module in modules) + b"\0"
    )
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    _ = (scripts / "mutation.sh").write_bytes(
        (PROJECT / "scripts/mutation.sh").read_bytes()
    )
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    stubs = {
        "git": (
            "#!/bin/sh\n"
            '[ "$*" = \'ls-files --cached --others --exclude-standard '
            "-z -- src/volcano_sdk' ] || exit 1\n"
            "cat git-paths.bin\n"
        ),
        "mutmut": "#!/bin/sh\nprintf '%s\\n' \"$@\" > mutation-args.txt\n",
        "python": "#!/bin/sh\nexit 0\n",
    }
    for name, content in stubs.items():
        stub = bin_dir / name
        _ = stub.write_text(content, encoding="utf-8")
        stub.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:{os.environ['PATH']}")


def run_mutation_script(tmp_path: Path) -> subprocess.CompletedProcess[str]:
    """Run the mutation orchestrator against the shell stubs.

    Returns:
        Completed script process.

    """
    return subprocess.run(
        ["/bin/bash", "scripts/mutation.sh"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )


def run_mutation_matrix(tmp_path: Path) -> subprocess.CompletedProcess[str]:
    """Read the complete CI module plan.

    Returns:
        Completed script process.

    """
    return subprocess.run(
        ["/bin/bash", "scripts/mutation.sh", "--matrix"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )


def mutant_pattern(module: str) -> str:
    """Mirror Mutmut's package-init name normalization.

    Returns:
        Exact function-prefix selector for the module.

    """
    name = module.removeprefix("src/").removesuffix(".py")
    return f"{name.removesuffix('/__init__').replace('/', '.')}.x*"


def module_name(path: str) -> str:
    """Return the Python module selected by the native Mutmut wildcard.

    Returns:
        Import name for a handwritten Python source file.

    """
    return mutant_pattern(path).removesuffix(".x*")


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("src/volcano_sdk/__init__.py", "volcano_sdk.x_probe__mutmut_1"),
        ("src/volcano_sdk/nested/__init__.py", "volcano_sdk.nested.x_probe__mutmut_1"),
    ],
)
def test_package_init_selector_matches_native_mutmut_name(
    path: str, expected: str
) -> None:
    assert get_mutant_name(Path(path), "x_probe__mutmut_1") == expected
    assert expected.startswith(mutant_pattern(path).removesuffix("*"))


def test_mutation_matrix_covers_all_handwritten_modules(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    modules = [f"src/volcano_sdk/module_{index}.py" for index in range(8)]
    modules.extend(
        [
            "src/volcano_sdk/__init__.py",
            "src/volcano_sdk/durable.py",
            "src/volcano_sdk/durable_authoring.py",
            "src/volcano_sdk/nested/cache.py",
            "src/volcano_sdk/nested/__init__.py",
        ]
    )
    generated = "src/volcano_sdk/_generated/wire.py"
    mutation_harness(tmp_path, monkeypatch, [*modules, generated])

    plan = run_mutation_matrix(tmp_path)
    assert plan.returncode == 0, plan.stderr
    assert json.loads(plan.stdout) == [module_name(path) for path in modules]

    selected: list[str] = []
    selected_patterns: list[str] = []
    for module in json.loads(plan.stdout):
        monkeypatch.setenv("MUTATION_MODULE", module)
        result = run_mutation_script(tmp_path)
        assert result.returncode == 0, result.stderr
        paths = (tmp_path / "reports/mutation-targets.bin").read_bytes().split(b"\0")
        selected_modules = [os.fsdecode(path) for path in paths if path]
        assert len(selected_modules) == 1
        selected.extend(selected_modules)
        patterns = [mutant_pattern(path) for path in selected_modules]
        selected_patterns.extend(patterns)
        arguments = (tmp_path / "mutation-args.txt").read_text(encoding="utf-8")
        assert arguments.splitlines() == ["run", "--max-children", "1", *patterns]

    assert sorted(selected) == sorted(modules)
    assert len(selected) == len(set(selected))
    assert "volcano_sdk.durable.x*" in selected_patterns
    assert "volcano_sdk.durable*" not in selected_patterns
    assert "volcano_sdk.nested.x*" in selected_patterns
    assert "volcano_sdk.x*" in selected_patterns


def test_empty_mutation_inventory_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    mutation_harness(tmp_path, monkeypatch, [])
    result = run_mutation_matrix(tmp_path)
    assert result.returncode == 1
    assert "No handwritten SDK runtime modules found" in result.stderr


def test_duplicate_import_name_fails_inventory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    mutation_harness(
        tmp_path,
        monkeypatch,
        ["src/volcano_sdk/nested.py", "src/volcano_sdk/nested/__init__.py"],
    )
    result = run_mutation_matrix(tmp_path)
    assert result.returncode == 1
    assert "Duplicate Python runtime module" in result.stderr


@pytest.mark.parametrize("module", ["volcano_sdk.missing", "-1", "not-a-module"])
def test_invalid_mutation_module_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, module: str
) -> None:
    mutation_harness(tmp_path, monkeypatch, ["src/volcano_sdk/probe.py"])
    monkeypatch.setenv("MUTATION_MODULE", module)
    result = run_mutation_script(tmp_path)
    assert result.returncode == 2
    assert "Unknown mutation module" in result.stderr


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


def test_functionless_package_init_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    source = Path("src/volcano_sdk/__init__.py")
    source.parent.mkdir(parents=True)
    _ = source.write_text('"""Public package exports."""\n', encoding="utf-8")
    targets = tmp_path / "targets.bin"
    _ = targets.write_bytes(f"{source}\0".encode())
    failed = tmp_path / "failed.bin"
    _ = failed.write_bytes(b"")
    assert main(targets, failed) == 0
    report = cast(
        "object", json.loads(Path("reports/mutation.json").read_text(encoding="utf-8"))
    )
    assert isinstance(report, dict)
    assert report["unmutatable_modules"] == [str(source)]


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
