# Mutation testing

`uv run --locked poe quality` runs all native checks and mutates every handwritten
runtime module. CI runs `checks` and divides `mutation-full` across eight jobs;
the required `Quality Gate` checks every job and the complete runtime inventory.
The weekly full audit also runs `mutation-full` without sharding. `poe mutation`
remains a faster local diagnostic for changed modules and the lock runtime.

Mutmut's [native configuration](https://mutmut.readthedocs.io/en/latest/) lives
in `pyproject.toml`; it excludes only the generated OpenAPI client. Mutmut can
select modules by name but cannot divide a run across CI jobs or verify that
their combined results cover every tracked source module. GitHub's matrix
reports job success without checking that source inventory.
`scripts/mutation.sh` assigns Git-tracked runtime modules to shards,
`scripts/mutation_results.py` reads each shard's native metadata, and
`scripts/check_mutation_shards.py` checks that all eight reports cover each
handwritten module exactly once. The
report at `reports/mutation.json` distinguishes killed, statically invalid,
surviving, uncovered, timed-out, crashed, interrupted, and missing results.
A pytest internal error is a harness crash, not a killed mutant.
The pinned Pyrefly check rejects type-invalid realtime and auth mutants before pytest;
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
