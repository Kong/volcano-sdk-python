from typing import Literal

FunctionCustomDomainResponseDomainStatus = Literal['active', 'detaching', 'failed', 'pending_verification', 'provisioning']

FUNCTION_CUSTOM_DOMAIN_RESPONSE_DOMAIN_STATUS_VALUES: set[FunctionCustomDomainResponseDomainStatus] = { 'active', 'detaching', 'failed', 'pending_verification', 'provisioning',  }

def check_function_custom_domain_response_domain_status(value: str) -> FunctionCustomDomainResponseDomainStatus:
    if value in FUNCTION_CUSTOM_DOMAIN_RESPONSE_DOMAIN_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_CUSTOM_DOMAIN_RESPONSE_DOMAIN_STATUS_VALUES!r}")
