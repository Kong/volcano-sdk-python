from typing import Literal

ShareStatus = Literal['active', 'disabled']

SHARE_STATUS_VALUES: set[ShareStatus] = { 'active', 'disabled',  }

def check_share_status(value: str) -> ShareStatus:
    if value in SHARE_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SHARE_STATUS_VALUES!r}")
