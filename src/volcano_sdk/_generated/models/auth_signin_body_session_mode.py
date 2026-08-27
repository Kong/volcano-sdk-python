from typing import Literal

AuthSigninBodySessionMode = Literal['cookie']

AUTH_SIGNIN_BODY_SESSION_MODE_VALUES: set[AuthSigninBodySessionMode] = { 'cookie',  }

def check_auth_signin_body_session_mode(value: str) -> AuthSigninBodySessionMode:
    if value in AUTH_SIGNIN_BODY_SESSION_MODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_SIGNIN_BODY_SESSION_MODE_VALUES!r}")
