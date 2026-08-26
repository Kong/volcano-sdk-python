from typing import Literal

FunctionDeploymentDeploySource = Literal['api', 'cli', 'git', 'system', 'unknown', 'web']

FUNCTION_DEPLOYMENT_DEPLOY_SOURCE_VALUES: set[FunctionDeploymentDeploySource] = { 'api', 'cli', 'git', 'system', 'unknown', 'web',  }

def check_function_deployment_deploy_source(value: str) -> FunctionDeploymentDeploySource:
    if value in FUNCTION_DEPLOYMENT_DEPLOY_SOURCE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_DEPLOYMENT_DEPLOY_SOURCE_VALUES!r}")
