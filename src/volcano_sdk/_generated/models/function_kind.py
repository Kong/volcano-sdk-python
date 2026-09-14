from typing import Literal

FunctionKind = Literal['durable', 'standard']

FUNCTION_KIND_VALUES: set[FunctionKind] = { 'durable', 'standard',  }

def check_function_kind(value: str) -> FunctionKind:
    if value in FUNCTION_KIND_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_KIND_VALUES!r}")
