from typing import Literal

CreateStoragePolicyRequestOperation = Literal['DELETE', 'INSERT', 'SELECT', 'UPDATE']

CREATE_STORAGE_POLICY_REQUEST_OPERATION_VALUES: set[CreateStoragePolicyRequestOperation] = { 'DELETE', 'INSERT', 'SELECT', 'UPDATE',  }

def check_create_storage_policy_request_operation(value: str) -> CreateStoragePolicyRequestOperation:
    if value in CREATE_STORAGE_POLICY_REQUEST_OPERATION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_STORAGE_POLICY_REQUEST_OPERATION_VALUES!r}")
