from typing import Literal

CreateDurableFunctionBodyRuntime = Literal['nodejs22.x', 'nodejs24.x']

CREATE_DURABLE_FUNCTION_BODY_RUNTIME_VALUES: set[CreateDurableFunctionBodyRuntime] = { 'nodejs22.x', 'nodejs24.x',  }

def check_create_durable_function_body_runtime(value: str) -> CreateDurableFunctionBodyRuntime:
    if value in CREATE_DURABLE_FUNCTION_BODY_RUNTIME_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_DURABLE_FUNCTION_BODY_RUNTIME_VALUES!r}")
