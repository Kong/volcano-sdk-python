from typing import Literal

ProjectDeploymentStatus = Literal['active', 'degraded', 'deleted', 'deleting', 'failed', 'provisioning', 'queued', 'superseded']

PROJECT_DEPLOYMENT_STATUS_VALUES: set[ProjectDeploymentStatus] = { 'active', 'degraded', 'deleted', 'deleting', 'failed', 'provisioning', 'queued', 'superseded',  }

def check_project_deployment_status(value: str) -> ProjectDeploymentStatus:
    if value in PROJECT_DEPLOYMENT_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_DEPLOYMENT_STATUS_VALUES!r}")
