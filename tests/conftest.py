"""Reject incomplete test runs, even when pytest would otherwise report success."""

from __future__ import annotations

from typing import Protocol

import pytest

pytest_plugins = ["pytester"]


class _TerminalSummary(Protocol):
    def write_sep(self, sep: str, title: str, *, red: bool) -> None: ...


class _TestIntegrity:
    def __init__(self) -> None:
        self.violations: set[str] = set()
        self.reports: set[tuple[str, str]] = set()
        self.completed: set[str] = set()

    def pytest_collection_modifyitems(self, items: list[pytest.Item]) -> None:
        for item in items:
            forbidden = {"skip", "skipif", "xfail"}
            if forbidden.intersection(marker.name for marker in item.iter_markers()):
                self.violations.add(f"disabled test marker: {item.nodeid}")

    def pytest_collectreport(self, report: pytest.CollectReport) -> None:
        if report.skipped:
            self.violations.add(f"skipped collection: {report.nodeid}")

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        key = (report.nodeid, report.when)
        if key in self.reports:
            self.violations.add(f"repeated test phase: {report.nodeid}")
        self.reports.add(key)
        if report.skipped or hasattr(report, "wasxfail"):
            self.violations.add(f"skipped or expected failure: {report.nodeid}")
        if report.when == "call":
            self.completed.add(report.nodeid)

    def pytest_sessionfinish(self, session: pytest.Session) -> None:
        expected = {item.nodeid for item in session.items}
        if not expected:
            self.violations.add("empty test discovery")
        if not session.config.option.collectonly and expected - self.completed:
            self.violations.add("selected tests did not execute")
        if self.violations and session.exitstatus == pytest.ExitCode.OK:
            session.exitstatus = pytest.ExitCode.TESTS_FAILED

    def pytest_terminal_summary(self, terminalreporter: _TerminalSummary) -> None:
        for violation in sorted(self.violations):
            terminalreporter.write_sep(
                "!", f"Incomplete test run: {violation}", red=True
            )


def pytest_configure(config: pytest.Config) -> None:
    config.pluginmanager.register(_TestIntegrity(), "sdk-test-integrity")
