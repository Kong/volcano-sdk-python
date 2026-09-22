# Contract binding types

Mypy and Pyright check `features/` and `typings/` with the same settings as
the SDK. `types-behave` supplies Behave's development-only signatures.

`typings/behave.pyi` describes the three synchronous decorators these bindings
use. It retains typeshed's signature-preserving callable bound and annotates
the otherwise untyped `**kwargs` as `object`. Behave 1.3.3 accepts these
arguments and returns the registered synchronous function unchanged.

Remove this local override when the installed upstream decorators annotate
`**kwargs`. Keep it as a single-module stub: Pyright overlays the installed
partial `behave-stubs` package onto matching package directories, including
a local `typings/behave/` directory.

Sources: [typeshed signatures](https://github.com/python/typeshed/blob/main/stubs/behave/behave/step_registry.pyi),
[Behave registration](https://github.com/behave/behave/blob/v1.3.3/behave/step_registry.py),
[Pyright partial stub resolution](https://github.com/microsoft/pyright/blob/main/packages/pyright-internal/src/partialStubService.ts).

`tests/typing/contract_steps.py` checks retained argument types and deliberately
invalid calls. The shared scenarios still require an executed contract run
against disposable infrastructure; `poe contract-check` only checks discovery.
