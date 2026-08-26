from typing import Literal

FrontendCustomDomainResponseTlsMode = Literal['byoc', 'managed']

FRONTEND_CUSTOM_DOMAIN_RESPONSE_TLS_MODE_VALUES: set[FrontendCustomDomainResponseTlsMode] = { 'byoc', 'managed',  }

def check_frontend_custom_domain_response_tls_mode(value: str) -> FrontendCustomDomainResponseTlsMode:
    if value in FRONTEND_CUSTOM_DOMAIN_RESPONSE_TLS_MODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FRONTEND_CUSTOM_DOMAIN_RESPONSE_TLS_MODE_VALUES!r}")
