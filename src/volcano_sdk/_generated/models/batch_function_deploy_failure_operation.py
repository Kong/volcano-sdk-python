from typing import Literal

BatchFunctionDeployFailureOperation = Literal['deploy', 'update']

BATCH_FUNCTION_DEPLOY_FAILURE_OPERATION_VALUES: set[BatchFunctionDeployFailureOperation] = { 'deploy', 'update',  }

def check_batch_function_deploy_failure_operation(value: str) -> BatchFunctionDeployFailureOperation:
    if value in BATCH_FUNCTION_DEPLOY_FAILURE_OPERATION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BATCH_FUNCTION_DEPLOY_FAILURE_OPERATION_VALUES!r}")
