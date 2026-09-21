# SDK quality

- Before pushing, run `uv run python scripts/quality.py`. CI runs the same
  command on Python 3.11 and 3.14.
- Keep handwritten runtime functions at cyclomatic complexity five or less;
  the quality command checks the complete runtime source tree.
- Fix failures rather than weakening rules or excluding code. Narrow exceptions
  for verified tool limitations require human approval and an exact record in
  `maintainers/quality-exceptions.json`. Never approve quality-policy changes
  on a human reviewer's behalf.
- Keep generated clients private. Regenerate them from the checked-in OpenAPI
  snapshot; never edit generated output by hand.
- Preserve shared behavioral scenarios and coordinate contract changes with
  `Kong/volcano-hosting` and the other SDKs.
- Keep maintainer guidance under `maintainers/`; `docs/` is published.
