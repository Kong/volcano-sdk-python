"""A full mutation gate must account for every tracked runtime module."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from scripts.check_mutation_shards import MutationShardError, main

if TYPE_CHECKING:
    from pathlib import Path


def write_report(
    root: Path, index: int, module: str, *, outcomes: dict[str, int] | None = None
) -> None:
    """Create one native-result-shaped shard fixture."""
    report = root / f"mutation-outcomes-{index}" / "mutation.json"
    report.parent.mkdir(parents=True)
    _ = report.write_text(
        json.dumps(
            {
                "modules": [module],
                "outcomes": outcomes or {"killed": 1},
                "unmutatable_modules": [],
                "failures": [],
            }
        ),
        encoding="utf-8",
    )


def test_full_mutation_shards_cover_each_runtime_module_once(tmp_path: Path) -> None:
    source = tmp_path / "source.bin"
    _ = source.write_bytes(
        b"src/volcano_sdk/auth.py\0src/volcano_sdk/realtime.py\0"
        b"src/volcano_sdk/_generated/client.py\0"
    )
    write_report(tmp_path, 0, "src/volcano_sdk/auth.py")
    write_report(tmp_path, 1, "src/volcano_sdk/realtime.py")

    assert main(tmp_path, source, 2) == 0


@pytest.mark.parametrize(
    ("failure", "message"),
    [
        ("missing", "mutation.json"),
        ("uncovered", "Failed mutation outcomes"),
        ("survived", "Failed mutation outcomes"),
        ("timed_out", "Failed mutation outcomes"),
        ("zero", "Failed mutation outcomes"),
        ("duplicate", "inventory differs"),
        ("omitted", "inventory differs"),
    ],
)
def test_incomplete_or_failed_mutation_shards_fail(
    tmp_path: Path, failure: str, message: str
) -> None:
    source = tmp_path / "source.bin"
    _ = source.write_bytes(b"src/volcano_sdk/auth.py\0src/volcano_sdk/realtime.py\0")
    write_report(tmp_path, 0, "src/volcano_sdk/auth.py")
    if failure not in {"missing", "omitted"}:
        module = (
            "src/volcano_sdk/auth.py"
            if failure == "duplicate"
            else "src/volcano_sdk/realtime.py"
        )
        outcomes = None
        if failure == "zero":
            outcomes = {"killed": 0}
        elif failure in {"uncovered", "survived", "timed_out"}:
            outcomes = {failure: 1}
        write_report(tmp_path, 1, module, outcomes=outcomes)
    elif failure == "omitted":
        write_report(tmp_path, 1, "src/volcano_sdk/other.py")

    with pytest.raises((MutationShardError, FileNotFoundError), match=message):
        _ = main(tmp_path, source, 2)
