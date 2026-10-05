from typing import Literal

DatabaseRestoreKind = Literal['point_in_time', 'snapshot']

DATABASE_RESTORE_KIND_VALUES: set[DatabaseRestoreKind] = { 'point_in_time', 'snapshot',  }

def check_database_restore_kind(value: str) -> DatabaseRestoreKind:
    if value in DATABASE_RESTORE_KIND_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATABASE_RESTORE_KIND_VALUES!r}")
