from typing import Literal

BYOCFrontendCustomDomainTLSConfigMode = Literal['byoc']

BYOC_FRONTEND_CUSTOM_DOMAIN_TLS_CONFIG_MODE_VALUES: set[BYOCFrontendCustomDomainTLSConfigMode] = { 'byoc',  }

def check_byoc_frontend_custom_domain_tls_config_mode(value: str) -> BYOCFrontendCustomDomainTLSConfigMode:
    if value in BYOC_FRONTEND_CUSTOM_DOMAIN_TLS_CONFIG_MODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BYOC_FRONTEND_CUSTOM_DOMAIN_TLS_CONFIG_MODE_VALUES!r}")
