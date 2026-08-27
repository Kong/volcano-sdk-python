from typing import Literal

UnbanUserResponseStatus = Literal['active']

UNBAN_USER_RESPONSE_STATUS_VALUES: set[UnbanUserResponseStatus] = { 'active',  }

def check_unban_user_response_status(value: str) -> UnbanUserResponseStatus:
    if value in UNBAN_USER_RESPONSE_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {UNBAN_USER_RESPONSE_STATUS_VALUES!r}")
