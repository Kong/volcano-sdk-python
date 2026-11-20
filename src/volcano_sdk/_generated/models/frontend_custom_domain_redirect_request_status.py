from typing import Literal

FrontendCustomDomainRedirectRequestStatus = Literal[301, 302, 307, 308]

FRONTEND_CUSTOM_DOMAIN_REDIRECT_REQUEST_STATUS_VALUES: set[FrontendCustomDomainRedirectRequestStatus] = { 301, 302, 307, 308,  }

def check_frontend_custom_domain_redirect_request_status(value: int) -> FrontendCustomDomainRedirectRequestStatus:
    if value in FRONTEND_CUSTOM_DOMAIN_REDIRECT_REQUEST_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FRONTEND_CUSTOM_DOMAIN_REDIRECT_REQUEST_STATUS_VALUES!r}")
