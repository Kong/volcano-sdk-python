from typing import Literal

DurableMessageWaitStatus = Literal['cancelled', 'delivered', 'expired', 'matched', 'waiting']

DURABLE_MESSAGE_WAIT_STATUS_VALUES: set[DurableMessageWaitStatus] = { 'cancelled', 'delivered', 'expired', 'matched', 'waiting',  }

def check_durable_message_wait_status(value: str) -> DurableMessageWaitStatus:
    if value in DURABLE_MESSAGE_WAIT_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DURABLE_MESSAGE_WAIT_STATUS_VALUES!r}")
