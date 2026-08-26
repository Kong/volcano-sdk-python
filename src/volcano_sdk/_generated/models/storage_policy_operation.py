from typing import Literal

StoragePolicyOperation = Literal['DELETE', 'INSERT', 'SELECT', 'UPDATE']

STORAGE_POLICY_OPERATION_VALUES: set[StoragePolicyOperation] = { 'DELETE', 'INSERT', 'SELECT', 'UPDATE',  }

def check_storage_policy_operation(value: str) -> StoragePolicyOperation:
    if value in STORAGE_POLICY_OPERATION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {STORAGE_POLICY_OPERATION_VALUES!r}")
