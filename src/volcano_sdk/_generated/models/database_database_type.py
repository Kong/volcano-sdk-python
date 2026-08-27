from typing import Literal

DatabaseDatabaseType = Literal['volcano-db-2xl', 'volcano-db-l', 'volcano-db-m', 'volcano-db-s', 'volcano-db-xl', 'volcano-db-xs']

DATABASE_DATABASE_TYPE_VALUES: set[DatabaseDatabaseType] = { 'volcano-db-2xl', 'volcano-db-l', 'volcano-db-m', 'volcano-db-s', 'volcano-db-xl', 'volcano-db-xs',  }

def check_database_database_type(value: str) -> DatabaseDatabaseType:
    if value in DATABASE_DATABASE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATABASE_DATABASE_TYPE_VALUES!r}")
