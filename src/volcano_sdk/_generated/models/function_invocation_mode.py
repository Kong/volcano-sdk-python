from typing import Literal

FunctionInvocationMode = Literal['http', 'rpc']

FUNCTION_INVOCATION_MODE_VALUES: set[FunctionInvocationMode] = { 'http', 'rpc',  }

def check_function_invocation_mode(value: str) -> FunctionInvocationMode:
    if value in FUNCTION_INVOCATION_MODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_INVOCATION_MODE_VALUES!r}")
