from typing import Literal

LogFrontendRequestResourceType = Literal['frontend']

LOG_FRONTEND_REQUEST_RESOURCE_TYPE_VALUES: set[LogFrontendRequestResourceType] = { 'frontend',  }

def check_log_frontend_request_resource_type(value: str) -> LogFrontendRequestResourceType:
    if value in LOG_FRONTEND_REQUEST_RESOURCE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LOG_FRONTEND_REQUEST_RESOURCE_TYPE_VALUES!r}")
