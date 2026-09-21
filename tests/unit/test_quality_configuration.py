"""Exercise native quality tools against deliberately invalid source."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

PROJECT = Path(__file__).parents[2] / "pyproject.toml"


@pytest.fixture
def configured(pytester: pytest.Pytester) -> pytest.Pytester:
    pytester.makepyprojecttoml(PROJECT.read_text())
    return pytester


def test_native_pytest_accepts_complete_run(configured: pytest.Pytester) -> None:
    configured.makepyfile("def test_valid(): assert 1 + 1 == 2")
    result = configured.runpytest_subprocess()
    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.OK


@pytest.mark.parametrize(
    ("source", "diagnostic"),
    [
        (
            "import pytest\n@pytest.mark.unknown\ndef test_invalid(): pass",
            "*'unknown' not found in*markers*",
        ),
        (
            (
                "import pytest\n@pytest.mark.parametrize('value', [1, 1])\n"
                "def test_invalid(value): assert value == 1"
            ),
            "*Duplicate parametrization IDs*",
        ),
        (
            (
                "import pytest\n@pytest.mark.parametrize('value', [])\n"
                "def test_invalid(value): assert value == 1"
            ),
            "*Empty parameter set*",
        ),
    ],
)
def test_native_pytest_rejects_invalid_collection(
    configured: pytest.Pytester, source: str, diagnostic: str
) -> None:
    configured.makepyfile(source)
    result = configured.runpytest_subprocess()
    result.assert_outcomes(errors=1)
    assert result.ret == pytest.ExitCode.INTERRUPTED
    result.stdout.fnmatch_lines([diagnostic])


def test_native_pytest_rejects_unknown_configuration(
    configured: pytest.Pytester,
) -> None:
    configured.makepyprojecttoml(
        PROJECT.read_text().replace(
            "[tool.pytest.ini_options]",
            "[tool.pytest.ini_options]\nunknown_quality_option = true",
        ),
    )
    configured.makepyfile("def test_valid(): assert True")
    result = configured.runpytest_subprocess()
    assert result.ret == pytest.ExitCode.USAGE_ERROR
    result.stderr.fnmatch_lines(["*Unknown config option: unknown_quality_option*"])


def test_native_pytest_rejects_unexpected_xfail_pass(
    configured: pytest.Pytester,
) -> None:
    configured.makepyfile(
        "import pytest\n@pytest.mark.xfail(reason='invalid fixture')\n"
        "def test_unexpected(): assert True",
    )
    result = configured.runpytest_subprocess()
    result.assert_outcomes(failed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    result.stdout.fnmatch_lines(["*XPASS(strict)*"])


def test_ruff_rejects_excessive_complexity_with_project_configuration() -> None:
    source = """def choose(value: int) -> int:
    if value == 0:
        return 0
    if value == 1:
        return 1
    if value == 2:
        return 2
    if value == 3:
        return 3
    if value == 4:
        return 4
    if value == 5:
        return 5
    return 6
"""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ruff",
            "check",
            "--output-format",
            "concise",
            "--stdin-filename",
            "src/volcano_sdk/_quality_probe.py",
            "-",
        ],
        input=source,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert "C901 `choose` is too complex (7 > 5)" in result.stdout
