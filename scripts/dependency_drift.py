"""Compare a lock-free install of the wheel with uv.lock.

`uv tree --outdated` reports the newest releases, not what the published
specifiers resolve to, so this report covers that gap. Drift is a warning; an
exact pin that resolves differently, or test tooling that changes a runtime
package, fails.
"""

from __future__ import annotations

import os
import re
import sys
import tomllib
from pathlib import Path
from typing import cast

EXACT_PIN = re.compile(r"==([^,*;\s]+)")


def canonical(name: str) -> str:
    """Normalize a distribution name as PEP 503 does.

    Returns:
        The normalized name.

    """
    return re.sub(r"[-_.]+", "-", name).lower()


def installed(path: Path) -> dict[str, str]:
    """Read `uv pip list --format freeze` output.

    Returns:
        Installed versions by normalized name.

    Raises:
        ValueError: A line is not an exact `name==version` entry.

    """
    versions: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        name, separator, version = line.partition("==")
        if not separator:
            msg = f"Unexpected freeze entry: {line}"
            raise ValueError(msg)
        versions[canonical(name)] = version
    return versions


def lock_packages(path: Path) -> list[dict[str, object]]:
    """Read the package entries of a uv lockfile.

    Returns:
        Every locked package entry.

    """
    lock = cast("dict[str, object]", tomllib.loads(path.read_text(encoding="utf-8")))
    return cast("list[dict[str, object]]", lock["package"])


def locked_versions(packages: list[dict[str, object]]) -> dict[str, set[str]]:
    """Collect locked versions; a fork can lock several per package.

    Returns:
        Locked versions by normalized name.

    """
    versions: dict[str, set[str]] = {}
    for package in packages:
        name = canonical(str(package["name"]))
        versions.setdefault(name, set()).add(str(package["version"]))
    return versions


def exact_pins(packages: list[dict[str, object]]) -> dict[str, str]:
    """Find the project's runtime requirements that name one exact version.

    Returns:
        Pinned versions by normalized name.

    """
    project = next(
        package for package in packages if package.get("source") == {"editable": "."}
    )
    metadata = cast("dict[str, object]", project["metadata"])
    requirements = cast("list[dict[str, str]]", metadata["requires-dist"])
    pins: dict[str, str] = {}
    for requirement in requirements:
        match = EXACT_PIN.fullmatch(requirement.get("specifier", ""))
        if match:
            pins[canonical(requirement["name"])] = match.group(1)
    return pins


def drift_rows(
    locked: dict[str, set[str]], resolved: dict[str, str]
) -> tuple[list[str], list[str]]:
    """Tabulate each resolved runtime package against the lock.

    Returns:
        Markdown table lines and GitHub warning annotations.

    """
    rows = [
        "| Runtime package | uv.lock | Fresh install |",
        "| --- | --- | --- |",
    ]
    warnings: list[str] = []
    for name, version in sorted(resolved.items()):
        expected = locked.get(name, set())
        lock_text = ", ".join(sorted(expected)) or "not locked"
        drifted = version not in expected
        status = " (drift)" if drifted else ""
        rows.append(f"| {name} | {lock_text} | {version}{status} |")
        if drifted:
            detail = f"uv.lock has {lock_text}; a fresh install resolves {version}"
            warnings.append(f"::warning title=Dependency drift::{name}: {detail}")
    return rows, warnings


def failures(
    pins: dict[str, str], resolved: dict[str, str], tested: dict[str, str]
) -> list[str]:
    """Find resolutions the tests must not accept.

    Returns:
        Exact pins that resolved differently and runtime packages that the
        test tooling changed.

    """
    missing = "nothing"
    return [
        *(
            f"{name}=={pin} resolved to {resolved.get(name, missing)}"
            for name, pin in sorted(pins.items())
            if resolved.get(name) != pin
        ),
        *(
            f"test tooling changed {name} from {version} to {tested.get(name, missing)}"
            for name, version in sorted(resolved.items())
            if tested.get(name) != version
        ),
    ]


def main(lock_path: Path, resolved_path: Path, tested_path: Path) -> int:
    """Print the drift report and enforce exact pins.

    Returns:
        Zero unless an exact pin or a runtime package version was not honored.

    """
    packages = lock_packages(lock_path)
    resolved = installed(resolved_path)
    rows, warnings = drift_rows(locked_versions(packages), resolved)
    errors = failures(exact_pins(packages), resolved, installed(tested_path))
    table = "\n".join(rows)
    print(table)
    for warning in warnings:
        print(warning)
    for error in errors:
        print(f"::error title=Fresh install::{error}", file=sys.stderr)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with Path(summary).open("a", encoding="utf-8") as stream:
            _ = stream.write(f"### Fresh-install dependency drift\n\n{table}\n\n")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])))
