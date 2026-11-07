from typing import Literal

DatabaseMigrationRunErrorCode = Literal['attempts_exhausted', 'backup_failed', 'branch_limit', 'checksum_mismatch', 'connection_failed', 'database_unavailable', 'history_missing', 'history_too_large', 'internal_error', 'invalid_file', 'invalid_layout', 'locked', 'migration_failed', 'operator_failed', 'owner_not_active', 'plan_changed', 'rehearsal_unavailable', 'restore_in_progress', 'timeout']

DATABASE_MIGRATION_RUN_ERROR_CODE_VALUES: set[DatabaseMigrationRunErrorCode] = { 'attempts_exhausted', 'backup_failed', 'branch_limit', 'checksum_mismatch', 'connection_failed', 'database_unavailable', 'history_missing', 'history_too_large', 'internal_error', 'invalid_file', 'invalid_layout', 'locked', 'migration_failed', 'operator_failed', 'owner_not_active', 'plan_changed', 'rehearsal_unavailable', 'restore_in_progress', 'timeout',  }

def check_database_migration_run_error_code(value: str) -> DatabaseMigrationRunErrorCode:
    if value in DATABASE_MIGRATION_RUN_ERROR_CODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATABASE_MIGRATION_RUN_ERROR_CODE_VALUES!r}")
