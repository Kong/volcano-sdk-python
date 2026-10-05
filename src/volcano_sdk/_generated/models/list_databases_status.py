from typing import Literal

ListDatabasesStatus = Literal['active', 'deleting', 'failed', 'provisioning', 'restoring']

LIST_DATABASES_STATUS_VALUES: set[ListDatabasesStatus] = { 'active', 'deleting', 'failed', 'provisioning', 'restoring',  }

def check_list_databases_status(value: str) -> ListDatabasesStatus:
    if value in LIST_DATABASES_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_DATABASES_STATUS_VALUES!r}")
