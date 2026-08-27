from typing import Literal

AuthUserStatus = Literal['active', 'banned', 'deleted']

AUTH_USER_STATUS_VALUES: set[AuthUserStatus] = { 'active', 'banned', 'deleted',  }

def check_auth_user_status(value: str) -> AuthUserStatus:
    if value in AUTH_USER_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_USER_STATUS_VALUES!r}")
