from typing import Literal

AuthLogoutBodySessionMode = Literal['cookie']

AUTH_LOGOUT_BODY_SESSION_MODE_VALUES: set[AuthLogoutBodySessionMode] = { 'cookie',  }

def check_auth_logout_body_session_mode(value: str) -> AuthLogoutBodySessionMode:
    if value in AUTH_LOGOUT_BODY_SESSION_MODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_LOGOUT_BODY_SESSION_MODE_VALUES!r}")
