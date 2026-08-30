from typing import Literal

FunctionCustomDomainResponseTlsMode = Literal['byoc']

FUNCTION_CUSTOM_DOMAIN_RESPONSE_TLS_MODE_VALUES: set[FunctionCustomDomainResponseTlsMode] = { 'byoc',  }

def check_function_custom_domain_response_tls_mode(value: str) -> FunctionCustomDomainResponseTlsMode:
    if value in FUNCTION_CUSTOM_DOMAIN_RESPONSE_TLS_MODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_CUSTOM_DOMAIN_RESPONSE_TLS_MODE_VALUES!r}")
