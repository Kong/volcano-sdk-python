from typing import Literal

LogAppRequestResourceType = Literal['app']

LOG_APP_REQUEST_RESOURCE_TYPE_VALUES: set[LogAppRequestResourceType] = { 'app',  }

def check_log_app_request_resource_type(value: str) -> LogAppRequestResourceType:
    if value in LOG_APP_REQUEST_RESOURCE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LOG_APP_REQUEST_RESOURCE_TYPE_VALUES!r}")
