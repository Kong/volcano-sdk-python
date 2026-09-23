# Quality policy

The quality task delegates diagnostics to native tools: Ruff `ALL` with preview
and unused-directive checks, strict Mypy, Basedpyright, pytest, coverage.py,
and mutmut. Their own configuration cannot establish that another change did
not disable a rule, exclude a new file, or bypass one of the tasks. Ruff's
[configuration](https://docs.astral.sh/ruff/settings/) permits global and
per-file ignores; its [RUF100](https://docs.astral.sh/ruff/linter/#detecting-unused-suppressions)
detects *unused* directives but cannot decide whether a useful directive was
approved. Mypy's [strict and unused-ignore options](https://mypy.readthedocs.io/en/stable/command_line.html)
have the same authorization gap.

`scripts/check_quality_policy.py` fills only those cross-tool gaps. It checks
the Git inventory against configured source roots, pins key thresholds with
readable errors, and fingerprints each complete native-tool table to catch
new override keys. It tokenizes comments in maintained implementation and
stub and test files, then requires every suppression to match one exact rule
and qualified function scope in `quality-exceptions.json`. An unused record
fails too. The listed invalid-type fixtures are the only exemption: their
deliberately wrong calls need Mypy `type: ignore` directives, and Mypy's
unused-ignore check rejects a fixture that stops exercising its diagnostic.
New test files are checked automatically.

Changing a fingerprint is a quality-policy change. Review the native setting,
its effect on actual diagnostics, and any exception evidence before updating
the fingerprint. A green fingerprint is not evidence that an exception is safe.
