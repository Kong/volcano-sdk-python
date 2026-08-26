from typing import Literal

AuthGetMySessionsSort = Literal['created_at', 'last_activity']

AUTH_GET_MY_SESSIONS_SORT_VALUES: set[AuthGetMySessionsSort] = { 'created_at', 'last_activity',  }

def check_auth_get_my_sessions_sort(value: str) -> AuthGetMySessionsSort:
    if value in AUTH_GET_MY_SESSIONS_SORT_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_GET_MY_SESSIONS_SORT_VALUES!r}")
