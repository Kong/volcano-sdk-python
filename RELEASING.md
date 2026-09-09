# Releasing

**PyPI publishing is disabled.** GitHub releases produce checked package artifacts,
not packages customers can install from PyPI.

## Release flow

[Release Please](https://github.com/googleapis/release-please-action) runs on
`main`. Releasable Conventional Commits update a version/changelog PR; docs-,
chore-, and CI-only changes normally wait for a feature or fix.

The App's release PR auto-merges after required GitHub checks pass. Release Please
then creates the tag and GitHub release. [Check release package](.github/workflows/publish.yml)
validates the release, runs CI, builds and smoke-tests the package, and uploads
the `release-package` Actions artifact.

## Repository setup

- Install `kong-volcano-app` with Contents, Pull requests, and Issues write access.
- Set Actions variable `VOLCANO_APP_ID=4307518` and secret `VOLCANO_APP_KEY`.
  Use the App token so release PRs and releases trigger downstream workflows.
- Enable auto-merge and require `test (3.11)` and `test (3.14)` on `main`.

## Recovery

Re-run the failed **Release Please** job or the original **Check release package**
run. For source fixes, release a new version; never move an existing release tag.

## Enable PyPI later

Confirm package-name availability, ownership, and release approval, then add
[trusted publishing](https://docs.pypi.org/trusted-publishers/) in a separate PR.
Publish a new release containing that workflow; older releases remain unpublished.
