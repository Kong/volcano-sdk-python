from typing import Literal

ListAuthUsersStatus = Literal['active', 'banned']

LIST_AUTH_USERS_STATUS_VALUES: set[ListAuthUsersStatus] = { 'active', 'banned',  }

def check_list_auth_users_status(value: str) -> ListAuthUsersStatus:
    if value in LIST_AUTH_USERS_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_AUTH_USERS_STATUS_VALUES!r}")
