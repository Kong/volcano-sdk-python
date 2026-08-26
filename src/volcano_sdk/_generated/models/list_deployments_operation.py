from typing import Literal

ListDeploymentsOperation = Literal['delete', 'deploy', 'redeploy', 'update']

LIST_DEPLOYMENTS_OPERATION_VALUES: set[ListDeploymentsOperation] = { 'delete', 'deploy', 'redeploy', 'update',  }

def check_list_deployments_operation(value: str) -> ListDeploymentsOperation:
    if value in LIST_DEPLOYMENTS_OPERATION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_DEPLOYMENTS_OPERATION_VALUES!r}")
