# SDK quality

- Research upstream tools before adding enforcement. Keep rules in native tool
  configuration and orchestration in standard tasks. Add custom checks only
  for requirements established tools cannot express; document that gap.
- Fix failures rather than weakening policy. Judge pragmatic exceptions against
  compatibility constraints and verified tool limits; do not use them to postpone
  cleanup. Never impersonate a human reviewer or submit review approval on their
  behalf.
- Keep reviewer and repository-administration credentials outside ordinary
  automation.
- Keep native unit, type, build, and package checks here. Hosting owns behavioral
  acceptance scenarios and bindings; coordinate changes with `Kong/volcano-hosting`.
- Keep maintainer guidance under `maintainers/`; `docs/` is published.
