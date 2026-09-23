# Quality policy

`uv run --locked poe quality` runs the repository's native lint, formatting,
typing, testing, coverage, package, audit, and mutation tools. `poe policy`
checks the few relationships those tools cannot express themselves: every Git
Python file appears in Ruff's [native file inventory](https://docs.astral.sh/ruff/configuration/),
the maintained roots and coverage threshold remain selected, and no nested
configuration, replaced quality-task command, expanded Ruff ignore list, or
unreviewed suppression can redirect the checks. The quality-task definitions
and existing Ruff ignore scopes are exact policy invariants; changing them
requires reviewing the policy update itself.

The policy task does not reimplement Ruff, Mypy, Basedpyright, pytest, or
coverage.py. Ruff validates active ignores with `RUF100` and `PGH003/PGH004`;
Mypy and Basedpyright reject unused and blanket type ignores. Coverage's
`source_dirs` includes unimported runtime files, so its 100% gate catches new
uncovered modules. These are the native mechanisms documented by
[Ruff](https://docs.astral.sh/ruff/rules/),
[Mypy](https://mypy.readthedocs.io/en/stable/config_file.html),
[Basedpyright](https://docs.basedpyright.com/latest/configuration/config-files/),
[pytest](https://docs.pytest.org/en/stable/reference/customize.html), and
[coverage.py](https://coverage.readthedocs.io/en/latest/source.html).

The exact files listed in `TYPE_FIXTURES` deliberately pass invalid arguments
to prove public type and runtime boundaries. Each `type: ignore[code]` there
must still mask its named Mypy diagnostic; an unnecessary ignore fails. Other
suppression directives are rejected even in those files. The one reviewed Ruff
`S603` exception lives in `quality-exceptions.json`; an absent use fails.

The generator comparison in `poe generated` verifies provenance of the
generated OpenAPI tree. The policy inventory excludes that tree only after the
generator check, and includes every other Python file in lint and type roots.
