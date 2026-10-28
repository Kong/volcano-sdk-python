# Runtime dependency ranges

The SDK installs into a consumer's environment beside their own packages, so
`[project] dependencies` and the `durable` extra are specifiers their resolver
must satisfy. `uv.lock` pins what this repository's checks run against;
consumers never see it.

## Ranges and pins

- Use bounded ranges for widely shared packages such as `httpx` and the durable
  runtime. An exact pin on a package the application also uses makes its
  resolution fail.
- Leave `attrs` and `typing-extensions` uncapped. Both keep backward
  compatibility across releases, so a cap would cause consumer conflicts
  without preventing breaks.
- Pin exactly only a package whose internals the SDK depends on and that few
  consumers share. `centrifuge-python` is the one case; see
  [realtime-compatibility.md](realtime-compatibility.md).

A range lets a consumer resolve a release this repository has never tested.
The fresh-install check covers that.

## Fresh-install check

`uv run --locked poe fresh-install` builds the wheel and installs it with the
`durable` extra into a new environment, resolving from PyPI without `uv.lock`
the way `pip install` does. It then:

- installs the `dev` group's tools at their `uv.lock` versions, constraining
  every runtime package to its fresh version;
- copies `src/volcano_sdk/_tests`, which the wheel excludes, beside the
  installed package and runs the full pytest suite. The
  `tests/package/installed_sdk.py` plugin fails the run if any SDK module was
  imported from outside the install;
- prints each runtime package's `uv.lock` and fresh versions with
  `scripts/dependency_drift.py`, to the log and the job summary, and warns for
  each drifted package.

It fails on a test failure, on an exact pin that resolves to another version,
or when test tooling changes a runtime package. Drift alone only warns. The
resolver and constraints already prevent the last two failures; the checks stop
a later edit to the script from silently testing a resolution consumers do not
get.
`uv tree --outdated` reports newest releases rather than this resolution, and
pytest does not report where a package was imported from; the two helpers
cover those gaps.

CI runs it as `fresh-install (3.11)` and `fresh-install (3.14)`, required by
Quality Gate, on every `ci.yml` trigger: pull requests including Dependabot's,
merge groups, `main`, the release build, and a daily schedule that catches
upstream releases between changes.

## When it fails

If the locked `test` jobs pass and fresh-install fails, a release inside a
published range breaks the SDK. Fix the SDK, or cap the range below that
release with a comment linking the upstream issue. Either change is
`fix(deps)`, so Release Please publishes it. Changing `uv.lock` does not fix
consumers.
