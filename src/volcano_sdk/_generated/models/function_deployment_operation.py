from typing import Literal

FunctionDeploymentOperation = Literal['delete', 'deploy', 'update']

FUNCTION_DEPLOYMENT_OPERATION_VALUES: set[FunctionDeploymentOperation] = { 'delete', 'deploy', 'update',  }

def check_function_deployment_operation(value: str) -> FunctionDeploymentOperation:
    if value in FUNCTION_DEPLOYMENT_OPERATION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_DEPLOYMENT_OPERATION_VALUES!r}")
