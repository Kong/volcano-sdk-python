from typing import Literal

DatabaseRestoreStatus = Literal['completed', 'exhausted', 'failed', 'pending', 'running']

DATABASE_RESTORE_STATUS_VALUES: set[DatabaseRestoreStatus] = { 'completed', 'exhausted', 'failed', 'pending', 'running',  }

def check_database_restore_status(value: str) -> DatabaseRestoreStatus:
    if value in DATABASE_RESTORE_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATABASE_RESTORE_STATUS_VALUES!r}")
