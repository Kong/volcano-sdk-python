# Mutation testing

`uv run --locked poe mutation` runs mutmut against the handwritten lock runtime
with the full unit-test suite. The native `[tool.mutmut]` configuration selects
`locks.py` and its three renewal/guard modules; it does not mutate the generated
OpenAPI client. This is the first subsystem in a staged rollout, not a passing
repository-wide mutation gate.

`poe mutation` exports and checks mutmut's native CI stats. Mutmut itself exits
successfully when mutants survive, so the Poe result check requires a nonempty
run with every mutant killed. Inspect `mutants/mutmut-cicd-stats.json` to keep
`survived`, `no_tests`, `timeout`,
`suspicious`, `segfault`, and interrupted counts separate. A timeout or crash
does not prove that a test detected a defect. Mutmut caches results in the
ignored `mutants/` directory; use a fresh directory when certifying a full run.

Mutmut 3.8.0's stats collection currently fails an unrelated storage read-size
assertion when it instruments the entire SDK at once. The copied, unmutated
source passes the full unit suite. The lock selection keeps this first
mutation pass reproducible while the broader instrumentation issue is resolved.
The selected source paths must expand to every handwritten runtime module
before mutation becomes a required quality task.

Reference: [mutmut configuration and workflow](https://mutmut.readthedocs.io/en/latest/).
