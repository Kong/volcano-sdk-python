from typing import Literal

ProjectConfigDatabaseDatabaseType = Literal['volcano-db-2xl', 'volcano-db-l', 'volcano-db-m', 'volcano-db-s', 'volcano-db-xl', 'volcano-db-xs']

PROJECT_CONFIG_DATABASE_DATABASE_TYPE_VALUES: set[ProjectConfigDatabaseDatabaseType] = { 'volcano-db-2xl', 'volcano-db-l', 'volcano-db-m', 'volcano-db-s', 'volcano-db-xl', 'volcano-db-xs',  }

def check_project_config_database_database_type(value: str) -> ProjectConfigDatabaseDatabaseType:
    if value in PROJECT_CONFIG_DATABASE_DATABASE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_CONFIG_DATABASE_DATABASE_TYPE_VALUES!r}")
