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
LOCK_SHA256 = "715cf5a0c1a93b2b77b4c63ed739dc9fa760276d43c25756230b762febab70a6"
TYPE_FIXTURES = {
    "src/volcano_sdk/_tests/typing/durable_callbacks.py",
    "src/volcano_sdk/_tests/typing/durable_configuration.py",
    "src/volcano_sdk/_tests/typing/durable_logger.py",
    "src/volcano_sdk/_tests/typing/mypy_correctness.py",
    "src/volcano_sdk/_tests/typing/realtime_subscriptions.py",
    "src/volcano_sdk/_tests/typing/transport.py",
    "src/volcano_sdk/_tests/fixtures/invalid_arguments.py",
    "src/volcano_sdk/_tests/fixtures/invalid_callbacks.py",
    "src/volcano_sdk/_tests/fixtures/invalid_realtime_callback.py",
    "src/volcano_sdk/_tests/fixtures/invalid_wait_options.py",
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
    "c99ab5004030aac824f434ab55626e40a8a0899867e77960c5dc7bbc0a0e247c"
)
CALLBACK_SCOPE = "src/volcano_sdk/_realtime_callbacks.py:DynamicCallback"
CALLBACK_RULE = "mypy.explicit-any"
CALLBACK_DECLARATION = ast.dump(
    ast.parse("DynamicCallback: TypeAlias = Callable[..., object]").body[0],
    include_attributes=False,
)
PRIVATE_CONTEXT_FACTORIES = {
    "src/volcano_sdk/_auth_context.py": ("auth_context", "_auth_context"),
    "src/volcano_sdk/_client_context.py": ("facade_context", "_facade_context"),
}
PRIVATE_CONTEXT_RULE = "basedpyright.reportPrivateUsage"
APPROVED_RULES = {
    *{
        (f"{name}:{scope}", rule)
        for name, (scope, _) in PRIVATE_CONTEXT_FACTORIES.items()
        for rule in ("SLF001", PRIVATE_CONTEXT_RULE)
    },
    (CALLBACK_SCOPE, CALLBACK_RULE),
    ("scripts/generate_openapi.py:generate", "S603"),
    (
        "src/volcano_sdk/_tests/test_durable_authoring.py:pytestmark",
        "pytest.filterwarnings",
    ),
    ("scripts/generate_openapi.py:import:subprocess", "S404"),
    ("tests/unit/test_dependency_audit.py:import:subprocess", "S404"),
    ("tests/unit/test_generation.py:import:subprocess", "S404"),
    ("tests/unit/test_mutation_results.py:import:subprocess", "S404"),
    ("tests/unit/test_quality_configuration.py:import:subprocess", "S404"),
    ("tests/unit/test_test_integrity.py:import:subprocess", "S404"),
}
RULE_NAMES = {
    "private-member-access": "SLF001",
    "suspicious-subprocess-import": "S404",
    "subprocess-without-shell-equals-true": "S603",
}
WARNING_PREFIX = "ignore:'asyncio.iscoroutinefunction' is deprecated"
REVIEWED_WARNING = f"{WARNING_PREFIX}:{DeprecationWarning.__name__}"
REVIEWED_WARNING_FILTER = ast.dump(
    ast.parse(f"pytestmark = pytest.mark.filterwarnings({REVIEWED_WARNING!r})").body[0],
    include_attributes=False,
)
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
PYRIGHT_IGNORE = re.compile(r"\bpyright:\s*ignore\[[A-Za-z0-9, ]+\]", re.IGNORECASE)
RUFF_IGNORE = re.compile(r"\bruff:\s*ignore\[([A-Z0-9, -]+)\]", re.IGNORECASE)


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


def suppression_scope(source: str, line: int) -> str | None:
    """Identify the exact function or subprocess import owning a directive.

    Returns:
        The reviewed syntax scope, if present.

    """
    for node in ast.parse(source).body:
        if (
            isinstance(node, ast.Import)
            and node.lineno == line
            and len(node.names) == 1
            and node.names[0].name == "subprocess"
            and node.names[0].asname is None
        ):
            return "import:subprocess"
    return enclosing_function(source, line)


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
    scope = f"{name}:{suppression_scope(source, token.start[0])}"
    for label in matches[0].group(1).replace(" ", "").split(","):
        rule = RULE_NAMES.get(label.lower(), label.upper())
        errors.extend(check_rule((scope, rule), location, approved, used))
    return errors


def callback_exception(name: str, source: str, token: tokenize.TokenInfo) -> bool:
    """Identify the sole callback argument-erasure declaration.

    Returns:
        Whether the exact declaration carries its reviewed mypy diagnostic.

    """
    if (name, token.string) != (
        CALLBACK_SCOPE.split(":", maxsplit=1)[0],
        "# type: ignore[explicit-any]",
    ):
        return False
    statements = [
        node for node in ast.parse(source).body if node.lineno == token.start[0]
    ]
    return (
        len(statements) == 1
        and ast.dump(statements[0], include_attributes=False) == CALLBACK_DECLARATION
    )


def check_type_comment(
    name: str,
    source: str,
    token: tokenize.TokenInfo,
    approved: set[tuple[str, str]],
    used: set[tuple[str, str]],
) -> list[str]:
    """Limit native type expectations to fixtures and one callback boundary.

    Returns:
        Unreviewed or repeated type-suppression errors.

    """
    if not TYPE_IGNORE.search(token.string) or name in TYPE_FIXTURES:
        return []
    location = f"{name}:{token.start[0]}"
    if not callback_exception(name, source, token):
        return [f"{location}: type ignore outside diagnostic fixture"]
    return check_rule((CALLBACK_SCOPE, CALLBACK_RULE), location, approved, used)


def private_factory_exception(
    name: str, source: str, token: tokenize.TokenInfo
) -> bool:
    """Match the two private calls that preserve direct facade construction.

    Returns:
        Whether this comment annotates the exact approved factory call.

    """
    expected = PRIVATE_CONTEXT_FACTORIES.get(name)
    if expected is None:
        return False
    scope, method = expected
    if enclosing_function(source, token.start[0]) != scope:
        return False
    statement = source.splitlines()[token.start[0] - 1].split("#", maxsplit=1)[0]
    return statement.strip() == f"return client.{method}()" and token.string == (
        "# ruff: ignore[private-member-access] # pyright: ignore[reportPrivateUsage]"
    )


def check_pyright_comment(
    name: str,
    source: str,
    token: tokenize.TokenInfo,
    approved: set[tuple[str, str]],
    used: set[tuple[str, str]],
) -> tuple[list[str], str]:
    """Limit native private-access exceptions to their two compatibility adapters.

    Returns:
        Violations and the comment remaining after a recognized native exception.

    """
    if not PYRIGHT_IGNORE.search(token.string):
        return [], token.string
    if name in TYPE_FIXTURES and TYPE_IGNORE.search(token.string):
        return [], PYRIGHT_IGNORE.sub("", token.string)
    location = f"{name}:{token.start[0]}"
    if private_factory_exception(name, source, token):
        scope = f"{name}:{enclosing_function(source, token.start[0])}"
        return (
            check_rule((scope, PRIVATE_CONTEXT_RULE), location, approved, used),
            PYRIGHT_IGNORE.sub("", token.string),
        )
    return [f"{location}: pyright ignore outside diagnostic fixture"], token.string


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
    errors, remaining = check_pyright_comment(name, source, token, approved, used)
    if FORBIDDEN.search(remaining):
        errors.append(f"{location}: forbidden suppression")
    errors.extend(check_type_comment(name, source, token, approved, used))
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
        if (
            name == "src/volcano_sdk/_tests/test_durable_authoring.py"
            and sum(
                ast.dump(statement, include_attributes=False) == REVIEWED_WARNING_FILTER
                for statement in ast.parse(source).body
            )
            == 1
        ):
            used.add((f"{name}:pytestmark", "pytest.filterwarnings"))
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
