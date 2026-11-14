from typing import Literal

DatabaseMigrationHistoryEntryStatus = Literal['applied', 'baselined']

DATABASE_MIGRATION_HISTORY_ENTRY_STATUS_VALUES: set[DatabaseMigrationHistoryEntryStatus] = { 'applied', 'baselined',  }

def check_database_migration_history_entry_status(value: str) -> DatabaseMigrationHistoryEntryStatus:
    if value in DATABASE_MIGRATION_HISTORY_ENTRY_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATABASE_MIGRATION_HISTORY_ENTRY_STATUS_VALUES!r}")
