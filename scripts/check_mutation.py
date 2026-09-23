"""Check selected mutmut results, including raw harness exit codes."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Literal, TypeGuard, cast

ExitCode = int | None
Outcome = Literal[
    "killed",
    "survived",
    "uncovered",
    "crashed",
    "timed_out",
    "incomplete",
]

STATUS: dict[ExitCode, Outcome] = {
    1: "killed",
    0: "survived",
    5: "uncovered",
    33: "uncovered",
    3: "crashed",  # mutmut 3.8 calls pytest internal error a kill.
    -11: "crashed",
    -9: "crashed",
    24: "timed_out",
    36: "timed_out",
    152: "timed_out",
    255: "timed_out",
    -24: "timed_out",
}


def is_result_map(value: object) -> TypeGuard[dict[str, ExitCode]]:
    """Validate the relevant part of mutmut's pinned JSON metadata.

    Returns:
        Whether each mutant has a name and a raw numeric result.

    """
    if not isinstance(value, dict):
        return False
    entries = cast("dict[object, object]", value)
    return all(
        isinstance(name, str) and (code is None or type(code) is int)
        for name, code in entries.items()
    )


def module_results(path: Path) -> dict[str, ExitCode]:
    """Read the selected module's raw mutmut outcomes.

    Returns:
        Mutant names and raw exit codes.

    Raises:
        ValueError: If the metadata is missing or lacks results.
        TypeError: If the metadata has the wrong shape.

    """
    metadata = Path("mutants") / f"{path}.meta"
    if not metadata.is_file():
        msg = f"Missing mutmut metadata for {path}"
        raise ValueError(msg)
    data = cast("object", json.loads(metadata.read_text(encoding="utf-8")))
    if not isinstance(data, dict):
        msg = f"Invalid mutmut metadata for {path}"
        raise TypeError(msg)
    fields = cast("dict[object, object]", data)
    results = fields.get("exit_code_by_key")
    if not is_result_map(results):
        msg = f"Invalid mutmut metadata for {path}"
        raise ValueError(msg)
    return results


def summarize(paths: list[Path]) -> dict[str, object]:
    """Classify the selected modules and retain each failed mutant name.

    Returns:
        A machine-readable outcome report.

    Raises:
        ValueError: If a selected module has no valid mutmut results.
        TypeError: If a selected module has malformed metadata.

    """
    counts: Counter[Outcome] = Counter()
    failures: list[str] = []
    unmutatable: list[str] = []
    for path in paths:
        results = module_results(path)
        if not results:
            unmutatable.append(str(path))
        for name, code in results.items():
            outcome = STATUS.get(code, "incomplete")
            counts[outcome] += 1
            if outcome != "killed":
                failures.append(f"{name}: {outcome} (exit {code})")
    return {
        "modules": [str(path) for path in paths],
        "outcomes": dict(sorted(counts.items())),
        "unmutatable_modules": unmutatable,
        "failures": failures,
    }


def main(paths: list[Path]) -> int:
    """Write the scoped report and reject every non-killed mutant.

    Returns:
        Zero only for a nonempty, fully killed mutation run.

    """
    report = summarize(paths)
    destination = Path("reports/mutation.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    _ = destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    outcomes = report["outcomes"]
    failures = report["failures"]
    return int(not outcomes or bool(failures))


if __name__ == "__main__":
    raise SystemExit(main([Path(argument) for argument in sys.argv[1:]]))
