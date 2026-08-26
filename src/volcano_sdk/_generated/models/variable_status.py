from typing import Literal

VariableStatus = Literal['active', 'failed', 'provisioning']

VARIABLE_STATUS_VALUES: set[VariableStatus] = { 'active', 'failed', 'provisioning',  }

def check_variable_status(value: str) -> VariableStatus:
    if value in VARIABLE_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {VARIABLE_STATUS_VALUES!r}")
