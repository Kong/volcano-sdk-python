from typing import Literal

GitDeploymentRunStatus = Literal['failed', 'pending', 'running', 'skipped', 'succeeded', 'superseded']

GIT_DEPLOYMENT_RUN_STATUS_VALUES: set[GitDeploymentRunStatus] = { 'failed', 'pending', 'running', 'skipped', 'succeeded', 'superseded',  }

def check_git_deployment_run_status(value: str) -> GitDeploymentRunStatus:
    if value in GIT_DEPLOYMENT_RUN_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GIT_DEPLOYMENT_RUN_STATUS_VALUES!r}")
