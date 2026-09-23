# Public type completeness

`uv run --locked poe verifytypes` uses basedpyright's native `--verifytypes`
check on the `py.typed` package. The command fails unless every exported SDK
symbol has a known type. `--ignoreexternal` leaves type incompleteness in the
optional durable runtime to its publisher; the SDK's own adapter remains in
scope. The base and durable wheel environments in `poe package-extras` check
the adapter against installed packages at runtime.

The `_Engine` annotations describe the members used by `DurableContext`.
Keep them aligned with the pinned durable runtime when that dependency changes.

Source: [Pyright's typed-library guidance](https://github.com/microsoft/pyright/blob/main/docs/typed-libraries.md#verifying-type-completeness).
