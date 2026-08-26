from typing import Literal

ListProjectDeploymentsResourceType = Literal['frontend', 'function']

LIST_PROJECT_DEPLOYMENTS_RESOURCE_TYPE_VALUES: set[ListProjectDeploymentsResourceType] = { 'frontend', 'function',  }

def check_list_project_deployments_resource_type(value: str) -> ListProjectDeploymentsResourceType:
    if value in LIST_PROJECT_DEPLOYMENTS_RESOURCE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_PROJECT_DEPLOYMENTS_RESOURCE_TYPE_VALUES!r}")
