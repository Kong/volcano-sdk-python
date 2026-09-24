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
report at `reports/mutation.json` distinguishes killed, statically invalid,
surviving, uncovered, timed-out, crashed, interrupted, and missing results.
A pytest internal error is a harness crash, not a killed mutant.
The pinned Pyrefly check rejects type-invalid realtime mutants before pytest;
the report counts these as `type_checked`, separately from test-killed mutants.
Surviving, uncovered, timed-out, crashed, and incomplete mutants still fail.
Mutmut passes pytest `-x` so a selected test's first assertion failure kills the
mutant before a later selected test can hang on the same defect. Mutants that
hang before any failure remain timeouts and fail separately.
The runner rebuilds mutmut's native test-selection cache for each gate so newly
added tests are included. Direct mutmut runs also watch Python test files for
cache invalidation.
The runner uses one mutmut child at a time because competing async mutant
processes can time out tests that kill the same mutant when run alone.
Mutmut uses its native forkserver isolation because forking from a process that
has already run asyncio tests can crash a worker before its tests report a result.
The mutation runner sets `NO_PROXY=*` for its hermetic transport tests because
macOS system-proxy discovery can abort after a fork with active threads.
The pinned pytest-order plugin runs bounded callback and presence assertions
first when mutmut's unordered test selection could otherwise reach a blocked test.

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
