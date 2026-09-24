"""Fail scoped mutmut runs on surviving, uncovered, or incomplete mutants."""

from __future__ import annotations

import ast
import json
import os
import sys
from collections import Counter
from pathlib import Path
from typing import cast

EXIT_OUTCOMES = {
    0: "survived",
    1: "killed",
    2: "interrupted",
    3: "crashed",  # pytest internal error is not evidence of a useful test.
    5: "uncovered",
    33: "uncovered",
    34: "skipped",
    35: "crashed",
    36: "timed_out",
    37: "type_checked",
    -24: "timed_out",
    24: "timed_out",
    152: "timed_out",
    255: "timed_out",
    -11: "crashed",
    -9: "crashed",
}


def nul_paths(path: Path) -> list[str]:
    """Read shell-produced NUL-delimited paths.

    Returns:
        Decoded paths.

    """
    return [os.fsdecode(raw) for raw in path.read_bytes().split(b"\0") if raw]


def exit_codes(path: Path) -> dict[str, int | None]:
    """Validate mutmut's per-module result metadata.

    Returns:
        Generated mutant keys and their native exit codes.

    Raises:
        TypeError: The metadata has the wrong shape.
        ValueError: The metadata contains invalid exit codes.

    """
    raw = cast("object", json.loads(path.read_text(encoding="utf-8")))
    if not isinstance(raw, dict):
        msg = f"Invalid mutmut metadata: {path}"
        raise TypeError(msg)
    data = cast("dict[object, object]", raw)
    codes = data.get("exit_code_by_key")
    if not isinstance(codes, dict):
        msg = f"Missing mutant results: {path}"
        raise TypeError(msg)
    entries = cast("dict[object, object]", codes)
    if not all(
        isinstance(key, str)
        and (value is None or (isinstance(value, int) and not isinstance(value, bool)))
        for key, value in entries.items()
    ):
        msg = f"Invalid mutant result codes: {path}"
        raise ValueError(msg)
    return cast("dict[str, int | None]", entries)


def declaration_only(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """Recognize annotation-only signatures without exempting executable bodies.

    Returns:
        Whether the optional docstring is followed only by an ellipsis.

    """
    body = node.body[1:] if ast.get_docstring(node) is not None else node.body
    if len(body) != 1:
        return False
    statement = body[0]
    return (
        isinstance(statement, ast.Expr)
        and isinstance(statement.value, ast.Constant)
        and statement.value.value is Ellipsis
    )


def has_functions(path: Path) -> bool:
    """Distinguish an export-only module from a missing mutation report.

    Returns:
        Whether the source defines a function or method with a runtime body.

    """
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return any(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and not declaration_only(node)
        for node in ast.walk(tree)
    )


def outcomes(path: Path) -> tuple[Counter[str], bool]:
    """Classify every mutant from one selected runtime module.

    Returns:
        Outcome counts and whether the module has no mutatable functions.

    Raises:
        ValueError: Mutmut omitted results for a function-bearing module.

    """
    meta = Path("mutants") / f"{path}.meta"
    if not meta.is_file():
        if not has_functions(path):
            return Counter(), True
        msg = f"Missing mutmut report: {path}"
        raise ValueError(msg)
    codes = exit_codes(meta)
    if not codes:
        if not has_functions(path):
            return Counter(), True
        msg = f"Empty mutmut report: {path}"
        raise ValueError(msg)
    counts = Counter(
        "incomplete" if code is None else EXIT_OUTCOMES.get(code, "crashed")
        for code in codes.values()
    )
    return counts, False


def main(targets_path: Path, failed_path: Path) -> int:
    """Write a machine-readable report and enforce the mutation gate.

    Returns:
        Zero when each selected mutant is killed or statically invalid.

    """
    targets = sorted(set(nul_paths(targets_path)))
    failures = [f"Mutmut harness failed: {name}" for name in nul_paths(failed_path)]
    counts: Counter[str] = Counter()
    unmutatable: list[str] = []
    for name in targets:
        try:
            module_counts, empty = outcomes(Path(name))
        except (OSError, SyntaxError, TypeError, ValueError) as error:
            failures.append(str(error))
            continue
        counts.update(module_counts)
        if empty:
            unmutatable.append(name)
    if not counts and (not targets or len(unmutatable) != len(targets)):
        failures.append("No mutants were tested")
    failures.extend(
        f"{name}: {count} mutant(s)"
        for name, count in sorted(counts.items())
        if name not in {"killed", "type_checked"}
    )
    report = {
        "modules": targets,
        "outcomes": dict(sorted(counts.items())),
        "unmutatable_modules": unmutatable,
        "failures": failures,
    }
    Path("reports").mkdir(exist_ok=True)
    _ = Path("reports/mutation.json").write_text(
        f"{json.dumps(report, indent=2)}\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2))
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2])))
