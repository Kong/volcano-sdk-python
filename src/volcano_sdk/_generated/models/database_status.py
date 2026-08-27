from typing import Literal

DatabaseStatus = Literal['active', 'deleting', 'failed', 'provisioning']

DATABASE_STATUS_VALUES: set[DatabaseStatus] = { 'active', 'deleting', 'failed', 'provisioning',  }

def check_database_status(value: str) -> DatabaseStatus:
    if value in DATABASE_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATABASE_STATUS_VALUES!r}")
