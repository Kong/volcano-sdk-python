from typing import Literal

ManagedProjectConfigFrontendCustomDomainTLSConfigMode = Literal['managed']

MANAGED_PROJECT_CONFIG_FRONTEND_CUSTOM_DOMAIN_TLS_CONFIG_MODE_VALUES: set[ManagedProjectConfigFrontendCustomDomainTLSConfigMode] = { 'managed',  }

def check_managed_project_config_frontend_custom_domain_tls_config_mode(value: str) -> ManagedProjectConfigFrontendCustomDomainTLSConfigMode:
    if value in MANAGED_PROJECT_CONFIG_FRONTEND_CUSTOM_DOMAIN_TLS_CONFIG_MODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {MANAGED_PROJECT_CONFIG_FRONTEND_CUSTOM_DOMAIN_TLS_CONFIG_MODE_VALUES!r}")
