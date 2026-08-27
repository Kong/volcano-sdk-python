from typing import Literal

FunctionStatus = Literal['active', 'deleting', 'failed', 'provisioning']

FUNCTION_STATUS_VALUES: set[FunctionStatus] = { 'active', 'deleting', 'failed', 'provisioning',  }

def check_function_status(value: str) -> FunctionStatus:
    if value in FUNCTION_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_STATUS_VALUES!r}")
