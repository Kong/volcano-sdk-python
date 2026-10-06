from typing import Literal

BYOCProjectConfigFrontendCustomDomainTLSConfigMode = Literal['byoc']

BYOC_PROJECT_CONFIG_FRONTEND_CUSTOM_DOMAIN_TLS_CONFIG_MODE_VALUES: set[BYOCProjectConfigFrontendCustomDomainTLSConfigMode] = { 'byoc',  }

def check_byoc_project_config_frontend_custom_domain_tls_config_mode(value: str) -> BYOCProjectConfigFrontendCustomDomainTLSConfigMode:
    if value in BYOC_PROJECT_CONFIG_FRONTEND_CUSTOM_DOMAIN_TLS_CONFIG_MODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BYOC_PROJECT_CONFIG_FRONTEND_CUSTOM_DOMAIN_TLS_CONFIG_MODE_VALUES!r}")
