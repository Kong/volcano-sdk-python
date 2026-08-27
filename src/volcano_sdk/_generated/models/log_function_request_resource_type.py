from typing import Literal

LogFunctionRequestResourceType = Literal['function']

LOG_FUNCTION_REQUEST_RESOURCE_TYPE_VALUES: set[LogFunctionRequestResourceType] = { 'function',  }

def check_log_function_request_resource_type(value: str) -> LogFunctionRequestResourceType:
    if value in LOG_FUNCTION_REQUEST_RESOURCE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LOG_FUNCTION_REQUEST_RESOURCE_TYPE_VALUES!r}")
