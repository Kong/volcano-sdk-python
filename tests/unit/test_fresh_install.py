"""The fresh-install check must report drift and reject untested resolutions."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.dependency_drift import main

PROJECT = Path(__file__).parents[2]
LOCK = """
version = 1

[[package]]
name = "attrs"
version = "26.1.0"

[[package]]
name = "centrifuge-python"
version = "0.6.0"

[[package]]
name = "volcano-sdk-python"
version = "0.15.1"
source = { editable = "." }

[package.metadata]
requires-dist = [
    { name = "attrs", specifier = ">=26.1.0" },
    { name = "centrifuge-python", specifier = "==0.6.0" },
]
"""


@pytest.fixture
def summary(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(path))
    return path


def run_report(tmp_path: Path, resolved: str, tested: str) -> int:
    lock = tmp_path / "uv.lock"
    _ = lock.write_text(LOCK, encoding="utf-8")
    resolved_path = tmp_path / "resolved.txt"
    _ = resolved_path.write_text(resolved, encoding="utf-8")
    tested_path = tmp_path / "tested.txt"
    _ = tested_path.write_text(tested, encoding="utf-8")
    return main(lock, resolved_path, tested_path)


def test_drift_is_reported_without_failing(
    tmp_path: Path, summary: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    resolved = "attrs==26.2.0\ncentrifuge_python==0.6.0\nwebsockets==17.3\n"

    status = run_report(tmp_path, resolved, f"{resolved}pytest==9.1.1\n")

    output = capsys.readouterr().out
    assert status == 0
    assert "| attrs | 26.1.0 | 26.2.0 (drift) |" in output
    assert "| centrifuge-python | 0.6.0 | 0.6.0 |" in output
    assert "| websockets | not locked | 17.3 (drift) |" in output
    assert "pytest" not in output
    assert (
        "::warning title=Dependency drift::attrs: uv.lock has 26.1.0; "
        "a fresh install resolves 26.2.0"
    ) in output
    assert "| attrs | 26.1.0 | 26.2.0 (drift) |" in summary.read_text(encoding="utf-8")


@pytest.mark.usefixtures("summary")
def test_exact_pin_must_resolve_to_its_version(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    resolved = "attrs==26.1.0\ncentrifuge-python==0.6.1\n"

    assert run_report(tmp_path, resolved, resolved) == 1
    assert "centrifuge-python==0.6.0 resolved to 0.6.1" in capsys.readouterr().err


@pytest.mark.usefixtures("summary")
def test_test_tooling_must_not_change_runtime_packages(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    status = run_report(
        tmp_path,
        "attrs==26.2.0\ncentrifuge-python==0.6.0\n",
        "attrs==26.1.0\n",
    )

    assert status == 1
    errors = capsys.readouterr().err
    assert "test tooling changed attrs from 26.2.0 to 26.1.0" in errors
    assert "test tooling changed centrifuge-python from 0.6.0 to nothing" in errors


@pytest.mark.usefixtures("summary")
def test_unpinned_freeze_entries_are_rejected(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Unexpected freeze entry: attrs @ file"):
        _ = run_report(tmp_path, "attrs @ file:///attrs.whl\n", "")


@pytest.fixture
def origin_check(
    pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch
) -> pytest.Pytester:
    monkeypatch.setenv("PYTHONPATH", str(PROJECT / "tests/package"))
    return pytester


def sdk_test(location: str) -> str:
    return (
        "import sys, sysconfig, types\n"
        "from pathlib import Path\n"
        "def test_imports_sdk():\n"
        "    for name in ('volcano_sdk', 'volcano_sdk._tests.helper'):\n"
        "        module = types.ModuleType(name)\n"
        f"        module.__file__ = str(Path({location}) / name / '__init__.py')\n"
        "        sys.modules[name] = module\n"
    )


def test_installed_sdk_passes_origin_check(origin_check: pytest.Pytester) -> None:
    _ = origin_check.makepyfile(sdk_test("sysconfig.get_path('purelib')"))

    result = origin_check.runpytest_subprocess("-p", "installed_sdk")

    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.OK
    result.stdout.fnmatch_lines(["SDK imported from *volcano_sdk"])


def test_source_tree_sdk_fails_origin_check(origin_check: pytest.Pytester) -> None:
    _ = origin_check.makepyfile(sdk_test("'src'"))

    result = origin_check.runpytest_subprocess("-p", "installed_sdk")

    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    result.stdout.fnmatch_lines(
        ["*SDK not from the installed wheel: volcano_sdk imported from *src*"]
    )
    result.stdout.no_fnmatch_line("*volcano_sdk._tests*")


def test_run_without_the_sdk_fails_origin_check(
    origin_check: pytest.Pytester,
) -> None:
    _ = origin_check.makepyfile("def test_unrelated(): assert True")

    result = origin_check.runpytest_subprocess("-p", "installed_sdk")

    assert result.ret == pytest.ExitCode.TESTS_FAILED
    result.stdout.fnmatch_lines(
        ["*SDK not from the installed wheel: volcano_sdk was not imported*"]
    )
