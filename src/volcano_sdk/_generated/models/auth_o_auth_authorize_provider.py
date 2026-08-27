from typing import Literal

AuthOAuthAuthorizeProvider = Literal['apple', 'github', 'google', 'microsoft']

AUTH_O_AUTH_AUTHORIZE_PROVIDER_VALUES: set[AuthOAuthAuthorizeProvider] = { 'apple', 'github', 'google', 'microsoft',  }

def check_auth_o_auth_authorize_provider(value: str) -> AuthOAuthAuthorizeProvider:
    if value in AUTH_O_AUTH_AUTHORIZE_PROVIDER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_O_AUTH_AUTHORIZE_PROVIDER_VALUES!r}")
