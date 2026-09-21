#!/usr/bin/env python3
"""Run the same SDK checks locally and in CI."""

from __future__ import annotations

import os
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path
from tempfile import TemporaryDirectory


def main() -> None:
    """Check source, contract bindings, and freshly built distributions."""
    os.chdir(Path(__file__).resolve().parent.parent)
    subprocess.run([sys.executable, "scripts/check_openapi.py"], check=True)
    subprocess.run([sys.executable, "-m", "ruff", "check", "."], check=True)
    subprocess.run(
        [sys.executable, "-m", "ruff", "format", "--check", "."],
        check=True,
    )
    subprocess.run([sys.executable, "-m", "mypy"], check=True)
    subprocess.run([sys.executable, "-m", "pyright"], check=True)
    subprocess.run(
        [sys.executable, "-m", "pytest", "tests/unit", "-q"],
        check=True,
    )
    fixture = Path("tests/fixtures/sdk-contract-dry-run.json").resolve()
    fixture.chmod(0o600)
    subprocess.run(
        [
            sys.executable,
            "-m",
            "behave",
            "features/contract",
            "--dry-run",
            "--no-snippets",
        ],
        check=True,
        env=os.environ | {"VOLCANO_SDK_CONTRACT_FIXTURE": str(fixture)},
    )
    with TemporaryDirectory(prefix="volcano-sdk-quality-") as directory:
        subprocess.run(  # noqa: S603 - fixed command and private temporary path.
            [sys.executable, "-m", "build", "--outdir", directory],
            check=True,
        )
        subprocess.run(  # noqa: S603 - fixed script and private build artifacts.
            [
                "/bin/bash",
                "scripts/check_package.sh",
                version("volcano-sdk-python"),
                directory,
            ],
            check=True,
        )


if __name__ == "__main__":
    main()
