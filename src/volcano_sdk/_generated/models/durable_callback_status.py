from typing import Literal

DurableCallbackStatus = Literal['delivering', 'failed', 'succeeded', 'waiting']

DURABLE_CALLBACK_STATUS_VALUES: set[DurableCallbackStatus] = { 'delivering', 'failed', 'succeeded', 'waiting',  }

def check_durable_callback_status(value: str) -> DurableCallbackStatus:
    if value in DURABLE_CALLBACK_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DURABLE_CALLBACK_STATUS_VALUES!r}")
