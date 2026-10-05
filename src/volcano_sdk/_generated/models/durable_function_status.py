from typing import Literal

DurableFunctionStatus = Literal['active', 'deleting', 'failed', 'provisioning']

DURABLE_FUNCTION_STATUS_VALUES: set[DurableFunctionStatus] = { 'active', 'deleting', 'failed', 'provisioning',  }

def check_durable_function_status(value: str) -> DurableFunctionStatus:
    if value in DURABLE_FUNCTION_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DURABLE_FUNCTION_STATUS_VALUES!r}")
