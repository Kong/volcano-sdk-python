from typing import Literal

FrontendCustomDomainResponseDomainStatus = Literal['active', 'deleted', 'detaching', 'failed', 'pending_verification', 'provisioning']

FRONTEND_CUSTOM_DOMAIN_RESPONSE_DOMAIN_STATUS_VALUES: set[FrontendCustomDomainResponseDomainStatus] = { 'active', 'deleted', 'detaching', 'failed', 'pending_verification', 'provisioning',  }

def check_frontend_custom_domain_response_domain_status(value: str) -> FrontendCustomDomainResponseDomainStatus:
    if value in FRONTEND_CUSTOM_DOMAIN_RESPONSE_DOMAIN_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FRONTEND_CUSTOM_DOMAIN_RESPONSE_DOMAIN_STATUS_VALUES!r}")
