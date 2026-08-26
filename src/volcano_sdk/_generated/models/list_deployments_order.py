from typing import Literal

ListDeploymentsOrder = Literal['completed_at.asc', 'created_at.desc']

LIST_DEPLOYMENTS_ORDER_VALUES: set[ListDeploymentsOrder] = { 'completed_at.asc', 'created_at.desc',  }

def check_list_deployments_order(value: str) -> ListDeploymentsOrder:
    if value in LIST_DEPLOYMENTS_ORDER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_DEPLOYMENTS_ORDER_VALUES!r}")
