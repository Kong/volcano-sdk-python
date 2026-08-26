from typing import Literal

LogResourceType = Literal['database', 'frontend', 'function']

LOG_RESOURCE_TYPE_VALUES: set[LogResourceType] = { 'database', 'frontend', 'function',  }

def check_log_resource_type(value: str) -> LogResourceType:
    if value in LOG_RESOURCE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LOG_RESOURCE_TYPE_VALUES!r}")
