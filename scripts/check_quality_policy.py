"""Attest to quality properties the native tools cannot express themselves."""

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
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from collections.abc import Iterable

GENERATED = "src/volcano_sdk/_generated"
ROOTS = ["src", "tests", "scripts", "features", "typings"]
TYPE_FIXTURES = {
    "tests/typing/contract_steps.py",
    "tests/typing/durable_callbacks.py",
    "tests/typing/durable_configuration.py",
    "tests/typing/durable_logger.py",
    "tests/typing/mypy_correctness.py",
    "tests/typing/realtime_subscriptions.py",
    "tests/typing/transport.py",
    "tests/unit/fixtures/invalid_arguments.py",
    "tests/unit/fixtures/invalid_callbacks.py",
    "tests/unit/fixtures/invalid_realtime_callback.py",
    "tests/unit/fixtures/invalid_wait_options.py",
}
CONFIG_NAMES = {
    "pyproject.toml",
    "ruff.toml",
    ".ruff.toml",
    "mypy.ini",
    ".mypy.ini",
    "pytest.toml",
    ".pytest.toml",
    "pytest.ini",
    "tox.ini",
    "setup.cfg",
    ".coveragerc",
}
GLOBAL_RUFF_IGNORES = {
    "CPY001",
    "COM812",
    "COM819",
    "D203",
    "D206",
    "D213",
    "D300",
    "E111",
    "E114",
    "E117",
    "ISC001",
    "ISC002",
    "Q000",
    "Q001",
    "Q002",
    "Q003",
    "W191",
}
PER_FILE_RUFF_IGNORES = {
    "features/**/*.py": {"D", "INP001", "S101"},
    "scripts/*.py": {"T201"},
    "src/volcano_sdk/auth.py": {"SLF001"},
    "src/volcano_sdk/database.py": {"SLF001"},
    "src/volcano_sdk/durable.py": {"SLF001"},
    "src/volcano_sdk/durable_authoring.py": {"ANN401"},
    "src/volcano_sdk/functions.py": {"SLF001"},
    "src/volcano_sdk/logs.py": {"SLF001"},
    "src/volcano_sdk/locks.py": {"SLF001"},
    "src/volcano_sdk/realtime.py": {"ANN401", "SLF001"},
    "src/volcano_sdk/storage.py": {"SLF001"},
    "tests/**/*.py": {
        "ANN401",
        "D",
        "INP001",
        "PLR2004",
        "S101",
        "S105",
        "S106",
        "SLF001",
    },
}
CHECKS = [
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
]
COVERAGE_PARTS = (
    "uv run --locked --isolated --python 3.12 pytest -c pyproject.toml",
    "tests/unit -q --cov --cov-config=pyproject.toml --cov-report=term-missing",
    "--cov-report=json:reports/coverage.json --junitxml=reports/coverage-unit.xml",
)
CONTRACT_FIXTURE = "${POE_ROOT}/tests/fixtures/sdk-contract-dry-run.json"
PACKAGE_EXTRAS_PARTS = (
    "tox run -c pyproject.toml --recreate -e",
    "package-base,package-min-typing,package-durable,package-types",
)
REQUIRED_TASKS: dict[str, object] = {
    "build": "uv build --no-sources --require-hashes",
    "policy": "bash scripts/check_quality_policy.sh",
    "audit": "bash scripts/audit_dependencies.sh",
    "generated": "python -m scripts.check_openapi",
    "lint": "ruff check --config pyproject.toml .",
    "format-check": "ruff format --check --config pyproject.toml .",
    "types": ["mypy", "basedpyright"],
    "mypy": "mypy --config-file pyproject.toml",
    "basedpyright": "basedpyright --project pyproject.toml",
    "test": "pytest -c pyproject.toml tests/unit -q --junitxml=reports/unit.xml",
    "coverage": " ".join(COVERAGE_PARTS),
    "contract-check": {
        "sequence": [
            {"cmd": "chmod 600 tests/fixtures/sdk-contract-dry-run.json"},
            {"cmd": "behave features/contract --dry-run --no-snippets"},
        ],
        "env": {"VOLCANO_SDK_CONTRACT_FIXTURE": CONTRACT_FIXTURE},
    },
    "package-check": {
        "interpreter": "bash",
        "shell": """set -euo pipefail
package_dir="$(mktemp -d)"
trap 'rm -rf "$package_dir"' EXIT
poe build --out-dir "$package_dir"
bash scripts/check_package.sh "" "$package_dir"
""",
    },
    "package-extras": {"cmd": " ".join(PACKAGE_EXTRAS_PARTS)},
    "mutation": "bash scripts/mutation.sh",
    "mutation-full": "MUTATION_FULL=1 bash scripts/mutation.sh",
}
REQUIRED = {
    ("mypy", "files"): ROOTS,
    ("mypy", "strict"): True,
    ("mypy", "exclude"): [f"{GENERATED}/"],
    ("basedpyright", "include"): ROOTS,
    ("basedpyright", "exclude"): [GENERATED],
    ("basedpyright", "typeCheckingMode"): "strict",
    ("ruff", "lint", "preview"): True,
    ("ruff", "lint", "mccabe", "max-complexity"): 5,
    ("coverage", "run", "branch"): True,
    ("coverage", "run", "source_dirs"): ["src/volcano_sdk"],
    ("coverage", "run", "omit"): [f"{GENERATED}/*"],
    ("coverage", "report", "fail_under"): 100,
    ("coverage", "report", "partial_branches"): [],
    ("pytest", "ini_options", "strict"): True,
    ("pytest", "ini_options", "empty_parameter_set_mark"): "fail_at_collect",
    ("poe", "tasks", "quality"): ["checks", "mutation"],
    ("poe", "tasks", "checks"): CHECKS,
}
FORBIDDEN = re.compile(
    r"""
    \b(?:noqa|nosec|pragma:\s*no\s+(?:cover|branch))\b
    |\b(?:pyright:|mypy:|coverage:)
    |\b(?:fmt:|isort:)\s*(?:off|skip)\b
    |\bpylint:\s*disable\b
    """,
    re.IGNORECASE | re.VERBOSE,
)
TYPE_IGNORE = re.compile(r"\btype:\s*ignore(?:\[[^]]+\])?(?=$|[\s#])", re.IGNORECASE)
RUFF_IGNORE = re.compile(r"\bruff:\s*ignore\[([A-Z0-9, ]+)\]", re.IGNORECASE)


def setting(tree: dict[str, object], path: tuple[str, ...]) -> object:
    """Read one native setting without inventing another config parser.

    Returns:
        The configured value, or None when absent.

    """
    value: object = tree
    for key in path:
        if not isinstance(value, dict):
            return None
        value = cast("object", value.get(key))
    return value


def check_ruff_ignores(lint: dict[str, object]) -> list[str]:
    """Protect reviewed Ruff rule exceptions.

    Returns:
        Deviations from the approved ignore scopes.

    """
    errors: list[str] = []
    if "ALL" not in cast("list[str]", lint.get("select", [])):
        errors.append("Ruff ALL rules disabled")
    if set(cast("list[str]", lint.get("ignore", []))) != GLOBAL_RUFF_IGNORES:
        errors.append("Ruff global ignores changed")
    per_file = cast("dict[str, list[str]]", lint.get("per-file-ignores", {}))
    if {
        scope: set(rules) for scope, rules in per_file.items()
    } != PER_FILE_RUFF_IGNORES:
        errors.append("Ruff per-file ignores changed")
    return errors


def check_config(config: dict[str, object]) -> list[str]:
    """Reject changes that weaken native tool coverage or thresholds.

    Returns:
        Config policy violations.

    """
    tool = cast("dict[str, object]", config.get("tool", {}))
    errors = [
        f"policy setting changed: {'.'.join(path)}"
        for path, expected in REQUIRED.items()
        if setting(tool, path) != expected
    ]
    lint = cast("dict[str, object]", setting(tool, ("ruff", "lint")))
    errors.extend(check_ruff_ignores(lint))
    errors.extend(
        f"quality task changed: {name}"
        for name, expected in REQUIRED_TASKS.items()
        if setting(tool, ("poe", "tasks", name)) != expected
    )
    if setting(tool, ("mypy", "overrides")) is not None:
        errors.append("nested Mypy override")
    if setting(tool, ("basedpyright", "ignore")) or setting(
        tool, ("coverage", "report", "exclude_also")
    ):
        errors.append("Additional type or coverage exclusions")
    return errors


def check_inventory(root: Path, tracked: set[str], linted: set[str]) -> list[str]:
    """Compare Git's handwritten files to Ruff's native file inventory.

    Returns:
        Nested configs and omitted Python files.

    """
    nested = {
        name
        for name in tracked
        if name != "pyproject.toml" and Path(name).name in CONFIG_NAMES
    }
    handwritten = {
        name
        for name in tracked
        if name.endswith((".py", ".pyi")) and not name.startswith(f"{GENERATED}/")
    }
    missing = {name for name in handwritten if not (root / name).is_file()}
    return [
        *(f"nested tool configuration: {name}" for name in sorted(nested)),
        *(f"tracked Python file is missing: {name}" for name in sorted(missing)),
        *(
            f"Ruff omitted tracked Python file: {name}"
            for name in sorted(handwritten - missing - linted)
        ),
    ]


def enclosing_function(source: str, line: int) -> str | None:
    """Locate a reviewed suppression's containing function.

    Returns:
        Its function name when present.

    """
    nodes = (
        node
        for node in ast.walk(ast.parse(source))
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.end_lineno is not None
        and node.lineno <= line <= node.end_lineno
    )
    nearest = max(nodes, key=lambda node: node.lineno, default=None)
    return nearest.name if nearest is not None else None


def check_comment(
    source_location: tuple[str, int],
    source: str,
    comment: str,
    approved: set[tuple[str, str]],
    used: set[tuple[str, str]],
) -> list[str]:
    """Check a comment without exempting type fixtures from other rules.

    Returns:
        Suppression violations in this comment.

    """
    name, line = source_location
    location = f"{name}:{line}"
    errors = [f"{location}: forbidden suppression"] if FORBIDDEN.search(comment) else []
    if TYPE_IGNORE.search(comment) and name not in TYPE_FIXTURES:
        errors.append(f"{location}: type ignore outside diagnostic fixture")
    if "ruff:" not in comment.lower():
        return errors
    match = RUFF_IGNORE.search(comment)
    if match is None:
        return [*errors, f"{location}: unrecognized Ruff directive"]
    scope = f"{name}:{enclosing_function(source, line)}"
    keys = {(scope, code.strip().upper()) for code in match.group(1).split(",")}
    errors.extend(
        f"{location}: unapproved {rule} suppression" for _, rule in keys - approved
    )
    errors.extend(f"{location}: repeated {rule} suppression" for _, rule in keys & used)
    used.update(keys)
    return errors


def check_comments(
    root: Path, paths: Iterable[str], exceptions: list[dict[str, str]]
) -> list[str]:
    """Reject unreviewed, redundant, and misplaced suppressions.

    Returns:
        Suppression violations and unused exception records.

    """
    required = {
        "rule",
        "scope",
        "rationale",
        "evidence",
        "approved_by",
        "approved_at",
        "approval_evidence",
    }
    errors = [
        "incomplete quality exception record"
        for item in exceptions
        if not all(item.get(key) for key in required)
    ]
    approved = {(item["scope"], item["rule"]) for item in exceptions}
    if len(approved) != len(exceptions):
        errors.append("duplicate quality exception record")
    used: set[tuple[str, str]] = set()
    for name in sorted(paths):
        if (
            not name.endswith((".py", ".pyi"))
            or name.startswith(f"{GENERATED}/")
            or not (root / name).is_file()
        ):
            continue
        source = (root / name).read_text(encoding="utf-8")
        comments = (
            token
            for token in tokenize.generate_tokens(io.StringIO(source).readline)
            if token.type == tokenize.COMMENT
        )
        for token in comments:
            errors.extend(
                check_comment(
                    (name, token.start[0]), source, token.string, approved, used
                )
            )
    errors.extend(
        f"unused exception: {scope} {rule}" for scope, rule in sorted(approved - used)
    )
    return errors


def main(tracked_file: Path, linted_file: Path) -> int:
    """Report every policy violation and fail the gate.

    Returns:
        Zero only when the selected code and policy are intact.

    """
    root = Path.cwd()
    config = cast(
        "dict[str, object]",
        tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8")),
    )
    exceptions = cast(
        "list[dict[str, str]]",
        json.loads(
            (root / "maintainers/quality-exceptions.json").read_text(encoding="utf-8")
        ),
    )
    tracked = {
        os.fsdecode(path) for path in tracked_file.read_bytes().split(b"\0") if path
    }
    linted = {
        str(Path(line).resolve().relative_to(root.resolve()))
        for line in linted_file.read_text(encoding="utf-8").splitlines()
        if line.endswith((".py", ".pyi"))
    }
    errors = check_config(config)
    errors.extend(check_inventory(root, tracked, linted))
    errors.extend(check_comments(root, tracked, exceptions))
    for error in errors:
        print(error, file=sys.stderr)
    print(f"Policy checked {len(tracked)} repository files")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2])))
