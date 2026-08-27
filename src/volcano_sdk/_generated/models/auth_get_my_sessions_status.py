from typing import Literal

AuthGetMySessionsStatus = Literal['active', 'expired']

AUTH_GET_MY_SESSIONS_STATUS_VALUES: set[AuthGetMySessionsStatus] = { 'active', 'expired',  }

def check_auth_get_my_sessions_status(value: str) -> AuthGetMySessionsStatus:
    if value in AUTH_GET_MY_SESSIONS_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_GET_MY_SESSIONS_STATUS_VALUES!r}")
