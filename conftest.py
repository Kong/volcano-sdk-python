"""Reject incomplete test runs, even when pytest would otherwise report success."""

from __future__ import annotations

from typing import Protocol

import pytest

pytest_plugins = ["pytester"]

_WARNING_PREFIX = "ignore:'asyncio.iscoroutinefunction' is deprecated"
_REVIEWED_WARNING = f"{_WARNING_PREFIX}:{DeprecationWarning.__name__}"


def _reviewed_warning_filter(item: pytest.Item, marker: pytest.Mark) -> bool:
    return (
        item.nodeid.startswith("src/volcano_sdk/_tests/test_durable_authoring.py::")
        and marker.args == (_REVIEWED_WARNING,)
        and not marker.kwargs
    )


def _mutation_checkout(config: pytest.Config) -> bool:
    # Mutmut runs relevant node IDs from its generated checkout.
    return (
        config.rootpath.name == "mutants" and (config.rootpath.parent / ".git").exists()
    )


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
            if any(
                marker.name == "filterwarnings"
                and not _reviewed_warning_filter(item, marker)
                for marker in item.iter_markers()
            ):
                self.violations.add(f"unreviewed warning filter: {item.nodeid}")

    def pytest_deselected(self, items: list[pytest.Item]) -> None:
        if items:
            self.violations.add(f"deselected tests: {items[0].nodeid}")

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
        collecting = bool(session.config.getoption("--collect-only"))
        if not collecting and expected - self.completed:
            self.violations.add("selected tests did not execute")
        if self.violations and session.exitstatus == pytest.ExitCode.OK:
            session.exitstatus = pytest.ExitCode.TESTS_FAILED

    def pytest_terminal_summary(self, terminalreporter: _TerminalSummary) -> None:
        for violation in sorted(self.violations):
            terminalreporter.write_sep(
                "!", f"Incomplete test run: {violation}", red=True
            )


def _selection_errors(config: pytest.Config) -> set[str]:
    errors: set[str] = set()
    roots = config.getoption("file_or_dir")
    if (
        roots
        and roots != ["tests/unit", "src/volcano_sdk/_tests"]
        and not _mutation_checkout(config)
    ):
        errors.add("focused test paths")
    if config.getoption("ignore") or config.getoption("ignore_glob"):
        errors.add("ignored test paths")
    return errors


def _warning_errors(config: pytest.Config) -> set[str]:
    errors: set[str] = set()
    if config.getoption("pythonwarnings"):
        errors.add("per-run warning filters")
    overrides: list[object] = config.getoption("override_ini") or []
    if any(
        isinstance(override, str)
        and override.partition("=")[0].strip() == "filterwarnings"
        for override in overrides
    ):
        errors.add("overridden warning filters")
    return errors


def pytest_configure(config: pytest.Config) -> None:
    integrity = _TestIntegrity()
    integrity.violations.update(_selection_errors(config))
    integrity.violations.update(_warning_errors(config))
    if config.getoption("collectonly") and config.getoption("xmlpath") is not None:
        integrity.violations.add("test report requested without execution")
    _ = config.pluginmanager.register(integrity, "sdk-test-integrity")
