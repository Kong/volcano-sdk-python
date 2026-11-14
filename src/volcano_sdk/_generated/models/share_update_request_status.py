from typing import Literal

ShareUpdateRequestStatus = Literal['active', 'disabled']

SHARE_UPDATE_REQUEST_STATUS_VALUES: set[ShareUpdateRequestStatus] = { 'active', 'disabled',  }

def check_share_update_request_status(value: str) -> ShareUpdateRequestStatus:
    if value in SHARE_UPDATE_REQUEST_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SHARE_UPDATE_REQUEST_STATUS_VALUES!r}")
