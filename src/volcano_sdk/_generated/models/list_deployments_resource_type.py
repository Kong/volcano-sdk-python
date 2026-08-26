from typing import Literal

ListDeploymentsResourceType = Literal['frontend', 'function']

LIST_DEPLOYMENTS_RESOURCE_TYPE_VALUES: set[ListDeploymentsResourceType] = { 'frontend', 'function',  }

def check_list_deployments_resource_type(value: str) -> ListDeploymentsResourceType:
    if value in LIST_DEPLOYMENTS_RESOURCE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_DEPLOYMENTS_RESOURCE_TYPE_VALUES!r}")
