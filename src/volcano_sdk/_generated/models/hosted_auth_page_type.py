from typing import Literal

HostedAuthPageType = Literal['login', 'reset-password']

HOSTED_AUTH_PAGE_TYPE_VALUES: set[HostedAuthPageType] = { 'login', 'reset-password',  }

def check_hosted_auth_page_type(value: str) -> HostedAuthPageType:
    if value in HOSTED_AUTH_PAGE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {HOSTED_AUTH_PAGE_TYPE_VALUES!r}")
