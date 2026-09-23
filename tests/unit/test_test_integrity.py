from __future__ import annotations

from pathlib import Path

import pytest

INTEGRITY = (Path(__file__).parents[1] / "conftest.py").read_text()


@pytest.fixture
def guarded(pytester: pytest.Pytester) -> pytest.Pytester:
    pytester.makeconftest(INTEGRITY)
    return pytester


def test_complete_run_passes(guarded: pytest.Pytester) -> None:
    guarded.makepyfile("def test_passes(): assert True")
    result = guarded.runpytest_subprocess()
    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.OK


def test_collect_only_discovers_tests_without_execution(
    guarded: pytest.Pytester,
) -> None:
    guarded.makepyfile("def test_discovered(): assert True")
    result = guarded.runpytest_subprocess("--collect-only", "-q")
    assert result.ret == pytest.ExitCode.OK
    result.stdout.fnmatch_lines(["*1 test collected*"])


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
    guarded.makepyfile(source)
    result = guarded.runpytest_subprocess()
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    result.stdout.fnmatch_lines(["*Incomplete test run:*"])


def test_empty_discovery_fails(guarded: pytest.Pytester) -> None:
    result = guarded.runpytest_subprocess()
    assert result.ret == pytest.ExitCode.NO_TESTS_COLLECTED
    result.stdout.fnmatch_lines(["*Incomplete test run: empty test discovery*"])


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
    guarded.makepyfile(
        test_skipped=source, test_passed="def test_passes(): assert True"
    )
    result = guarded.runpytest_subprocess()
    result.assert_outcomes(passed=1, skipped=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    result.stdout.fnmatch_lines(["*Incomplete test run: skipped collection:*"])


def test_missing_execution_fails(guarded: pytest.Pytester) -> None:
    guarded.makeconftest(
        INTEGRITY + "\ndef pytest_runtest_protocol(item, nextitem): return True\n",
    )
    guarded.makepyfile("def test_omitted(): assert True")
    result = guarded.runpytest_subprocess()
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    result.stdout.fnmatch_lines(
        ["*Incomplete test run: selected tests did not execute*"]
    )


def test_repeated_execution_fails(guarded: pytest.Pytester) -> None:
    guarded.makepyfile("def test_repeated(): assert True")
    result = guarded.runpytest_subprocess(
        "--keep-duplicates",
        "test_repeated_execution_fails.py",
        "test_repeated_execution_fails.py",
    )
    result.assert_outcomes(passed=2)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    result.stdout.fnmatch_lines(["*Incomplete test run: repeated test phase:*"])


def test_real_failure_stays_failed(guarded: pytest.Pytester) -> None:
    guarded.makepyfile("def test_failure(): assert False")
    result = guarded.runpytest_subprocess()
    result.assert_outcomes(failed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
