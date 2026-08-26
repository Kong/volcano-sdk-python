from typing import Literal

AuthSessionProvider = Literal['anonymous', 'apple', 'email', 'github', 'google', 'microsoft']

AUTH_SESSION_PROVIDER_VALUES: set[AuthSessionProvider] = { 'anonymous', 'apple', 'email', 'github', 'google', 'microsoft',  }

def check_auth_session_provider(value: str) -> AuthSessionProvider:
    if value in AUTH_SESSION_PROVIDER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_SESSION_PROVIDER_VALUES!r}")
