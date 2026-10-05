from typing import Literal

FunctionHTTPAuthMode = Literal['none', 'volcano']

FUNCTION_HTTP_AUTH_MODE_VALUES: set[FunctionHTTPAuthMode] = { 'none', 'volcano',  }

def check_function_http_auth_mode(value: str) -> FunctionHTTPAuthMode:
    if value in FUNCTION_HTTP_AUTH_MODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_HTTP_AUTH_MODE_VALUES!r}")
