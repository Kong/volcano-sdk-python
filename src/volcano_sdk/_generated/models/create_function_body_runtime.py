from typing import Literal

CreateFunctionBodyRuntime = Literal['nodejs22.x', 'nodejs24.x', 'python3.10', 'python3.11', 'python3.12', 'python3.13', 'python3.14', 'ruby3.3', 'ruby3.4', 'ruby4.0']

CREATE_FUNCTION_BODY_RUNTIME_VALUES: set[CreateFunctionBodyRuntime] = { 'nodejs22.x', 'nodejs24.x', 'python3.10', 'python3.11', 'python3.12', 'python3.13', 'python3.14', 'ruby3.3', 'ruby3.4', 'ruby4.0',  }

def check_create_function_body_runtime(value: str) -> CreateFunctionBodyRuntime:
    if value in CREATE_FUNCTION_BODY_RUNTIME_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_FUNCTION_BODY_RUNTIME_VALUES!r}")
