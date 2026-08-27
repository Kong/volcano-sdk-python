from typing import Literal

DatabaseBranchStatus = Literal['active', 'deleting', 'failed', 'provisioning']

DATABASE_BRANCH_STATUS_VALUES: set[DatabaseBranchStatus] = { 'active', 'deleting', 'failed', 'provisioning',  }

def check_database_branch_status(value: str) -> DatabaseBranchStatus:
    if value in DATABASE_BRANCH_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATABASE_BRANCH_STATUS_VALUES!r}")
