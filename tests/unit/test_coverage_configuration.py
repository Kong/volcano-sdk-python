from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from coverage import Coverage

if TYPE_CHECKING:
    from collections.abc import Sequence

PROJECT = Path(__file__).parents[2] / "pyproject.toml"
SOURCE = """\
def absolute(value):
    if value < 0:
        value = -value
    return value
"""
COMPLETE_TEST = """\
from volcano_sdk import absolute

def test_absolute():
    assert absolute(-1) == 1
    assert absolute(1) == 1
"""


@pytest.fixture
def coverage_project(pytester: pytest.Pytester) -> pytest.Pytester:
    _ = pytester.makepyprojecttoml(PROJECT.read_text())
    (pytester.path / "tests/unit").mkdir(parents=True)
    package = pytester.path / "src" / "volcano_sdk"
    package.mkdir(parents=True)
    _ = (package / "__init__.py").write_text(SOURCE)
    _ = (pytester.path / "tests/unit/test_fixture.py").write_text(COMPLETE_TEST)
    return pytester


def run_coverage(project: pytest.Pytester) -> pytest.RunResult:
    return project.runpytest_subprocess(
        "--cov",
        "--cov-config=pyproject.toml",
        "--cov-report=term-missing",
        "-o",
        "pythonpath=src",
    )


def test_coverage_threshold_requires_complete_coverage() -> None:
    configured = Coverage(config_file=str(PROJECT))
    assert configured.get_option("report:fail_under") == 100


def test_native_coverage_accepts_complete_runtime_coverage(
    coverage_project: pytest.Pytester,
) -> None:
    result = run_coverage(coverage_project)
    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.OK


@pytest.mark.parametrize("pragma", ["", "  # pragma: no branch"])
def test_native_coverage_requires_both_branch_outcomes(
    coverage_project: pytest.Pytester, pragma: str
) -> None:
    package = coverage_project.path / "src" / "volcano_sdk"
    _ = (package / "__init__.py").write_text(
        SOURCE.replace("if value < 0:", f"if value < 0:{pragma}")
    )
    _ = (coverage_project.path / "tests/unit/test_fixture.py").write_text(
        COMPLETE_TEST.replace("    assert absolute(1) == 1\n", "")
    )

    result = run_coverage(coverage_project)

    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    result.stdout.fnmatch_lines(["*FAIL*Required test coverage of 100.0% not reached*"])


@pytest.mark.parametrize("parts", [("unimported.py",), ("nested", "unimported.py")])
@pytest.mark.parametrize("pragma", ["", "  # pragma: no cover"])
def test_native_coverage_discovers_unimported_runtime_files(
    coverage_project: pytest.Pytester, parts: Sequence[str], pragma: str
) -> None:
    unimported = coverage_project.path.joinpath("src", "volcano_sdk", *parts)
    unimported.parent.mkdir(parents=True, exist_ok=True)
    _ = unimported.write_text(f"def uncovered():{pragma}\n    return 1\n")

    result = run_coverage(coverage_project)

    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    result.stdout.fnmatch_lines(
        ["*unimported.py*0%*", "*FAIL*Required test coverage of 100.0% not reached*"]
    )


def test_generated_code_does_not_count_as_handwritten_runtime(
    coverage_project: pytest.Pytester,
) -> None:
    generated = coverage_project.path / "src" / "volcano_sdk" / "_generated"
    generated.mkdir()
    _ = (generated / "client.py").write_text("def generated():\n    return 1\n")

    result = run_coverage(coverage_project)

    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.OK


def test_private_test_support_does_not_count_as_runtime(
    coverage_project: pytest.Pytester,
) -> None:
    support = coverage_project.path / "src/volcano_sdk/_tests"
    support.mkdir()
    _ = (support / "unexecuted_support.py").write_text(
        "def fixture():\n    return 1\n", encoding="utf-8"
    )

    result = run_coverage(coverage_project)

    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.OK
