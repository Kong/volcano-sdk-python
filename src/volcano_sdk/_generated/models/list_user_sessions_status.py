from typing import Literal

ListUserSessionsStatus = Literal['active', 'expired']

LIST_USER_SESSIONS_STATUS_VALUES: set[ListUserSessionsStatus] = { 'active', 'expired',  }

def check_list_user_sessions_status(value: str) -> ListUserSessionsStatus:
    if value in LIST_USER_SESSIONS_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_USER_SESSIONS_STATUS_VALUES!r}")
