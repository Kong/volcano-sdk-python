"""Guard native quality configuration and tracked Python code inclusion."""

from __future__ import annotations

import ast
import io
import json
import os
import re
import sys
import tokenize
import tomllib
from pathlib import Path
from typing import cast

ROOTS = {"src", "tests", "scripts", "features", "typings"}
CONFIG_NAMES = {
    "pyproject.toml",
    "mypy.ini",
    ".ruff.toml",
    "ruff.toml",
    "pyrightconfig.json",
    "pytest.ini",
    ".coveragerc",
    "tox.ini",
}
SUPPRESSIONS = (
    re.compile(r"#\s*(?:ruff:\s*ignore\[|noqa\b|pyright:\s*ignore)"),
    re.compile(r"#\s*(?:type:\s*ignore|pragma:\s*no cover)"),
)
DECLARATION_EXCLUSION = r"^\s*(((async )?def .*?)?[\])]+(\s*->.*?)?:\s*)?\.\.\.\s*(#|$)"


def table(value: object) -> dict[str, object]:
    """Require a TOML or JSON mapping with string keys.

    Returns:
        The validated mapping.

    Raises:
        TypeError: If the value is not a string-keyed table.

    """
    if not isinstance(value, dict):
        msg = "Expected a string-keyed quality configuration table"
        raise TypeError(msg)
    entries = cast("dict[object, object]", value)
    if not all(isinstance(key, str) for key in entries):
        msg = "Expected a string-keyed quality configuration table"
        raise TypeError(msg)
    return cast("dict[str, object]", value)


def nested(root: dict[str, object], *keys: str) -> object:
    """Read a configuration key without accepting missing intermediate tables.

    Returns:
        The selected configuration value.

    """
    current: object = root
    for key in keys:
        current = table(current)[key]
    return current


def require_equal(config: dict[str, object], expected: object, *keys: str) -> list[str]:
    """Check one non-negotiable native-tool setting.

    Returns:
        An error when the value differs or is missing.

    """
    label = ".".join(keys)
    try:
        actual = nested(config, *keys)
    except (KeyError, TypeError):
        return [f"Missing quality setting: {label}"]
    return [] if actual == expected else [f"Weakened quality setting: {label}"]


def configuration_errors(config: dict[str, object]) -> list[str]:
    """Protect native thresholds, inclusion, and the canonical task.

    Returns:
        Native configuration violations.

    """
    checks: list[tuple[tuple[str, ...], object]] = [
        (("tool", "mypy", "files"), ["src", "tests", "scripts", "features", "typings"]),
        (("tool", "mypy", "exclude"), ["src/volcano_sdk/_generated/"]),
        (
            ("tool", "basedpyright", "include"),
            ["src", "tests", "scripts", "features", "typings"],
        ),
        (("tool", "basedpyright", "exclude"), ["src/volcano_sdk/_generated"]),
        (("tool", "ruff", "extend-exclude"), ["src/volcano_sdk/_generated"]),
        (("tool", "ruff", "lint", "preview"), True),
        (("tool", "ruff", "lint", "mccabe", "max-complexity"), 5),
        (("tool", "coverage", "run", "branch"), True),
        (("tool", "coverage", "run", "source_dirs"), ["src/volcano_sdk"]),
        (("tool", "coverage", "run", "omit"), ["src/volcano_sdk/_generated/*"]),
        (("tool", "coverage", "report", "fail_under"), 100),
        (
            ("tool", "coverage", "report", "exclude_lines"),
            [DECLARATION_EXCLUSION, r"if (typing\.)?TYPE_CHECKING:"],
        ),
        (("tool", "coverage", "report", "partial_branches"), []),
        (("tool", "mutmut", "source_paths"), ["src/volcano_sdk"]),
        (("tool", "mutmut", "do_not_mutate"), ["src/volcano_sdk/_generated/*"]),
        (("tool", "pytest", "ini_options", "strict"), True),
        (("tool", "pytest", "ini_options", "filterwarnings"), ["error"]),
        (("tool", "poe", "tasks", "quality"), ["checks", "mutation"]),
        (
            ("tool", "poe", "tasks", "checks"),
            [
                "policy",
                "audit",
                "generated",
                "lint",
                "format-check",
                "types",
                "test",
                "coverage",
                "contract-check",
                "package-check",
                "package-extras",
            ],
        ),
        (("tool", "poe", "tasks", "policy"), "bash scripts/quality_policy.sh"),
        (("tool", "poe", "tasks", "audit"), "bash scripts/audit_dependencies.sh"),
        (("tool", "poe", "tasks", "generated"), "python -m scripts.check_openapi"),
        (("tool", "poe", "tasks", "lint"), "ruff check ."),
        (("tool", "poe", "tasks", "format-check"), "ruff format --check ."),
        (("tool", "poe", "tasks", "mypy"), "mypy"),
        (("tool", "poe", "tasks", "basedpyright"), "basedpyright"),
        (
            ("tool", "poe", "tasks", "test"),
            "pytest tests/unit -q --junitxml=reports/unit.xml",
        ),
        (("tool", "poe", "tasks", "mutation"), "bash scripts/mutation.sh"),
    ]
    errors = [
        error
        for keys, expected in checks
        for error in require_equal(config, expected, *keys)
    ]
    lint = table(nested(config, "tool", "ruff", "lint"))
    if "ALL" not in table_list(lint.get("select")):
        errors.append("Ruff ALL selection is required")
    if "only_mutate" in table(nested(config, "tool", "mutmut")):
        errors.append("Mutation source exclusions are forbidden")
    coverage_args = [
        "uv",
        "run",
        "--locked",
        "--isolated",
        "--python",
        "3.12",
        "pytest",
        "tests/unit",
        "-q",
        "--cov",
        "--cov-config=pyproject.toml",
        "--cov-report=term-missing",
        "--cov-report=json:reports/coverage.json",
        "--junitxml=reports/coverage-unit.xml",
    ]
    coverage_task = nested(config, "tool", "poe", "tasks", "coverage")
    if not isinstance(coverage_task, str) or coverage_task.split() != coverage_args:
        errors.append("Weakened quality setting: tool.poe.tasks.coverage")
    return errors


def table_list(value: object) -> list[str]:
    """Return a string list only when every member is a string.

    Returns:
        The validated list, or an empty list for invalid values.

    """
    if not isinstance(value, list):
        return []
    items = cast("list[object]", value)
    if not all(isinstance(item, str) for item in items):
        return []
    return cast("list[str]", value)


def tracked_errors(paths: list[Path]) -> list[str]:
    """Reject code outside configured roots and nested override files.

    Returns:
        Tracked-file inventory violations.

    """
    errors: list[str] = []
    for path in paths:
        if path.name in CONFIG_NAMES and path != Path("pyproject.toml"):
            errors.append(f"Nested quality configuration: {path}")
        if path.suffix in {".py", ".pyi"} and path.parts[0] not in ROOTS:
            errors.append(f"Python code outside checked roots: {path}")
        if (
            path.suffix in {".py", ".pyi"}
            and path.parts[0] == "src"
            and path.parts[1] != "volcano_sdk"
        ):
            errors.append(f"Runtime outside coverage source: {path}")
    return errors


def source_suppressions(path: Path) -> list[tuple[int, str]]:
    """Find real comment directives without matching negative fixture strings.

    Returns:
        Suppression directives in maintained source.

    """
    content = path.read_bytes()
    tokens = tokenize.tokenize(io.BytesIO(content).readline)
    return [
        (token.start[0], token.string)
        for token in tokens
        if token.type == tokenize.COMMENT
        and any(pattern.search(token.string) for pattern in SUPPRESSIONS)
    ]


def enclosing_function(path: Path, line: int) -> str:
    """Identify the narrow function scope of a suppression.

    Returns:
        The enclosing function name or an empty string.

    """
    tree = ast.parse(path.read_text(encoding="utf-8"))
    functions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.lineno <= line <= (node.end_lineno or node.lineno)
    ]
    return (
        min(functions, key=lambda node: node.end_lineno or node.lineno).name
        if functions
        else ""
    )


def approved_suppressions(exceptions: list[object]) -> dict[tuple[str, str, str], int]:
    """Validate exception records and index their exact source scopes.

    Returns:
        The approved directives, initially unused.

    Raises:
        TypeError: If a record lacks an exact rule or path/symbol scope.
        ValueError: If a record duplicates another exception.

    """
    allowed: dict[tuple[str, str, str], int] = {}
    for raw in exceptions:
        entry = table(raw)
        scope = entry.get("scope")
        rule = entry.get("rule")
        if not isinstance(scope, str) or not isinstance(rule, str) or ":" not in scope:
            msg = "Invalid quality exception record"
            raise TypeError(msg)
        evidence_fields = (
            "rationale",
            "evidence",
            "approved_by",
            "approved_at",
            "approval_evidence",
        )
        if any(
            not isinstance(entry.get(field), str) or not entry[field]
            for field in evidence_fields
        ):
            msg = "Quality exception lacks approval evidence"
            raise TypeError(msg)
        path, symbol = scope.split(":", maxsplit=1)
        key = (path, symbol, rule)
        if key in allowed:
            msg = f"Duplicate quality exception: {scope}:{rule}"
            raise ValueError(msg)
        allowed[key] = 0
    return allowed


def check_source_suppressions(
    path: Path, allowed: dict[tuple[str, str, str], int]
) -> list[str]:
    """Match a source file's directives to approved scopes.

    Returns:
        Unapproved directives.

    """
    errors: list[str] = []
    for line, directive in source_suppressions(path):
        rules = re.findall(r"[A-Z]+\d+", directive)
        symbol = enclosing_function(path, line)
        key = (str(path), symbol, rules[0]) if len(rules) == 1 else None
        if key is None or key not in allowed:
            errors.append(f"Undocumented suppression: {path}: {directive}")
        else:
            allowed[key] += 1
    return errors


def suppression_errors(paths: list[Path], exceptions: list[object]) -> list[str]:
    """Require exact documented exceptions for maintained-source directives.

    Returns:
        Unapproved or unused exception entries.

    """
    allowed = approved_suppressions(exceptions)
    source_paths = (
        path
        for path in paths
        if path.suffix == ".py"
        and "_generated" not in path.parts
        and path.parts[0] in {"src", "scripts", "features"}
    )
    errors = [
        error
        for path in source_paths
        for error in check_source_suppressions(path, allowed)
    ]
    errors.extend(
        f"Unused or duplicated quality exception: {path}:{symbol}:{rule}"
        for (path, symbol, rule), count in allowed.items()
        if count != 1
    )
    return errors


def main() -> int:
    """Check tracked inventory, native settings, and approved suppressions.

    Returns:
        Zero only when the quality policy is intact.

    Raises:
        TypeError: If the exception registry is malformed.

    """
    raw_paths = sys.stdin.buffer.read().split(b"\0")
    paths = [Path(os.fsdecode(raw)) for raw in raw_paths if raw]
    config_text = Path("pyproject.toml").read_text(encoding="utf-8")
    config = cast("object", tomllib.loads(config_text))
    exception_text = Path("maintainers/quality-exceptions.json").read_text(
        encoding="utf-8"
    )
    exceptions = cast("object", json.loads(exception_text))
    if not isinstance(exceptions, list):
        msg = "Expected a quality-exception list"
        raise TypeError(msg)
    errors = (
        configuration_errors(table(config))
        + tracked_errors(paths)
        + suppression_errors(paths, cast("list[object]", exceptions))
    )
    for error in errors:
        print(error, file=sys.stderr)
    if not errors:
        print(f"Quality policy covers {len(paths)} tracked paths")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
