from typing import Literal

CreateDatabaseRequestDatabaseType = Literal['volcano-db-2xl', 'volcano-db-l', 'volcano-db-m', 'volcano-db-s', 'volcano-db-xl', 'volcano-db-xs']

CREATE_DATABASE_REQUEST_DATABASE_TYPE_VALUES: set[CreateDatabaseRequestDatabaseType] = { 'volcano-db-2xl', 'volcano-db-l', 'volcano-db-m', 'volcano-db-s', 'volcano-db-xl', 'volcano-db-xs',  }

def check_create_database_request_database_type(value: str) -> CreateDatabaseRequestDatabaseType:
    if value in CREATE_DATABASE_REQUEST_DATABASE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_DATABASE_REQUEST_DATABASE_TYPE_VALUES!r}")
