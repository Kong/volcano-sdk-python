# Native Python boundaries

Ruff uses its pinned `ALL` preview rules. Mypy rejects explicit, unimported, and
decorator-introduced `Any`; basedpyright uses `all` without a baseline. The same
configuration checks runtime code, tests, contract bindings, scripts, and local
third-party stubs. Invalid-type examples carry exact expected diagnostics in
the dedicated fixture inventory; unused expectations fail both checkers.

Runtime tests and typed support live in `src/volcano_sdk/_tests`, following
[pytest’s in-package test layout](https://docs.pytest.org/en/stable/explanation/goodpractices.html).
Pytest uses importlib mode and discovers this package together with `tests/unit`
for enforcement-tool tests. Relative imports identify sibling fixtures without
adding their directory to import search paths. Both roots remain linted and typed.

The wheel excludes the private test package through
[Hatch target configuration](https://hatch.pypa.io/latest/config/build/#excluding-files).
The sdist retains source tests, following the [PyPA distribution model](https://packaging.python.org/en/latest/flow/).
Package smoke checks install both archives and verify that the resulting wheel
omits tests. Coverage and Mutmut exclude that test subtree while retaining every
handwritten runtime module, including newly extracted internal implementations.

Internal modules retain underscore names so they remain outside the public
library interface. Their collaborating functions use normal names; facades
receive typed capabilities, and test probes access protected state through
subclasses. No runtime API exists solely for test inspection.

The pinned OpenAPI generator uses checked-in
[custom templates](https://github.com/openapi-generators/openapi-python-client#using-custom-templates)
for normal-named internal request adapters and `UUID | str` wire identifiers.
UUID headers are serialized explicitly; existing string identifiers retain their
spelling. `poe generated` regenerates into a temporary directory and compares
every generated file. Generated output is never edited directly.

CI retains the Python 3.11–3.14 check names and selects exact patch versions
listed by the native [setup-python manifest](https://github.com/actions/python-versions/blob/main/versions-manifest.json).
`UV_PYTHON` selects each matrix interpreter; `.python-version` pins the local
3.12 environment. The isolated coverage command pins the same 3.12 patch.
