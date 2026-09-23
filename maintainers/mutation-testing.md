# Mutation testing

`uv run --locked poe quality` runs native mutmut against every changed handwritten
SDK function and the lock subsystem on each PR. The lock modules always run
because credential scope, ownership, and lease renewal are critical. The Git
diff is measured from the merge base with `origin/main`, including local
working-tree edits. CI fetches that base before running the same quality task.

Mutmut has native mutant-name patterns and cached incremental results, but no
Git-diff selector or failing exit status for survivors. The narrow
`scripts/mutation_targets.py` adapter maps changed function lines to mutmut
patterns and checks native `mutmut results --all true` output. It does not
select tests or implement a mutation engine. Native `[tool.mutmut]` configuration
instruments all handwritten runtime modules, excludes generated code, runs the
full unit suite for test relevance, and reruns cached mutants after dependency
changes. The `mutants/` directory is ignored; use a fresh checkout to certify
a complete run.

`reports/mutation-summary.json` classifies selected killed, surviving,
uncovered, crashing, timed-out, and incomplete mutants separately. Equivalent
mutants are never inferred from a crash or timeout; the equivalent count stays
zero until a specific human-reviewed exception exists. Any selected outcome
other than killed fails the PR gate, including an empty result. CI preserves
the summary, target list, native stats, and detailed results.

The weekly [Full Mutation Audit](../.github/workflows/mutation-audit.yml) runs
mutmut without a selector against every handwritten runtime module and uploads
native stats plus all outcomes. It reports debt outside the changed functions
without silently treating survivors or harness failures as kills. Mutmut's
protocol instrumentation previously changed a runtime `isinstance` check in
storage; that check now tests the required stream methods directly, so the
full-source clean baseline completes.

Reference: [mutmut configuration and workflow](https://mutmut.readthedocs.io/en/latest/).
