from typing import Literal

HostedAuthPageType = Literal['device', 'forgot-password', 'login', 'reset-password', 'signup', 'verify-email']

HOSTED_AUTH_PAGE_TYPE_VALUES: set[HostedAuthPageType] = { 'device', 'forgot-password', 'login', 'reset-password', 'signup', 'verify-email',  }

def check_hosted_auth_page_type(value: str) -> HostedAuthPageType:
    if value in HOSTED_AUTH_PAGE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {HOSTED_AUTH_PAGE_TYPE_VALUES!r}")
