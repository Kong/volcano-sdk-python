"""Check changed-callable mutation selection and result classification."""

from __future__ import annotations

import sys
from io import StringIO
from typing import TYPE_CHECKING

import pytest

from scripts.mutation_targets import (
    CRITICAL_MODULES,
    changed_lines,
    check_results,
    main,
    result_report,
    select_targets,
)

if TYPE_CHECKING:
    from pathlib import Path


def test_changed_callables_select_native_mutmut_patterns(tmp_path: Path) -> None:
    path = "src/volcano_sdk/sample.py"
    source = """def increment(value: int) -> int:
    return value + 1

class Counter:
    def advance(self, value: int) -> int:
        return value + 2

async def fetch(value: int) -> int:
    return value + 3
"""
    destination = tmp_path / path
    destination.parent.mkdir(parents=True)
    destination.write_text(source, encoding="utf-8")
    diff = f"""+++ b/{path}
@@ -2 +2 @@
@@ -6 +6 @@
@@ -9 +9 @@
"""

    assert select_targets(diff, tmp_path) == sorted(
        [
            *CRITICAL_MODULES,
            "volcano_sdk.sample.x_increment__mutmut_*",
            "volcano_sdk.sample.x\u01c1Counter\u01c1advance__mutmut_*",
            "volcano_sdk.sample.x_fetch__mutmut_*",
        ]
    )


def test_deletion_only_hunk_still_selects_enclosing_callable(tmp_path: Path) -> None:
    path = "src/volcano_sdk/sample.py"
    destination = tmp_path / path
    destination.parent.mkdir(parents=True)
    destination.write_text("def changed() -> int:\n    return 1\n", encoding="utf-8")

    diff = f"+++ b/{path}\n@@ -2,1 +2,0 @@\n"

    assert "volcano_sdk.sample.x_changed__mutmut_*" in select_targets(diff, tmp_path)


def test_generated_files_are_not_mutation_targets() -> None:
    diff = "+++ b/src/volcano_sdk/_generated/client.py\n@@ -1 +1 @@\n"

    assert changed_lines(diff) == {}


def test_selected_mutants_report_failures_separately() -> None:
    results = """volcano_sdk.sample.x_run__mutmut_1: killed
volcano_sdk.sample.x_run__mutmut_2: survived
volcano_sdk.sample.x_run__mutmut_3: no tests
volcano_sdk.sample.x_run__mutmut_4: timeout
volcano_sdk.sample.x_run__mutmut_5: segfault
volcano_sdk.sample.x_run__mutmut_6: not checked
volcano_sdk.other.x_run__mutmut_1: survived
"""
    report = result_report(results, ["volcano_sdk.sample.*"])

    assert report == {
        "selected": 6,
        "killed": 1,
        "survived": 1,
        "uncovered": 1,
        "equivalent": 0,
        "crashes": 1,
        "timeouts": 1,
        "incomplete": 1,
        "unmatched_targets": 0,
    }
    with pytest.raises(ValueError, match="unchecked or alive"):
        check_results(report)


def test_only_selected_mutants_must_be_killed() -> None:
    results = """volcano_sdk.sample.x_run__mutmut_1: killed
volcano_sdk.other.x_run__mutmut_1: survived
"""

    check_results(result_report(results, ["volcano_sdk.sample.*"]))


def test_every_changed_callable_must_produce_a_mutant() -> None:
    results = "volcano_sdk._lock_guard.x_run__mutmut_1: killed\n"
    targets = [*CRITICAL_MODULES, "volcano_sdk.sample.x_changed__mutmut_*"]

    report = result_report(results, targets)

    assert report["unmatched_targets"] == len(targets) - 1
    with pytest.raises(ValueError, match="unchecked or alive"):
        check_results(report)


def test_empty_mutation_result_fails() -> None:
    with pytest.raises(ValueError, match="no mutants"):
        check_results(result_report("", ["volcano_sdk.sample.*"]))


def test_failed_mutation_check_preserves_category_report(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    targets = tmp_path / "targets.txt"
    report = tmp_path / "summary.json"
    targets.write_text("volcano_sdk.sample.*\n", encoding="utf-8")
    monkeypatch.setattr(
        sys, "argv", ["mutation_targets", "check", str(targets), str(report)]
    )
    monkeypatch.setattr(
        sys,
        "stdin",
        StringIO("volcano_sdk.sample.x_run__mutmut_1: survived\n"),
    )

    with pytest.raises(ValueError, match="unchecked or alive"):
        main()

    assert '"survived": 1' in report.read_text(encoding="utf-8")
