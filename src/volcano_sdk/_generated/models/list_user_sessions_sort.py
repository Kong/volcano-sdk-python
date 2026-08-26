from typing import Literal

ListUserSessionsSort = Literal['created_at', 'last_activity']

LIST_USER_SESSIONS_SORT_VALUES: set[ListUserSessionsSort] = { 'created_at', 'last_activity',  }

def check_list_user_sessions_sort(value: str) -> ListUserSessionsSort:
    if value in LIST_USER_SESSIONS_SORT_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_USER_SESSIONS_SORT_VALUES!r}")
