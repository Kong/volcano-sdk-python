# Mutation testing

`uv run --locked poe quality` includes the mutation gate. CI runs its other
native checks in the Python matrix and runs `poe mutation` once on Python 3.12;
the required `Quality Gate` needs both jobs. Mutmut 3.8.0 instruments every
handwritten SDK module while excluding the generated OpenAPI client. The PR
gate runs every mutant in whole changed modules and the four critical lock
modules. It compares PRs against their actual base, pushes against the prior
commit, and merge groups against their base commit. Local uncommitted and
untracked runtime modules are included too.

The small shell adapter selects native mutmut dotted-name patterns. The result
checker reads mutmut's pinned JSON metadata because mutmut exits successfully
when mutants survive and labels pytest internal-error exit code 3 as a kill.
`reports/mutation.json` keeps survivors, uncovered mutants, crashes, timeouts,
and incomplete results separate. Any outcome other than a test kill fails.
Modules with no mutatable functions are listed explicitly; the selected lock
modules ensure the gate never passes an empty mutation run. Mutmut caches work
under ignored `mutants/`; dependency changes force a rerun.

The weekly `Full Mutation Audit` runs all handwritten modules and uploads the
same report. It is separate from the PR gate because full-repository mutation
is too expensive on every change. It reports unresolved mutants as failures,
without a grandfathered baseline.

Reference: [mutmut configuration and workflow](https://mutmut.readthedocs.io/en/latest/).
