"""Pytest plugin: fail a run whose SDK modules did not come from the installed wheel.

`scripts/check_fresh_install.sh` loads it with `-p installed_sdk`. The source
tree stays importable during that run, so a stray import of `src/` would test
the checkout instead of the wheel.
"""

from __future__ import annotations

import sys
import sysconfig
from pathlib import Path
from typing import Protocol

import pytest

PACKAGE = "volcano_sdk"
TESTS = f"{PACKAGE}._tests"


class _TerminalSummary(Protocol):
    def write_line(self, line: str) -> None: ...

    def write_sep(self, sep: str, title: str, *, red: bool) -> None: ...


def sdk_origins() -> dict[str, str]:
    """Locate each loaded SDK module other than the copied tests.

    Returns:
        Module files by module name.

    """
    return {
        name: module.__file__ or ""
        for name, module in sys.modules.items()
        if (name == PACKAGE or name.startswith(f"{PACKAGE}."))
        and name != TESTS
        and not name.startswith(f"{TESTS}.")
    }


def misplaced(origins: dict[str, str], installed: Path) -> list[str]:
    """Find SDK modules loaded from outside the installed package.

    Returns:
        Violations, including a run that never imported the SDK.

    """
    if PACKAGE not in origins:
        return [f"{PACKAGE} was not imported"]
    return [
        f"{name} imported from {origin or 'no file'}"
        for name, origin in sorted(origins.items())
        if not origin or not Path(origin).resolve().is_relative_to(installed)
    ]


class _InstalledSdk:
    def __init__(self) -> None:
        purelib = Path(sysconfig.get_path("purelib"))
        self.installed: Path = (purelib / PACKAGE).resolve()
        self.violations: list[str] = []

    def pytest_sessionfinish(self, session: pytest.Session) -> None:
        self.violations = misplaced(sdk_origins(), self.installed)
        if self.violations and session.exitstatus == pytest.ExitCode.OK:
            session.exitstatus = pytest.ExitCode.TESTS_FAILED

    def pytest_terminal_summary(self, terminalreporter: _TerminalSummary) -> None:
        for violation in self.violations:
            terminalreporter.write_sep(
                "!", f"SDK not from the installed wheel: {violation}", red=True
            )
        if not self.violations:
            terminalreporter.write_line(f"SDK imported from {self.installed}")


def pytest_configure(config: pytest.Config) -> None:
    """Register the origin check for this session."""
    _ = config.pluginmanager.register(_InstalledSdk(), "installed-sdk-origin")
