# Public type completeness

`uv run --locked poe verifytypes` uses basedpyright's native `--verifytypes`
check on the `py.typed` package. The command fails unless every exported SDK
symbol has a known type, including types reachable through the public API.
The pinned optional durable runtime has incomplete annotations for several
configuration types reachable through `DurableContext`. Narrow development
stubs in `typings/aws_durable_execution_sdk_python/` model the members the
SDK uses, while the built package retains its declared optional dependency.
The `package-types` Tox environment checks the built wheel in a clean
environment with the pinned stub package. The base and durable wheel
environments check optional imports and the adapter at runtime.

The `_Engine` annotations describe the members used by `DurableContext`.
Keep them aligned with the pinned durable runtime when that dependency changes.
The partial stub package follows [PEP 561's stub-package convention](https://typing.python.org/en/latest/spec/distributing.html#partial-stub-packages);
it is a development dependency and is not included in the SDK wheel.

Source: [Pyright's typed-library guidance](https://github.com/microsoft/pyright/blob/main/docs/typed-libraries.md#verifying-type-completeness).
