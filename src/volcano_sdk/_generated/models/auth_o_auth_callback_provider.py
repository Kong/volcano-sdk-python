from typing import Literal

AuthOAuthCallbackProvider = Literal['apple', 'github', 'google', 'microsoft']

AUTH_O_AUTH_CALLBACK_PROVIDER_VALUES: set[AuthOAuthCallbackProvider] = { 'apple', 'github', 'google', 'microsoft',  }

def check_auth_o_auth_callback_provider(value: str) -> AuthOAuthCallbackProvider:
    if value in AUTH_O_AUTH_CALLBACK_PROVIDER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_O_AUTH_CALLBACK_PROVIDER_VALUES!r}")
