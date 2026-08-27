from typing import Literal

ProjectDeploymentOperation = Literal['delete', 'deploy', 'redeploy', 'update']

PROJECT_DEPLOYMENT_OPERATION_VALUES: set[ProjectDeploymentOperation] = { 'delete', 'deploy', 'redeploy', 'update',  }

def check_project_deployment_operation(value: str) -> ProjectDeploymentOperation:
    if value in PROJECT_DEPLOYMENT_OPERATION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_DEPLOYMENT_OPERATION_VALUES!r}")
