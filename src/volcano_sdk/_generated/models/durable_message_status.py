from typing import Literal

DurableMessageStatus = Literal['delivered', 'delivering', 'dropped', 'published', 'queued']

DURABLE_MESSAGE_STATUS_VALUES: set[DurableMessageStatus] = { 'delivered', 'delivering', 'dropped', 'published', 'queued',  }

def check_durable_message_status(value: str) -> DurableMessageStatus:
    if value in DURABLE_MESSAGE_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DURABLE_MESSAGE_STATUS_VALUES!r}")
