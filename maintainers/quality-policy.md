# Quality policy

`uv run --locked poe quality` runs the native Ruff, mypy, basedpyright, pytest,
coverage.py, package, audit, and mutmut checks. `pyproject.toml` is their source of
truth. `quality-policy.lock.json` records the exact native tool configuration so
that changes to exclusions, severities, thresholds, test discovery, and task
commands appear as explicit policy changes. Its SHA-256 is pinned in
`scripts/check_quality_policy.py`; a config change requires updating both the
readable snapshot and the digest for review.

The small policy check handles relationships native tools do not express:
every Git-tracked handwritten `.py` and `.pyi` file must appear in
[Ruff's own file inventory](https://docs.astral.sh/ruff/configuration/), tool
configuration cannot be nested, and suppressions must match the exact reviewed
record in `quality-exceptions.json`. Generated OpenAPI files are checked by
regeneration in the required `generated` task. Runtime coverage uses
[coverage.py `source_dirs`](https://coverage.readthedocs.io/en/latest/source.html)
so unimported modules count toward the 100% line and branch threshold.

Diagnostic fixtures deliberately call public APIs with invalid types. Their
`type: ignore[code]` comments are limited to named files and must still mask a
real error under [mypy `warn_unused_ignores`](https://mypy.readthedocs.io/en/stable/config_file.html).
Ruff's `RUF100` rejects unused Ruff suppressions. The reviewed `S603` exception
is pinned to one function and must remain used. Basedpyright's
[native configuration](https://docs.basedpyright.com/latest/configuration/config-files/)
remains independently active; this policy lock does not replace type checking.

The lock is a review signal, not a second lint implementation. It must be
updated only for an intentional policy change, with the native tool
configuration and the lock diff reviewed together.
