from typing import Literal

ProjectDeploymentDeploySource = Literal['api', 'cli', 'git', 'system', 'unknown', 'web']

PROJECT_DEPLOYMENT_DEPLOY_SOURCE_VALUES: set[ProjectDeploymentDeploySource] = { 'api', 'cli', 'git', 'system', 'unknown', 'web',  }

def check_project_deployment_deploy_source(value: str) -> ProjectDeploymentDeploySource:
    if value in PROJECT_DEPLOYMENT_DEPLOY_SOURCE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_DEPLOYMENT_DEPLOY_SOURCE_VALUES!r}")
