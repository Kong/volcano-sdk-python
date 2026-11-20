from typing import Literal

ListAccountSessionsStatus = Literal['active', 'expired']

LIST_ACCOUNT_SESSIONS_STATUS_VALUES: set[ListAccountSessionsStatus] = { 'active', 'expired',  }

def check_list_account_sessions_status(value: str) -> ListAccountSessionsStatus:
    if value in LIST_ACCOUNT_SESSIONS_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_ACCOUNT_SESSIONS_STATUS_VALUES!r}")
