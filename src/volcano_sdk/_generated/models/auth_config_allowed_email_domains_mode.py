from typing import Literal

AuthConfigAllowedEmailDomainsMode = Literal['disabled', 'signup', 'signup_and_signin']

AUTH_CONFIG_ALLOWED_EMAIL_DOMAINS_MODE_VALUES: set[AuthConfigAllowedEmailDomainsMode] = { 'disabled', 'signup', 'signup_and_signin',  }

def check_auth_config_allowed_email_domains_mode(value: str) -> AuthConfigAllowedEmailDomainsMode:
    if value in AUTH_CONFIG_ALLOWED_EMAIL_DOMAINS_MODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_CONFIG_ALLOWED_EMAIL_DOMAINS_MODE_VALUES!r}")
