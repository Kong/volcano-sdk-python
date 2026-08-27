from typing import Literal

BanUserResponseStatus = Literal['banned']

BAN_USER_RESPONSE_STATUS_VALUES: set[BanUserResponseStatus] = { 'banned',  }

def check_ban_user_response_status(value: str) -> BanUserResponseStatus:
    if value in BAN_USER_RESPONSE_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BAN_USER_RESPONSE_STATUS_VALUES!r}")
