from typing import Literal

FrontendDeploymentOperation = Literal['delete', 'deploy', 'redeploy']

FRONTEND_DEPLOYMENT_OPERATION_VALUES: set[FrontendDeploymentOperation] = { 'delete', 'deploy', 'redeploy',  }

def check_frontend_deployment_operation(value: str) -> FrontendDeploymentOperation:
    if value in FRONTEND_DEPLOYMENT_OPERATION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FRONTEND_DEPLOYMENT_OPERATION_VALUES!r}")
