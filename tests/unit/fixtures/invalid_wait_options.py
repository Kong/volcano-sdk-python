from volcano_sdk.durable_authoring import WaitUntilOptions


def non_callable_predicate() -> WaitUntilOptions:
    # This invalid consumer example must fail mypy's arg-type check; the
    # unused-ignore check fails if the constructor stops enforcing its type.
    return WaitUntilOptions(until=None, initial_state=False)  # type: ignore[arg-type]
