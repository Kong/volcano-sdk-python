from typing import Literal

DatabaseMigrationRunStatus = Literal['failed', 'queued', 'running', 'succeeded']

DATABASE_MIGRATION_RUN_STATUS_VALUES: set[DatabaseMigrationRunStatus] = { 'failed', 'queued', 'running', 'succeeded',  }

def check_database_migration_run_status(value: str) -> DatabaseMigrationRunStatus:
    if value in DATABASE_MIGRATION_RUN_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATABASE_MIGRATION_RUN_STATUS_VALUES!r}")
