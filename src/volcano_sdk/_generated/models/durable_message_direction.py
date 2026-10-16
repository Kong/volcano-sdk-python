from typing import Literal

DurableMessageDirection = Literal['in', 'out']

DURABLE_MESSAGE_DIRECTION_VALUES: set[DurableMessageDirection] = { 'in', 'out',  }

def check_durable_message_direction(value: str) -> DurableMessageDirection:
    if value in DURABLE_MESSAGE_DIRECTION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DURABLE_MESSAGE_DIRECTION_VALUES!r}")
