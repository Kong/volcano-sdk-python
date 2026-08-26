from typing import Literal

FrontendCustomDomainResponseVerificationStatus = Literal['pending', 'verified']

FRONTEND_CUSTOM_DOMAIN_RESPONSE_VERIFICATION_STATUS_VALUES: set[FrontendCustomDomainResponseVerificationStatus] = { 'pending', 'verified',  }

def check_frontend_custom_domain_response_verification_status(value: str) -> FrontendCustomDomainResponseVerificationStatus:
    if value in FRONTEND_CUSTOM_DOMAIN_RESPONSE_VERIFICATION_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FRONTEND_CUSTOM_DOMAIN_RESPONSE_VERIFICATION_STATUS_VALUES!r}")
