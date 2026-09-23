# Mutation testing

`uv run --locked poe quality` runs all native checks and mutates every changed
handwritten runtime module plus the lock acquisition, guard, renewal, and worker
modules. CI uses the same `checks` and `mutation` tasks in separate jobs, then
requires both through `Quality Gate`. The weekly `poe mutation-full` task audits
every handwritten runtime module without a debt baseline.

Mutmut's [native configuration](https://mutmut.readthedocs.io/en/latest/) lives
in `pyproject.toml`; it excludes only the generated OpenAPI client. Mutmut can
select modules by name but has no Git-changed-module option and returns success
when mutants survive. `scripts/mutation.sh` selects module names from Git and
`scripts/mutation_results.py` reads only those modules' native metadata. The
report at `reports/mutation.json` distinguishes survivors, uncovered mutants,
timeouts, crashes, interrupted runs, and missing results. A pytest internal
error is a harness crash, not a killed mutant. All non-killed outcomes fail.

The full audit runs mutmut once across the entire source tree. It reports any
surviving mutants without treating them as an approved baseline. Equivalent
mutants require a reviewed, exact exception before a gate can accept them.

Ruff, Mypy, Basedpyright, pytest, and Tox tasks pass `pyproject.toml`
explicitly. Their documented config-file precedence can otherwise select a
new local config before the checked-in policy:
[Ruff](https://docs.astral.sh/ruff/configuration/),
[Mypy](https://mypy.readthedocs.io/en/stable/command_line.html),
[pytest](https://docs.pytest.org/en/stable/reference/customize.html),
[Tox](https://tox.wiki/en/latest/man/tox.1.html).
