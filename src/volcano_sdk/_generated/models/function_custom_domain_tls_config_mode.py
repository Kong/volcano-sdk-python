from typing import Literal

FunctionCustomDomainTLSConfigMode = Literal['byoc']

FUNCTION_CUSTOM_DOMAIN_TLS_CONFIG_MODE_VALUES: set[FunctionCustomDomainTLSConfigMode] = { 'byoc',  }

def check_function_custom_domain_tls_config_mode(value: str) -> FunctionCustomDomainTLSConfigMode:
    if value in FUNCTION_CUSTOM_DOMAIN_TLS_CONFIG_MODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_CUSTOM_DOMAIN_TLS_CONFIG_MODE_VALUES!r}")
