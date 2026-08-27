from typing import Literal

CreateDatabaseRequestPgVersion = Literal['15', '16']

CREATE_DATABASE_REQUEST_PG_VERSION_VALUES: set[CreateDatabaseRequestPgVersion] = { '15', '16',  }

def check_create_database_request_pg_version(value: str) -> CreateDatabaseRequestPgVersion:
    if value in CREATE_DATABASE_REQUEST_PG_VERSION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_DATABASE_REQUEST_PG_VERSION_VALUES!r}")
