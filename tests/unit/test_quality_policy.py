"""Negative fixtures for the native quality configuration attestation."""

from __future__ import annotations

import copy
import json
import tomllib
from pathlib import Path
from typing import cast

import pytest

from scripts.check_quality_policy import (
    REVIEWED_WARNING,
    check_comments,
    check_config,
    check_inventory,
    check_lock_bytes,
)

ROOT = Path(__file__).parents[2]


def config_copy() -> dict[str, object]:
    """Load a mutable copy of native tool settings.

    Returns:
        A complete pyproject configuration tree.

    """
    return copy.deepcopy(
        cast("dict[str, object]", tomllib.loads((ROOT / "pyproject.toml").read_text()))
    )


def locked_config() -> dict[str, object]:
    """Load the separately pinned native-tool snapshot.

    Returns:
        The recorded configuration tree.

    """
    return cast(
        "dict[str, object]",
        json.loads((ROOT / "maintainers/quality-policy.lock.json").read_text()),
    )


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        (("coverage", "report", "fail_under"), 99),
        (("coverage", "report", "exclude_lines"), [".*"]),
        (("coverage", "report", "exclude_also"), ["def untested"]),
        (("mypy", "ignore_errors"), True),
        (("basedpyright", "reportAny"), False),
        (("basedpyright", "executionEnvironments"), []),
        (("ruff", "lint", "ignore"), ["ALL"]),
        (("ruff", "lint", "extend-ignore"), ["F821"]),
        (("ruff", "lint", "extend-per-file-ignores"), {"**/*.py": ["ALL"]}),
        (("pytest", "ini_options", "filterwarnings"), ["ignore"]),
        (("poe", "tasks", "checks"), ["policy"]),
        (("poe", "tasks", "coverage"), "true"),
    ],
)
def test_native_guardrail_change_fails(
    path: tuple[str, ...], replacement: object
) -> None:
    config = config_copy()
    section = cast("dict[str, object]", config["tool"])
    for key in path[:-1]:
        section = cast("dict[str, object]", section[key])
    section[path[-1]] = replacement

    assert f"tool.{'.'.join(path)}" in check_config(config, locked_config())


def test_lock_change_requires_reviewed_digest() -> None:
    data = (ROOT / "maintainers/quality-policy.lock.json").read_bytes()

    assert check_lock_bytes(data) == []
    assert check_lock_bytes(data + b" ") == ["quality policy lock digest changed"]


def test_nested_config_fails(tmp_path: Path) -> None:
    name = "tests/unit/pytest.toml"

    assert f"nested tool configuration: {name}" in check_inventory(
        tmp_path, {name}, set()
    )


@pytest.mark.parametrize(
    "name", ["src/volcano_sdk/new_module.py", "typings/external/new_module.pyi"]
)
def test_unlinted_python_file_fails(tmp_path: Path, name: str) -> None:
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    _ = source.write_text("def untested() -> bool: return True\n", encoding="utf-8")

    assert f"Ruff omitted tracked Python file: {name}" in check_inventory(
        tmp_path, {name}, set()
    )


def test_unapproved_ruff_suppression_fails(tmp_path: Path) -> None:
    name = "src/volcano_sdk/new_module.py"
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    _ = source.write_text(
        "def unsafe():\n    return True  # ruff: ignore[S603]\n", encoding="utf-8"
    )

    assert any(
        "unapproved S603" in error for error in check_comments(tmp_path, {name}, [])
    )


def test_multiple_ruff_directives_fail(tmp_path: Path) -> None:
    name = "scripts/generate_openapi.py"
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    _ = source.write_text(
        "def generate():\n    return True  # ruff: ignore[S603] ruff: ignore[S607]\n",
        encoding="utf-8",
    )

    assert any(
        "multiple Ruff directives" in error
        for error in check_comments(tmp_path, {name}, [])
    )


@pytest.mark.parametrize("comment", ["# isort: skip_file", "# yapf: disable"])
def test_file_wide_action_comment_fails(tmp_path: Path, comment: str) -> None:
    name = "src/volcano_sdk/new_module.py"
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    _ = source.write_text(f"{comment}\n", encoding="utf-8")

    assert any(
        "forbidden suppression" in error
        for error in check_comments(tmp_path, {name}, [])
    )


def test_type_check_opt_out_fails(tmp_path: Path) -> None:
    name = "src/volcano_sdk/new_module.py"
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    fixture_lines = (
        "from typing import no_type_check",
        "@no_type_check",
        "def unsafe() -> str:",
        "    return 1",
        "",
    )
    _ = source.write_text(
        "\n".join(fixture_lines),
        encoding="utf-8",
    )

    assert any(
        "forbidden type-check opt-out" in error
        for error in check_comments(tmp_path, {name}, [])
    )


def test_type_ignore_outside_diagnostic_fixture_fails(tmp_path: Path) -> None:
    name = "tests/unit/test_new_behavior.py"
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    _ = source.write_text(
        "value: str = 1  # type: ignore[assignment]\n", encoding="utf-8"
    )

    assert any(
        "type ignore outside diagnostic fixture" in error
        for error in check_comments(tmp_path, {name}, [])
    )


def test_pyright_ignore_outside_diagnostic_fixture_fails(tmp_path: Path) -> None:
    name = "tests/unit/test_new_behavior.py"
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    _ = source.write_text(
        "value: str = 1  # pyright: ignore[reportAssignmentType]\n",
        encoding="utf-8",
    )

    assert any(
        "pyright ignore outside diagnostic fixture" in error
        for error in check_comments(tmp_path, {name}, [])
    )


def test_type_fixture_cannot_hide_other_suppression(tmp_path: Path) -> None:
    name = "src/volcano_sdk/_tests/fixtures/invalid_arguments.py"
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    _ = source.write_text("value = 1  # noqa: S101\n", encoding="utf-8")

    assert any(
        "forbidden suppression" in error
        for error in check_comments(tmp_path, {name}, [])
    )


def test_type_fixture_cannot_hide_pyright_suppression(tmp_path: Path) -> None:
    name = "src/volcano_sdk/_tests/fixtures/invalid_arguments.py"
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    _ = source.write_text(
        "value: str = 1  # pyright: ignore[reportAssignmentType]\n",
        encoding="utf-8",
    )

    assert any(
        "forbidden suppression" in error
        for error in check_comments(tmp_path, {name}, [])
    )


def test_self_authorized_exception_fails(tmp_path: Path) -> None:
    exception = {
        "scope": "src/volcano_sdk/auth.py:login",
        "rule": "S603",
        "rationale": "self-authorized",
        "evidence": "none",
        "approved_by": "self",
        "approved_at": "2026-09-23",
        "approval_evidence": "none",
    }

    assert "unapproved quality exception record" in check_comments(
        tmp_path, set(), [exception]
    )


def test_unused_reviewed_exception_fails(tmp_path: Path) -> None:
    assert (
        "unused exception: scripts/generate_openapi.py:generate S603"
        in check_comments(tmp_path, set(), [])
    )


def test_reviewed_warning_filter_must_remain_exact(tmp_path: Path) -> None:
    name = "src/volcano_sdk/_tests/test_durable_authoring.py"
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    exceptions = cast(
        "list[dict[str, str]]",
        json.loads((ROOT / "maintainers/quality-exceptions.json").read_text()),
    )
    unused = (
        "unused exception: src/volcano_sdk/_tests/test_durable_authoring.py:pytestmark "
        "pytest.filterwarnings"
    )
    assignment = f"pytestmark = pytest.mark.filterwarnings({REVIEWED_WARNING!r})"
    _ = source.write_text(f"import pytest\n{assignment}\n")
    assert unused not in check_comments(tmp_path, {name}, exceptions)

    _ = source.write_text(
        "import pytest\npytestmark = pytest.mark.filterwarnings('ignore')\n"
    )
    assert unused in check_comments(tmp_path, {name}, exceptions)


def test_native_expected_errors_are_limited_to_invalid_fixtures(tmp_path: Path) -> None:
    name = "src/volcano_sdk/_tests/fixtures/invalid_arguments.py"
    target = tmp_path / name
    target.parent.mkdir(parents=True)
    source = (
        "value: str = 1  # type: ignore[assignment]  "
        "# pyright: ignore[reportAssignmentType]\n"
    )
    _ = target.write_text(source, encoding="utf-8")

    errors = check_comments(tmp_path, {name}, [])

    assert not any("forbidden suppression" in error for error in errors)
    assert not any("outside diagnostic fixture" in error for error in errors)


@pytest.mark.parametrize(
    "source",
    [
        "import subprocess as runner  # ruff: ignore[S404]\n",
        "from subprocess import run  # ruff: ignore[S404]\n",
        "import subprocess, sys  # ruff: ignore[S404]\n",
        "def changed_scope():\n    import subprocess  # ruff: ignore[S404]\n",
        "import subprocess\nvalue = 1  # ruff: ignore[S404]\n",
    ],
)
def test_subprocess_import_exception_requires_its_exact_syntax(
    tmp_path: Path, source: str
) -> None:
    name = "scripts/generate_openapi.py"
    target = tmp_path / name
    target.parent.mkdir(parents=True)
    _ = target.write_text(source, encoding="utf-8")

    errors = check_comments(tmp_path, {name}, [])

    assert any("unapproved S404" in error for error in errors)
    assert (
        "unused exception: scripts/generate_openapi.py:import:subprocess S404" in errors
    )


def test_reviewed_subprocess_import_cannot_be_repeated(tmp_path: Path) -> None:
    name = "scripts/generate_openapi.py"
    target = tmp_path / name
    target.parent.mkdir(parents=True)
    _ = target.write_text(
        "import subprocess  # ruff: ignore[S404]\n" * 2, encoding="utf-8"
    )

    errors = check_comments(tmp_path, {name}, [])

    assert any("repeated S404" in error for error in errors)


def test_recorded_callback_erasure_is_limited_to_its_declaration(
    tmp_path: Path,
) -> None:
    name = "src/volcano_sdk/_realtime_callbacks.py"
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    declaration = "DynamicCallback: TypeAlias = Callable[..., object]"
    _ = source.write_text(f"{declaration}  # type: ignore[explicit-any]\n")

    errors = check_comments(tmp_path, {name}, [])

    assert not any("type ignore outside" in error for error in errors)
    assert f"unused exception: {name}:DynamicCallback mypy.explicit-any" not in errors


@pytest.mark.parametrize(
    "statement",
    [
        "OtherCallback: TypeAlias = Callable[..., object]",
        "DynamicCallback: TypeAlias = Callable[..., object]; other: Any = 1",
        "DynamicCallback = Callable[..., object]",
        "DynamicCallback: TypeAlias = Any",
        "DynamicCallback: TypeAlias = Callable[..., Any]",
        "def callback():\n    DynamicCallback: TypeAlias = Callable[..., object]",
    ],
)
def test_callback_erasure_cannot_expand_to_another_type_or_scope(
    tmp_path: Path, statement: str
) -> None:
    name = "src/volcano_sdk/_realtime_callbacks.py"
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    _ = source.write_text(f"{statement}  # type: ignore[explicit-any]\n")

    assert any(
        "type ignore outside diagnostic fixture" in error
        for error in check_comments(tmp_path, {name}, [])
    )


def test_callback_erasure_cannot_hide_another_error_code(tmp_path: Path) -> None:
    name = "src/volcano_sdk/_realtime_callbacks.py"
    source = tmp_path / name
    source.parent.mkdir(parents=True)
    declaration = "DynamicCallback: TypeAlias = Callable[..., object]"
    _ = source.write_text(f"{declaration}  # type: ignore[explicit-any,assignment]\n")

    assert any(
        "type ignore outside diagnostic fixture" in error
        for error in check_comments(tmp_path, {name}, [])
    )


@pytest.mark.parametrize(
    ("name", "scope", "method"),
    [
        ("_auth_context", "auth_context", "_auth_context"),
        ("_client_context", "facade_context", "_facade_context"),
    ],
)
def test_private_factory_exception_accepts_only_the_compatibility_call(
    tmp_path: Path, name: str, scope: str, method: str
) -> None:
    path = f"src/volcano_sdk/{name}.py"
    target = tmp_path / path
    target.parent.mkdir(parents=True)
    directive = (
        "# ruff: ignore[private-member-access] # pyright: ignore[reportPrivateUsage]"
    )
    _ = target.write_text(
        f"def {scope}(client):\n    return client.{method}()  {directive}\n",
        encoding="utf-8",
    )

    errors = check_comments(tmp_path, {path}, [])

    assert not any("forbidden suppression" in error for error in errors)
    assert not any("outside diagnostic fixture" in error for error in errors)
    assert not any(f"unused exception: {path}" in error for error in errors)


@pytest.mark.parametrize(
    ("scope", "statement", "directive"),
    [
        ("facade_context", "return client._other()", "reportPrivateUsage"),
        ("other_context", "return client._facade_context()", "reportPrivateUsage"),
        ("facade_context", "return client._facade_context(1)", "reportPrivateUsage"),
        (
            "facade_context",
            "return client._facade_context()",
            "reportPrivateUsage, reportAny",
        ),
    ],
)
def test_private_factory_exception_cannot_expand(
    tmp_path: Path, scope: str, statement: str, directive: str
) -> None:
    path = "src/volcano_sdk/_client_context.py"
    target = tmp_path / path
    target.parent.mkdir(parents=True)
    comment = f"# ruff: ignore[private-member-access] # pyright: ignore[{directive}]"
    _ = target.write_text(
        f"def {scope}(client):\n    {statement}  {comment}\n", encoding="utf-8"
    )

    errors = check_comments(tmp_path, {path}, [])

    assert any("forbidden suppression" in error for error in errors)
    assert any("pyright ignore outside diagnostic fixture" in error for error in errors)
