from typing import Literal

ProjectConfigAuthSignupAllowedEmailDomainsMode = Literal['disabled', 'signup', 'signup_and_signin']

PROJECT_CONFIG_AUTH_SIGNUP_ALLOWED_EMAIL_DOMAINS_MODE_VALUES: set[ProjectConfigAuthSignupAllowedEmailDomainsMode] = { 'disabled', 'signup', 'signup_and_signin',  }

def check_project_config_auth_signup_allowed_email_domains_mode(value: str) -> ProjectConfigAuthSignupAllowedEmailDomainsMode:
    if value in PROJECT_CONFIG_AUTH_SIGNUP_ALLOWED_EMAIL_DOMAINS_MODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_CONFIG_AUTH_SIGNUP_ALLOWED_EMAIL_DOMAINS_MODE_VALUES!r}")
