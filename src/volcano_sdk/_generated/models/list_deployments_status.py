from typing import Literal

ListDeploymentsStatus = Literal['active', 'degraded', 'deleted', 'deleting', 'failed', 'provisioning', 'queued', 'superseded']

LIST_DEPLOYMENTS_STATUS_VALUES: set[ListDeploymentsStatus] = { 'active', 'degraded', 'deleted', 'deleting', 'failed', 'provisioning', 'queued', 'superseded',  }

def check_list_deployments_status(value: str) -> ListDeploymentsStatus:
    if value in LIST_DEPLOYMENTS_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_DEPLOYMENTS_STATUS_VALUES!r}")
