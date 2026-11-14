from typing import Literal

DatabaseMigrationRunFileOutcome = Literal['already_applied', 'applied', 'failed', 'not_run', 'pending', 'unknown']

DATABASE_MIGRATION_RUN_FILE_OUTCOME_VALUES: set[DatabaseMigrationRunFileOutcome] = { 'already_applied', 'applied', 'failed', 'not_run', 'pending', 'unknown',  }

def check_database_migration_run_file_outcome(value: str) -> DatabaseMigrationRunFileOutcome:
    if value in DATABASE_MIGRATION_RUN_FILE_OUTCOME_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATABASE_MIGRATION_RUN_FILE_OUTCOME_VALUES!r}")
