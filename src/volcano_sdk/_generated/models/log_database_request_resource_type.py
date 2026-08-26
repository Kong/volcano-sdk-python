from typing import Literal

LogDatabaseRequestResourceType = Literal['database']

LOG_DATABASE_REQUEST_RESOURCE_TYPE_VALUES: set[LogDatabaseRequestResourceType] = { 'database',  }

def check_log_database_request_resource_type(value: str) -> LogDatabaseRequestResourceType:
    if value in LOG_DATABASE_REQUEST_RESOURCE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LOG_DATABASE_REQUEST_RESOURCE_TYPE_VALUES!r}")
