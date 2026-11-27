from typing import Literal

FrontendCustomDomainRedirectStatus = Literal[301, 302, 307, 308]

FRONTEND_CUSTOM_DOMAIN_REDIRECT_STATUS_VALUES: set[FrontendCustomDomainRedirectStatus] = { 301, 302, 307, 308,  }

def check_frontend_custom_domain_redirect_status(value: int) -> FrontendCustomDomainRedirectStatus:
    if value in FRONTEND_CUSTOM_DOMAIN_REDIRECT_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FRONTEND_CUSTOM_DOMAIN_REDIRECT_STATUS_VALUES!r}")
