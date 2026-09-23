"""Attest to native quality configuration and source-file inclusion."""

from __future__ import annotations

import ast
import hashlib
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
LOCK_SHA256 = "00e065b217d4a56575f14c38dfef8628e3f3439794743e17504532c32fdcdb14"
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
    "pyrightconfig.json",
    "basedpyrightconfig.json",
    "pytest.toml",
    ".pytest.toml",
    "pytest.ini",
    "tox.ini",
    "setup.cfg",
    ".coveragerc",
}
APPROVED_EXCEPTION_SHA256 = (
    "a00f1cb0e255bea7f8ac7ada615ae8953e3e30c20ca5580a7a41333e695bfb23"
)
APPROVED_RULES = {("scripts/generate_openapi.py:generate", "S603")}
FORBIDDEN = re.compile(
    r"""
    \b(?:noqa|nosec|pragma:\s*no\s+(?:cover|branch))\b
    |\b(?:pyright:|mypy:|coverage:)
    |\b(?:fmt:|isort:)\s*(?:off|skip|skip_file)\b
    |\byapf:\s*disable\b
    |\bpylint:\s*disable\b
    """,
    re.IGNORECASE | re.VERBOSE,
)
TYPE_IGNORE = re.compile(r"\btype:\s*ignore(?:\[[^]]+\])?(?=$|[\s#])", re.IGNORECASE)
RUFF_IGNORE = re.compile(r"\bruff:\s*ignore\[([A-Z0-9, ]+)\]", re.IGNORECASE)


def changed_paths(expected: object, actual: object, path: str) -> list[str]:
    """Show where native configuration differs from its reviewed snapshot.

    Returns:
        Changed setting paths.

    """
    if isinstance(expected, dict) and isinstance(actual, dict):
        before = cast("dict[str, object]", expected)
        after = cast("dict[str, object]", actual)
        keys = before.keys() | after.keys()
        return [
            child
            for key in sorted(keys)
            for child in changed_paths(before.get(key), after.get(key), f"{path}.{key}")
        ]
    return [path] if expected != actual else []


def check_config(config: dict[str, object], locked: dict[str, object]) -> list[str]:
    """Require an exact match to the reviewed native tool configuration.

    Returns:
        Changed native settings or lock schema.

    """
    if set(locked) != {"schema", "native_tool_config"} or locked["schema"] != 1:
        return ["invalid quality policy lock schema"]
    return changed_paths(locked["native_tool_config"], config.get("tool"), "tool")


def check_lock_bytes(data: bytes) -> list[str]:
    """Require a deliberate code change when the readable lock changes.

    Returns:
        A policy-lock error when the recorded digest differs.

    """
    return (
        ["quality policy lock digest changed"]
        if hashlib.sha256(data).hexdigest() != LOCK_SHA256
        else []
    )


def check_inventory(root: Path, tracked: set[str], linted: set[str]) -> list[str]:
    """Compare Git's handwritten Python files to Ruff's native inventory.

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
    """Find the function containing a reviewed Ruff suppression.

    Returns:
        Its name, if present.

    """
    matches = (
        node
        for node in ast.walk(ast.parse(source))
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.end_lineno is not None
        and node.lineno <= line <= node.end_lineno
    )
    nearest = max(matches, key=lambda node: node.lineno, default=None)
    return nearest.name if nearest is not None else None


def check_rule(
    key: tuple[str, str],
    location: str,
    approved: set[tuple[str, str]],
    used: set[tuple[str, str]],
) -> list[str]:
    """Check one scoped Ruff rule and mark it used.

    Returns:
        New or repeated suppression errors.

    """
    errors: list[str] = []
    if key not in approved:
        errors.append(f"{location}: unapproved {key[1]} suppression")
    if key in used:
        errors.append(f"{location}: repeated {key[1]} suppression")
    used.add(key)
    return errors


def check_ruff_comment(
    name: str,
    source: str,
    token: tokenize.TokenInfo,
    approved: set[tuple[str, str]],
    used: set[tuple[str, str]],
) -> list[str]:
    """Match a Ruff directive to its reviewed function and rule.

    Returns:
        Ruff suppression violations.

    """
    comment = token.string
    if "ruff:" not in comment.lower():
        return []
    location = f"{name}:{token.start[0]}"
    matches = list(RUFF_IGNORE.finditer(comment))
    if len(matches) != 1 or comment.lower().count("ruff:") != 1:
        return [f"{location}: unrecognized or multiple Ruff directives"]
    errors: list[str] = []
    scope = f"{name}:{enclosing_function(source, token.start[0])}"
    for rule in matches[0].group(1).replace(" ", "").upper().split(","):
        errors.extend(check_rule((scope, rule), location, approved, used))
    return errors


def check_comment(
    name: str,
    source: str,
    token: tokenize.TokenInfo,
    approved: set[tuple[str, str]],
    used: set[tuple[str, str]],
) -> list[str]:
    """Check one Python comment without exempting fixtures from other rules.

    Returns:
        Suppression violations.

    """
    location = f"{name}:{token.start[0]}"
    errors = (
        [f"{location}: forbidden suppression"] if FORBIDDEN.search(token.string) else []
    )
    if TYPE_IGNORE.search(token.string) and name not in TYPE_FIXTURES:
        errors.append(f"{location}: type ignore outside diagnostic fixture")
    errors.extend(check_ruff_comment(name, source, token, approved, used))
    return errors


def check_token(
    name: str,
    source: str,
    token: tokenize.TokenInfo,
    approved: set[tuple[str, str]],
    used: set[tuple[str, str]],
) -> list[str]:
    """Check the syntax locations that can bypass native diagnostics.

    Returns:
        Suppression violations.

    """
    if token.type == tokenize.NAME and token.string == "no_type_check":
        return [f"{name}:{token.start[0]}: forbidden type-check opt-out"]
    if token.type == tokenize.COMMENT:
        return check_comment(name, source, token, approved, used)
    return []


def check_comments(
    root: Path, paths: Iterable[str], exceptions: list[dict[str, str]]
) -> list[str]:
    """Reject all new exception records and unreviewed suppressions.

    Returns:
        Suppression violations and unused exception records.

    """
    encoded = json.dumps(exceptions, sort_keys=True, separators=(",", ":")).encode()
    errors = (
        ["unapproved quality exception record"]
        if hashlib.sha256(encoded).hexdigest() != APPROVED_EXCEPTION_SHA256
        else []
    )
    approved = APPROVED_RULES
    used: set[tuple[str, str]] = set()
    for name in sorted(paths):
        if (
            not name.endswith((".py", ".pyi"))
            or name.startswith(f"{GENERATED}/")
            or not (root / name).is_file()
        ):
            continue
        source = (root / name).read_text(encoding="utf-8")
        for token in tokenize.generate_tokens(io.StringIO(source).readline):
            errors.extend(check_token(name, source, token, approved, used))
    errors.extend(
        f"unused exception: {scope} {rule}" for scope, rule in sorted(approved - used)
    )
    return errors


def main(tracked_file: Path, linted_file: Path) -> int:
    """Run the repository-specific attestation after native tools inventory files.

    Returns:
        Zero only when all policy boundaries are intact.

    """
    root = Path.cwd()
    config = cast(
        "dict[str, object]",
        tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8")),
    )
    lock_bytes = (root / "maintainers/quality-policy.lock.json").read_bytes()
    locked = cast("dict[str, object]", json.loads(lock_bytes))
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
    errors = check_lock_bytes(lock_bytes)
    errors.extend(check_config(config, locked))
    errors.extend(check_inventory(root, tracked, linted))
    errors.extend(check_comments(root, tracked, exceptions))
    for error in errors:
        print(error, file=sys.stderr)
    print(f"Policy checked {len(tracked)} repository files")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2])))
