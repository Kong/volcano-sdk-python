from typing import Literal

FrontendCustomDomainTLSConfigMode = Literal['byoc', 'managed']

FRONTEND_CUSTOM_DOMAIN_TLS_CONFIG_MODE_VALUES: set[FrontendCustomDomainTLSConfigMode] = { 'byoc', 'managed',  }

def check_frontend_custom_domain_tls_config_mode(value: str) -> FrontendCustomDomainTLSConfigMode:
    if value in FRONTEND_CUSTOM_DOMAIN_TLS_CONFIG_MODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FRONTEND_CUSTOM_DOMAIN_TLS_CONFIG_MODE_VALUES!r}")
