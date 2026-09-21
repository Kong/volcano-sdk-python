"""Exercise native quality tools against deliberately invalid source."""

from __future__ import annotations

import subprocess
import sys


def test_ruff_rejects_excessive_complexity_with_project_configuration() -> None:
    source = """def choose(value: int) -> int:
    if value == 0:
        return 0
    if value == 1:
        return 1
    if value == 2:
        return 2
    if value == 3:
        return 3
    if value == 4:
        return 4
    if value == 5:
        return 5
    return 6
"""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ruff",
            "check",
            "--output-format",
            "concise",
            "--stdin-filename",
            "src/volcano_sdk/_quality_probe.py",
            "-",
        ],
        input=source,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert "C901 `choose` is too complex (7 > 5)" in result.stdout
