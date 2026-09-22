# Release evidence and recovery

The checked-in release and publish workflows own versioning and publication.
This checklist does not authorize a release, a registry mutation or an environment approval.

## Before publication

1. Identify the release PR, exact source commit, version, tag and intended registry account. Inspect the generated changelog and package metadata.
2. Require `uv run --locked poe quality`. Verify the OpenAPI snapshot and generated output using the checked-in commands.
3. Obtain clean code and security reviews. Record the approved shared-acceptance run and exact Hosting/SDK revisions for behavior changes; dry runs and synthetic HTTP tests are not live acceptance.
4. Build the wheel and source distribution locally, install it in a clean environment, and run the exact public quickstart. Retain its digest and inventory as candidate package-content evidence; this is not proof of the bytes the release workflow will later build.
5. Confirm explicit release authorization before any publication action. The existing automatic release path may publish after a release PR lands; a successful check or an unprotected environment is not itself release approval. Resolve authorization before merging a release PR rather than assuming the configured PyPI environment has a human gate.

Use the existing workflows and their tag, ancestry, identity and artifact checks.
The release-triggered workflow builds after the GitHub release is published, then passes its preserved artifact to the registry job without rebuilding. A local candidate and the workflow artifact are separate builds. Authorize the source version and this workflow before triggering that path; do not claim exact-byte pre-publication approval from the local check. If approval of specific bytes is required, first add and review a build/test/approval boundary that holds that same artifact before publication. Do not retag a release or overwrite a published version.
After publication, verify the registry's package identity and version, digest/provenance where available, clean installation, and the documented quickstart against the approved platform revision.
Record the workflow URL and registry URL. Source-main tests alone do not prove the published artifact contains that source.

`scripts/check_package.sh` also runs the unchanged public quickstart from each
isolated wheel and sdist install. The test checks sign-in, profile retrieval and
logout against synthetic local HTTP responses, without publisher credentials.
It records each unchanged artifact's SHA256 before the release job uploads it.
This package/example check does not replace registry installation or approved
live platform acceptance.

## Build inputs

`poe build` builds the sdist and then the wheel from that sdist. Quality and
publication use this task. uv verifies isolated build dependencies against the
versions and hashes in `tool.uv.build-constraint-dependencies`. These native
constraints also apply to editable installs during `uv sync` and `uv run`.
The project and CI require uv 0.12.17.

The release job installs locked dependency wheels without building an editable
SDK and disables implicit sync in subsequent commands. To reproduce that setup:

```sh
uv sync --locked --no-install-project --no-build
UV_NO_SYNC=true uv run --no-sync poe build
```

To update Hatchling, change its version in `build-system.requires` and the
`build` dependency group. Resolve and inspect the group's hashes without
executing project or dependency builds:

```sh
uv lock --no-build
uv export --locked --only-group build --no-build
```

Copy the reviewed versions and hashes into `tool.uv.build-constraint-dependencies`,
then run `uv lock --no-build` to record them. Run quality checks on all supported
CI Python versions (3.11 through 3.14). The build group also includes these tools in the audit.
Build constraints do not pin consumers' runtime dependencies.

## Recover from a bad release

For an application regression, first restore its previously tested application revision and dependency lock using [the public guide](../docs/versions.md).
Confirm compatibility with current server configuration and data; an SDK downgrade does not roll either back.

Record the affected versions, symptom, safe previous version, artifact digests and any required data/server remediation in the incident or release issue.
Prepare a reviewed fix as a new version. Do not republish altered bytes under an existing version.
If package deprecation, yanking, an npm tag move or another registry action is needed, preview the exact package/version/action and obtain explicit release-owner authorization first.
Keep already published artifacts and audit evidence available unless the approved response specifically requires otherwise.

Before calling recovery verified, run clean installs and the affected application/quickstart checks for both the safe version and the proposed fix. Record actual results and remaining limits; a written rollback plan is not a performed rollback.
