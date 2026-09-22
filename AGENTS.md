# SDK quality

- Research upstream tools before adding enforcement. Keep rules in native tool
  configuration and orchestration in standard tasks. Add custom checks only
  for requirements established tools cannot express; document that gap.
- Fix failures rather than weakening rules or excluding code. Narrow exceptions
  for verified tool limitations require human approval and an exact record in
  `maintainers/quality-exceptions.json`. Never approve quality-policy changes
  on a human reviewer's behalf.
- Keep reviewer and repository-administration credentials outside ordinary
  automation.
- Preserve shared behavioral scenarios and coordinate contract changes with
  `Kong/volcano-hosting` and the other SDKs.
- Keep maintainer guidance under `maintainers/`; `docs/` is published.
