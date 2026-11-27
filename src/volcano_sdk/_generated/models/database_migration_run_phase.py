from typing import Literal

DatabaseMigrationRunPhase = Literal['apply', 'backup', 'plan', 'rehearse']

DATABASE_MIGRATION_RUN_PHASE_VALUES: set[DatabaseMigrationRunPhase] = { 'apply', 'backup', 'plan', 'rehearse',  }

def check_database_migration_run_phase(value: str) -> DatabaseMigrationRunPhase:
    if value in DATABASE_MIGRATION_RUN_PHASE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATABASE_MIGRATION_RUN_PHASE_VALUES!r}")
