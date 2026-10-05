from typing import Literal

DatabaseBackupScheduleEntryFrequency = Literal['daily', 'monthly', 'weekly']

DATABASE_BACKUP_SCHEDULE_ENTRY_FREQUENCY_VALUES: set[DatabaseBackupScheduleEntryFrequency] = { 'daily', 'monthly', 'weekly',  }

def check_database_backup_schedule_entry_frequency(value: str) -> DatabaseBackupScheduleEntryFrequency:
    if value in DATABASE_BACKUP_SCHEDULE_ENTRY_FREQUENCY_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATABASE_BACKUP_SCHEDULE_ENTRY_FREQUENCY_VALUES!r}")
