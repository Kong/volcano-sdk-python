from typing import Literal

FunctionDeploymentStatus = Literal['active', 'deleted', 'deleting', 'failed', 'provisioning', 'queued', 'superseded']

FUNCTION_DEPLOYMENT_STATUS_VALUES: set[FunctionDeploymentStatus] = { 'active', 'deleted', 'deleting', 'failed', 'provisioning', 'queued', 'superseded',  }

def check_function_deployment_status(value: str) -> FunctionDeploymentStatus:
    if value in FUNCTION_DEPLOYMENT_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_DEPLOYMENT_STATUS_VALUES!r}")
