from typing import Literal

FrontendDeploymentDeploySource = Literal['api', 'cli', 'git', 'system', 'unknown', 'web']

FRONTEND_DEPLOYMENT_DEPLOY_SOURCE_VALUES: set[FrontendDeploymentDeploySource] = { 'api', 'cli', 'git', 'system', 'unknown', 'web',  }

def check_frontend_deployment_deploy_source(value: str) -> FrontendDeploymentDeploySource:
    if value in FRONTEND_DEPLOYMENT_DEPLOY_SOURCE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FRONTEND_DEPLOYMENT_DEPLOY_SOURCE_VALUES!r}")
