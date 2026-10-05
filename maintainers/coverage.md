# Runtime coverage

`uv run --locked poe coverage` measures every handwritten runtime module under `src/volcano_sdk`,
including unimported files and namespace directories. Native coverage.py
configuration requires 100% line and branch coverage. `poe quality` includes
this task, and CI preserves `reports/coverage.json` for each quality run.

The generated OpenAPI client, private `_tests` package, and declaration-only
code are excluded. Coverage
pragmas cannot suppress missing lines or branches. Tests exercise this policy
with unimported modules, missing branches, and ineffective pragma comments.
Examples, generator tooling, package contents, and installed consumers have
separate smoke and gate tests; they are outside runtime coverage.

Coverage runs in an isolated Python 3.12.14 environment with the same lockfile.
The ordinary test task and all other quality checks still run on the selected
Python version, including every supported version from 3.11 through 3.14 in CI.
uv's isolation keeps coverage from replacing that interpreter or its environment.

The fixed coverage interpreter avoids incorrect async branch attribution on
Python 3.11. With coverage.py 7.16.1, both `ctrace` and `pytrace` report the
unexecuted raise below as covered and the executed false exit as missing.
Python 3.12 reports those outcomes correctly. Run this with `coverage run
--branch` and `coverage report -m` to reproduce:

```python
import asyncio


async def finish(error):
    async with asyncio.Lock():
        if error is not None:
            raise error


asyncio.run(finish(None))
```

Native references: [coverage configuration](https://coverage.readthedocs.io/en/latest/config.html),
[pytest-cov configuration](https://pytest-cov.readthedocs.io/en/latest/config.html),
and [uv isolated execution](https://docs.astral.sh/uv/reference/cli/#uv-run--isolated).
