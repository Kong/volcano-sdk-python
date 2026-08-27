from typing import Literal

UpdateDatabaseTypeRequestDatabaseType = Literal['volcano-db-2xl', 'volcano-db-l', 'volcano-db-m', 'volcano-db-s', 'volcano-db-xl', 'volcano-db-xs']

UPDATE_DATABASE_TYPE_REQUEST_DATABASE_TYPE_VALUES: set[UpdateDatabaseTypeRequestDatabaseType] = { 'volcano-db-2xl', 'volcano-db-l', 'volcano-db-m', 'volcano-db-s', 'volcano-db-xl', 'volcano-db-xs',  }

def check_update_database_type_request_database_type(value: str) -> UpdateDatabaseTypeRequestDatabaseType:
    if value in UPDATE_DATABASE_TYPE_REQUEST_DATABASE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {UPDATE_DATABASE_TYPE_REQUEST_DATABASE_TYPE_VALUES!r}")
