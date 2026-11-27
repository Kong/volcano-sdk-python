from typing import Literal

DatabaseMigrationRunSource = Literal['api', 'git_deploy']

DATABASE_MIGRATION_RUN_SOURCE_VALUES: set[DatabaseMigrationRunSource] = { 'api', 'git_deploy',  }

def check_database_migration_run_source(value: str) -> DatabaseMigrationRunSource:
    if value in DATABASE_MIGRATION_RUN_SOURCE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATABASE_MIGRATION_RUN_SOURCE_VALUES!r}")
