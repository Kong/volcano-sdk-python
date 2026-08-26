from typing import Literal

ProjectDeploymentResourceType = Literal['frontend', 'function']

PROJECT_DEPLOYMENT_RESOURCE_TYPE_VALUES: set[ProjectDeploymentResourceType] = { 'frontend', 'function',  }

def check_project_deployment_resource_type(value: str) -> ProjectDeploymentResourceType:
    if value in PROJECT_DEPLOYMENT_RESOURCE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_DEPLOYMENT_RESOURCE_TYPE_VALUES!r}")
