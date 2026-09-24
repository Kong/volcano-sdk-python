from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

INTEGRITY = (Path(__file__).parents[1] / "conftest.py").read_text()
PROJECT = Path(__file__).parents[2]


@pytest.fixture
def guarded(pytester: pytest.Pytester) -> pytest.Pytester:
    _ = pytester.makeconftest(INTEGRITY)
    return pytester


def test_complete_run_passes(guarded: pytest.Pytester) -> None:
    _ = guarded.makepyfile("def test_passes(): assert True")
    result = guarded.runpytest_subprocess()
    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.OK


def test_collect_only_discovers_tests_without_execution(
    guarded: pytest.Pytester,
) -> None:
    _ = guarded.makepyfile("def test_discovered(): assert True")
    result = guarded.runpytest_subprocess("--collect-only", "-q")
    assert result.ret == pytest.ExitCode.OK
    result.stdout.fnmatch_lines(["*1 test collected*"])


def test_collect_only_cannot_satisfy_a_reported_test_run(
    guarded: pytest.Pytester,
) -> None:
    _ = guarded.makepyfile("def test_discovered(): assert True")
    result = guarded.runpytest_subprocess("--collect-only", "--junitxml=unit.xml")
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    result.stdout.fnmatch_lines(
        ["*Incomplete test run: test report requested without execution*"]
    )


@pytest.mark.parametrize(
    "source",
    [
        "import pytest\n@pytest.mark.skip\ndef test_skipped(): assert True",
        (
            "import pytest\n@pytest.mark.skipif(False, reason='disabled')\n"
            "def test_skipped(): assert True"
        ),
        "import pytest\ndef test_skipped(): pytest.skip('disabled at runtime')",
        (
            "import pytest\n@pytest.fixture\ndef fixture(): pytest.skip('setup')\n"
            "def test_skipped(fixture): assert True"
        ),
        "import pytest\n@pytest.mark.xfail\ndef test_expected(): assert False",
        "import pytest\n@pytest.mark.xfail\ndef test_unexpected(): assert True",
        "import pytest\ndef test_expected(): pytest.xfail('pending implementation')",
    ],
)
def test_disabled_tests_fail(guarded: pytest.Pytester, source: str) -> None:
    _ = guarded.makepyfile(source)
    result = guarded.runpytest_subprocess()
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    result.stdout.fnmatch_lines(["*Incomplete test run:*"])


@pytest.mark.parametrize(
    ("module", "warning", "exit_code"),
    [
        (
            "test_durable_authoring.py",
            "ignore:'asyncio.iscoroutinefunction' is deprecated:DeprecationWarning",
            pytest.ExitCode.OK,
        ),
        ("test_durable_authoring.py", "ignore", pytest.ExitCode.TESTS_FAILED),
        (
            "test_other.py",
            "ignore:'asyncio.iscoroutinefunction' is deprecated:DeprecationWarning",
            pytest.ExitCode.TESTS_FAILED,
        ),
    ],
)
def test_only_reviewed_warning_filter_is_allowed(
    guarded: pytest.Pytester, module: str, warning: str, exit_code: pytest.ExitCode
) -> None:
    target = guarded.path / "tests" / "unit" / module
    target.parent.mkdir(parents=True)
    _ = target.write_text(
        "import pytest\n"
        f"pytestmark = pytest.mark.filterwarnings({warning!r})\n"
        "def test_passes(): assert True\n",
        encoding="utf-8",
    )
    result = guarded.runpytest_subprocess("tests/unit")
    result.assert_outcomes(passed=1)
    assert result.ret == exit_code
    if exit_code == pytest.ExitCode.TESTS_FAILED:
        result.stdout.fnmatch_lines(
            ["*Incomplete test run: unreviewed warning filter:*"]
        )


def test_empty_discovery_fails(guarded: pytest.Pytester) -> None:
    result = guarded.runpytest_subprocess()
    assert result.ret == pytest.ExitCode.NO_TESTS_COLLECTED
    result.stdout.fnmatch_lines(["*Incomplete test run: empty test discovery*"])


@pytest.mark.parametrize(
    "selection",
    [("-k", "selected"), ("--deselect", "test_cases.py::test_other")],
)
def test_deselection_fails(
    guarded: pytest.Pytester, selection: tuple[str, str]
) -> None:
    _ = guarded.makepyfile(
        test_cases="def test_selected(): assert True\ndef test_other(): assert True"
    )
    result = guarded.runpytest_subprocess(*selection)
    result.assert_outcomes(passed=1, deselected=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    result.stdout.fnmatch_lines(["*Incomplete test run: deselected tests:*"])


@pytest.mark.parametrize("option", ["--ignore", "--ignore-glob"])
def test_ignored_test_paths_fail(guarded: pytest.Pytester, option: str) -> None:
    _ = guarded.makepyfile(
        test_visible="def test_visible(): assert True",
        test_hidden="def test_hidden(): assert True",
    )
    ignored = "test_hidden.py" if option == "--ignore" else "*hidden.py"
    result = guarded.runpytest_subprocess(f"{option}={ignored}")
    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    result.stdout.fnmatch_lines(["*Incomplete test run: ignored test paths*"])


def test_per_run_warning_filter_fails(guarded: pytest.Pytester) -> None:
    _ = guarded.makepyfile("def test_passes(): assert True")
    result = guarded.runpytest_subprocess("-W", "ignore")
    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    result.stdout.fnmatch_lines(["*Incomplete test run: per-run warning filters*"])


def test_overridden_warning_filter_fails(guarded: pytest.Pytester) -> None:
    _ = guarded.makepyfile(
        "import warnings\ndef test_warns(): warnings.warn('unexpected', UserWarning)"
    )
    result = guarded.runpytest_subprocess("-o", "filterwarnings=ignore")
    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    result.stdout.fnmatch_lines(["*Incomplete test run: overridden warning filters*"])


@pytest.mark.parametrize(
    "selection", ["test_selected.py", "test_selected.py::test_one"]
)
def test_positional_selection_fails(guarded: pytest.Pytester, selection: str) -> None:
    _ = guarded.makepyfile(
        test_selected="def test_one(): assert True",
        test_other="def test_other(): assert True",
    )
    result = guarded.runpytest_subprocess(selection)
    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    result.stdout.fnmatch_lines(["*Incomplete test run: focused test paths*"])


@pytest.mark.parametrize(
    "source",
    [
        "import pytest\npytest.skip('module disabled', allow_module_level=True)",
        "import pytest\npytest.importorskip('_volcano_quality_missing_module_')",
        (
            "import pytest\nclass TestDisabled:\n"
            "    pytest.skip('class disabled', allow_module_level=True)"
        ),
    ],
)
def test_collection_skips_fail(guarded: pytest.Pytester, source: str) -> None:
    _ = guarded.makepyfile(
        test_skipped=source, test_passed="def test_passes(): assert True"
    )
    result = guarded.runpytest_subprocess()
    result.assert_outcomes(passed=1, skipped=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    result.stdout.fnmatch_lines(["*Incomplete test run: skipped collection:*"])


def test_missing_execution_fails(guarded: pytest.Pytester) -> None:
    _ = guarded.makeconftest(
        INTEGRITY + "\ndef pytest_runtest_protocol(item, nextitem): return True\n",
    )
    _ = guarded.makepyfile("def test_omitted(): assert True")
    result = guarded.runpytest_subprocess()
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    result.stdout.fnmatch_lines(
        ["*Incomplete test run: selected tests did not execute*"]
    )


def test_repeated_execution_fails(guarded: pytest.Pytester) -> None:
    _ = guarded.makepyfile("def test_repeated(): assert True")
    result = guarded.runpytest_subprocess(
        "--keep-duplicates",
        "test_repeated_execution_fails.py",
        "test_repeated_execution_fails.py",
    )
    result.assert_outcomes(passed=2)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    result.stdout.fnmatch_lines(["*Incomplete test run: repeated test phase:*"])


def test_real_failure_stays_failed(guarded: pytest.Pytester) -> None:
    _ = guarded.makepyfile("def test_failure(): assert False")
    result = guarded.runpytest_subprocess()
    result.assert_outcomes(failed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED


def test_reportless_success_fails_quality_task() -> None:
    result = subprocess.run(
        ["/bin/bash", "tests/quality/report_gate.sh"],
        cwd=PROJECT,
        text=True,
        capture_output=True,
        check=False,
        timeout=10,
    )

    assert result.returncode == 0, result.stdout + result.stderr
