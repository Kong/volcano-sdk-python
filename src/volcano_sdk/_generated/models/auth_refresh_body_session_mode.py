from typing import Literal

AuthRefreshBodySessionMode = Literal['cookie']

AUTH_REFRESH_BODY_SESSION_MODE_VALUES: set[AuthRefreshBodySessionMode] = { 'cookie',  }

def check_auth_refresh_body_session_mode(value: str) -> AuthRefreshBodySessionMode:
    if value in AUTH_REFRESH_BODY_SESSION_MODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_REFRESH_BODY_SESSION_MODE_VALUES!r}")
