from typing import Literal

ListAccountSessionsSort = Literal['created_at', 'last_activity']

LIST_ACCOUNT_SESSIONS_SORT_VALUES: set[ListAccountSessionsSort] = { 'created_at', 'last_activity',  }

def check_list_account_sessions_sort(value: str) -> ListAccountSessionsSort:
    if value in LIST_ACCOUNT_SESSIONS_SORT_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_ACCOUNT_SESSIONS_SORT_VALUES!r}")
