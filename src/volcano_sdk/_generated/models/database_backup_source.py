from typing import Literal

DatabaseBackupSource = Literal['manual', 'scheduled']

DATABASE_BACKUP_SOURCE_VALUES: set[DatabaseBackupSource] = { 'manual', 'scheduled',  }

def check_database_backup_source(value: str) -> DatabaseBackupSource:
    if value in DATABASE_BACKUP_SOURCE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATABASE_BACKUP_SOURCE_VALUES!r}")
