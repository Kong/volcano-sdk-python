# SDK quality

- Before pushing, run `uv run --locked poe quality`. CI runs the same
  command on Python 3.11 and 3.14.
- Research upstream tools before adding enforcement. Keep rules in native tool
  configuration and orchestration in declarative tasks. Add custom checks only
  for requirements established tools cannot express; document that gap.
- Keep every handwritten Python function at cyclomatic complexity five or less,
  including tests and contract support. Ruff enforces this in `pyproject.toml`.
- Fix failures rather than weakening rules or excluding code. Narrow exceptions
  for verified tool limitations require human approval and an exact record in
  `maintainers/quality-exceptions.json`. Never approve quality-policy changes
  on a human reviewer's behalf.
- Keep reviewer and repository-administration credentials outside ordinary
  automation. Quality policy and enforcement are owned by `@Kong/team-volcano`
  through `.github/CODEOWNERS`.
- Keep generated clients private. Regenerate them from the checked-in OpenAPI
  snapshot; never edit generated output by hand.
- Preserve shared behavioral scenarios and coordinate contract changes with
  `Kong/volcano-hosting` and the other SDKs.
- Keep maintainer guidance under `maintainers/`; `docs/` is published.
