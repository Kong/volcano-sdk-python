from typing import Literal

FunctionVisibility = Literal['authenticated', 'private', 'public']

FUNCTION_VISIBILITY_VALUES: set[FunctionVisibility] = { 'authenticated', 'private', 'public',  }

def check_function_visibility(value: str) -> FunctionVisibility:
    if value in FUNCTION_VISIBILITY_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_VISIBILITY_VALUES!r}")
