from typing import Literal

FunctionKindFilter = Literal['durable', 'standard']

FUNCTION_KIND_FILTER_VALUES: set[FunctionKindFilter] = { 'durable', 'standard',  }

def check_function_kind_filter(value: str) -> FunctionKindFilter:
    if value in FUNCTION_KIND_FILTER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_KIND_FILTER_VALUES!r}")
