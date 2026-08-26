from typing import Literal

AuthMethodSummaryType = Literal['anonymous', 'oauth', 'password']

AUTH_METHOD_SUMMARY_TYPE_VALUES: set[AuthMethodSummaryType] = { 'anonymous', 'oauth', 'password',  }

def check_auth_method_summary_type(value: str) -> AuthMethodSummaryType:
    if value in AUTH_METHOD_SUMMARY_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_METHOD_SUMMARY_TYPE_VALUES!r}")
