#!/usr/bin/env python3
"""Verify that the checked-in OpenAPI client matches regeneration."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

from generate_openapi import DEFAULT_OUTPUT, generate


def generated_files(root: Path) -> dict[Path, Path]:
    """Return generated files keyed by their path relative to the output root."""
    return {
        path.relative_to(root): path
        for path in root.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix not in {".pyc", ".pyo"}
    }


def compared_files(left: Path, right: Path) -> tuple[list[str], list[str], list[str]]:
    """Return missing, extra, and changed paths between two generated trees."""
    left_files = generated_files(left)
    right_files = generated_files(right)
    missing = [str(path) for path in sorted(left_files.keys() - right_files.keys())]
    extra = [str(path) for path in sorted(right_files.keys() - left_files.keys())]
    changed = [
        str(path)
        for path in sorted(left_files.keys() & right_files.keys())
        if left_files[path].read_bytes() != right_files[path].read_bytes()
    ]
    return missing, extra, changed


def main() -> None:
    """Regenerate the client and report any checked-in drift."""
    with tempfile.TemporaryDirectory(prefix="volcano-sdk-openapi-") as directory:
        generated = Path(directory) / "_generated"
        generate(generated)
        missing, extra, changed = compared_files(DEFAULT_OUTPUT, generated)

    if missing or extra or changed:
        for label, paths in (
            ("missing from regeneration", missing),
            ("unexpected in regeneration", extra),
            ("changed after regeneration", changed),
        ):
            for path in sorted(paths):
                print(f"{label}: {path}", file=sys.stderr)
        raise SystemExit(1)

    print("OpenAPI generated client is up to date")


if __name__ == "__main__":
    main()
