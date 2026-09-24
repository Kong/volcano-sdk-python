"""Require every runtime module in exactly one successful mutation shard."""

from __future__ import annotations

import json
import os
import sys
from collections import Counter
from pathlib import Path
from typing import cast


class MutationShardError(Exception):
    """A required mutation shard or runtime module is missing or failed."""


def source_modules(path: Path) -> set[str]:
    """Read the tracked handwritten runtime inventory.

    Returns:
        Runtime module paths.

    """
    return {
        os.fsdecode(raw)
        for raw in path.read_bytes().split(b"\0")
        if raw and not raw.startswith(b"src/volcano_sdk/_generated/")
    }


def valid_outcomes(raw: object) -> bool:
    """Accept only nonempty native killed or statically invalid outcomes.

    Returns:
        Whether the result counts are complete and successful.

    """
    if not isinstance(raw, dict):
        return False
    counts = cast("dict[object, object]", raw)
    if not counts or any(
        name not in {"killed", "type_checked"}
        or not isinstance(count, int)
        or isinstance(count, bool)
        or count < 0
        for name, count in counts.items()
    ):
        return False
    validated_counts = cast("dict[str, int]", counts)
    return sum(validated_counts.values()) > 0


def shard_modules(path: Path) -> list[str]:
    """Validate one native Mutmut result report.

    Returns:
        Paths audited by this shard.

    Raises:
        MutationShardError: The report is incomplete or contains failed mutants.

    """
    raw = cast("object", json.loads(path.read_text(encoding="utf-8")))
    if not isinstance(raw, dict):
        msg = f"Invalid mutation report: {path}"
        raise MutationShardError(msg)
    report = cast("dict[str, object]", raw)
    modules = report.get("modules")
    outcomes = report.get("outcomes")
    failures = report.get("failures")
    if (
        not isinstance(modules, list)
        or not modules
        or not isinstance(failures, list)
        or failures
    ):
        msg = f"Incomplete mutation report: {path}"
        raise MutationShardError(msg)
    typed_modules = cast("list[object]", modules)
    if not all(isinstance(module, str) for module in typed_modules):
        msg = f"Invalid mutation modules: {path}"
        raise MutationShardError(msg)
    if not valid_outcomes(outcomes):
        msg = f"Failed mutation outcomes: {path}"
        raise MutationShardError(msg)
    return cast("list[str]", modules)


def main(root: Path, source_path: Path, count: int) -> int:
    """Check shard presence, successful results, and complete source coverage.

    Returns:
        Zero only when every runtime module appears exactly once.

    Raises:
        MutationShardError: A shard or source module is missing or invalid.

    """
    expected = source_modules(source_path)
    if not expected or count < 1:
        msg = "Empty source inventory or invalid shard count"
        raise MutationShardError(msg)
    actual: Counter[str] = Counter()
    for index in range(count):
        report = root / f"mutation-outcomes-{index}" / "mutation.json"
        actual.update(shard_modules(report))
    extra = sorted(set(actual) - expected)
    missing = sorted(expected - set(actual))
    duplicate = sorted(name for name, occurrences in actual.items() if occurrences != 1)
    if extra or missing or duplicate:
        msg = f"Mutation shard inventory differs: {extra=}, {missing=}, {duplicate=}"
        raise MutationShardError(msg)
    print(f"Mutation shards covered {len(expected)} handwritten runtime modules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])))
