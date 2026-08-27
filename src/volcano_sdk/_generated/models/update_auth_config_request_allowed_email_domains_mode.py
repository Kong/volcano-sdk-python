from typing import Literal

UpdateAuthConfigRequestAllowedEmailDomainsMode = Literal['disabled', 'signup', 'signup_and_signin']

UPDATE_AUTH_CONFIG_REQUEST_ALLOWED_EMAIL_DOMAINS_MODE_VALUES: set[UpdateAuthConfigRequestAllowedEmailDomainsMode] = { 'disabled', 'signup', 'signup_and_signin',  }

def check_update_auth_config_request_allowed_email_domains_mode(value: str) -> UpdateAuthConfigRequestAllowedEmailDomainsMode:
    if value in UPDATE_AUTH_CONFIG_REQUEST_ALLOWED_EMAIL_DOMAINS_MODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {UPDATE_AUTH_CONFIG_REQUEST_ALLOWED_EMAIL_DOMAINS_MODE_VALUES!r}")
