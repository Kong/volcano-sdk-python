from typing import Literal

FrontendDeploymentStatus = Literal['active', 'degraded', 'deleted', 'deleting', 'failed', 'provisioning', 'queued', 'superseded']

FRONTEND_DEPLOYMENT_STATUS_VALUES: set[FrontendDeploymentStatus] = { 'active', 'degraded', 'deleted', 'deleting', 'failed', 'provisioning', 'queued', 'superseded',  }

def check_frontend_deployment_status(value: str) -> FrontendDeploymentStatus:
    if value in FRONTEND_DEPLOYMENT_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FRONTEND_DEPLOYMENT_STATUS_VALUES!r}")
