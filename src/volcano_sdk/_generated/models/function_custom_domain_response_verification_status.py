from typing import Literal

FunctionCustomDomainResponseVerificationStatus = Literal['failed', 'pending', 'verified']

FUNCTION_CUSTOM_DOMAIN_RESPONSE_VERIFICATION_STATUS_VALUES: set[FunctionCustomDomainResponseVerificationStatus] = { 'failed', 'pending', 'verified',  }

def check_function_custom_domain_response_verification_status(value: str) -> FunctionCustomDomainResponseVerificationStatus:
    if value in FUNCTION_CUSTOM_DOMAIN_RESPONSE_VERIFICATION_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_CUSTOM_DOMAIN_RESPONSE_VERIFICATION_STATUS_VALUES!r}")
