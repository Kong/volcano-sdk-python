"""Select changed SDK callables and check mutmut's selected results."""

from __future__ import annotations

import ast
import fnmatch
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

SOURCE_PREFIX = "src/volcano_sdk/"
CRITICAL_MODULES = (
    "volcano_sdk._lock_guard.*",
    "volcano_sdk._lock_renewer.*",
    "volcano_sdk._lock_worker.*",
    "volcano_sdk.locks.*",
)
_HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")
_RESULT = re.compile(r"^\s*(volcano_sdk\.[^:]+): ([a-z_ ]+)$")


def changed_lines(diff: str) -> dict[str, set[int]]:
    """Read new-side line numbers from a zero-context Git diff.

    Returns:
        Source paths mapped to changed line numbers.

    """
    changes: dict[str, set[int]] = {}
    path: str | None = None
    for line in diff.splitlines():
        if line.startswith("+++ "):
            candidate = line.removeprefix("+++ b/")
            path = (
                candidate
                if candidate.startswith(SOURCE_PREFIX)
                and not candidate.startswith(f"{SOURCE_PREFIX}_generated/")
                and candidate.endswith(".py")
                else None
            )
        elif path is not None and (match := _HUNK.match(line)):
            start = max(1, int(match[1]))
            count = int(match[2]) if match[2] is not None else 1
            changes.setdefault(path, set()).update(range(start, start + max(1, count)))
    return changes


def _callables(
    nodes: Iterable[ast.stmt], classes: tuple[str, ...] = ()
) -> Iterable[tuple[tuple[str, ...], ast.FunctionDef | ast.AsyncFunctionDef]]:
    for node in nodes:
        if isinstance(node, ast.ClassDef):
            yield from _callables(node.body, (*classes, node.name))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield classes, node


def _mutant_pattern(module: str, classes: tuple[str, ...], name: str) -> str:
    callable_name = (
        "x\u01c1" + "\u01c1".join((*classes, name)) if classes else "x_" + name
    )
    return f"{module}.{callable_name}__mutmut_*"


def select_targets(diff: str, root: Path) -> list[str]:
    """Select native mutmut patterns for changed functions and critical locks.

    Returns:
        Sorted native mutmut selection patterns.

    """
    targets: set[str] = set(CRITICAL_MODULES)
    for path, lines in changed_lines(diff).items():
        source = root / path
        if not source.is_file():
            continue
        module = ".".join(Path(path).with_suffix("").parts[1:])
        tree = ast.parse(source.read_text(encoding="utf-8"), filename=path)
        for classes, node in _callables(tree.body):
            first = min(
                (decorator.lineno for decorator in node.decorator_list),
                default=node.lineno,
            )
            last = node.end_lineno or node.lineno
            if any(first <= line <= last for line in lines):
                targets.add(_mutant_pattern(module, classes, node.name))
    return sorted(targets)


def selected_results(results: str, targets: list[str]) -> Counter[str]:
    """Count only mutants selected by native mutmut run patterns.

    Returns:
        Mutmut outcome counts for selected mutants.

    """
    counts: Counter[str] = Counter()
    for line in results.splitlines():
        if match := _RESULT.match(line):
            name, status = match.groups()
            if any(fnmatch.fnmatchcase(name, target) for target in targets):
                counts[status] += 1
    return counts


def result_report(results: str, targets: list[str]) -> dict[str, int]:
    """Classify selected mutants without counting crashes as test failures.

    Returns:
        Counts for each distinct outcome category.

    """
    counts = selected_results(results, targets)
    incomplete = counts.total() - sum(
        counts[status]
        for status in ("killed", "survived", "no tests", "segfault", "timeout")
    )
    return {
        "selected": counts.total(),
        "killed": counts["killed"],
        "survived": counts["survived"],
        "uncovered": counts["no tests"],
        "equivalent": 0,
        "crashes": counts["segfault"],
        "timeouts": counts["timeout"],
        "incomplete": incomplete,
    }


def check_results(report: dict[str, int]) -> None:
    """Reject empty, surviving, uncovered, or incomplete selected mutants.

    Raises:
        ValueError: The selected mutation run is incomplete or has survivors.

    """
    if report["selected"] == 0:
        msg = "mutation run selected no mutants"
        raise ValueError(msg)
    if report["selected"] != report["killed"]:
        msg = f"mutation run left selected mutants unchecked or alive: {report}"
        raise ValueError(msg)


def main() -> None:
    """Select Git-diff targets or validate native mutmut results on stdin.

    Raises:
        SystemExit: The command is invalid or selected mutation results fail.

    """
    match sys.argv[1:]:
        case ["select"]:
            targets = select_targets(sys.stdin.read(), Path.cwd())
            _ = sys.stdout.write("\n".join(targets) + "\n")
        case ["check", targets_path, report_path]:
            targets = Path(targets_path).read_text(encoding="utf-8").splitlines()
            report = result_report(sys.stdin.read(), targets)
            output = json.dumps(report, indent=2) + "\n"
            _ = Path(report_path).write_text(output, encoding="utf-8")
            _ = sys.stdout.write(output)
            check_results(report)
        case _:
            msg = "usage: mutation_targets.py select|check TARGETS REPORT"
            raise SystemExit(msg)


if __name__ == "__main__":
    main()
