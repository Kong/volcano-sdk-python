from typing import Literal

DatabaseMigrationWarningCode = Literal['backup_prune_failed', 'backup_skipped', 'missing_file', 'out_of_order', 'rehearsal_skipped', 'warnings_truncated']

DATABASE_MIGRATION_WARNING_CODE_VALUES: set[DatabaseMigrationWarningCode] = { 'backup_prune_failed', 'backup_skipped', 'missing_file', 'out_of_order', 'rehearsal_skipped', 'warnings_truncated',  }

def check_database_migration_warning_code(value: str) -> DatabaseMigrationWarningCode:
    if value in DATABASE_MIGRATION_WARNING_CODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATABASE_MIGRATION_WARNING_CODE_VALUES!r}")
