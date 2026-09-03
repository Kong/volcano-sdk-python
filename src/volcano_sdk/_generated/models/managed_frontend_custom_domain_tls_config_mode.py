from typing import Literal

ManagedFrontendCustomDomainTLSConfigMode = Literal['managed']

MANAGED_FRONTEND_CUSTOM_DOMAIN_TLS_CONFIG_MODE_VALUES: set[ManagedFrontendCustomDomainTLSConfigMode] = { 'managed',  }

def check_managed_frontend_custom_domain_tls_config_mode(value: str) -> ManagedFrontendCustomDomainTLSConfigMode:
    if value in MANAGED_FRONTEND_CUSTOM_DOMAIN_TLS_CONFIG_MODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {MANAGED_FRONTEND_CUSTOM_DOMAIN_TLS_CONFIG_MODE_VALUES!r}")
