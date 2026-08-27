from typing import Literal

FrontendStatus = Literal['active', 'degraded', 'deleting', 'failed', 'provisioning']

FRONTEND_STATUS_VALUES: set[FrontendStatus] = { 'active', 'degraded', 'deleting', 'failed', 'provisioning',  }

def check_frontend_status(value: str) -> FrontendStatus:
    if value in FRONTEND_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FRONTEND_STATUS_VALUES!r}")
