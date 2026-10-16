from typing import Literal

DurableMessageSenderType = Literal['anon', 'execution', 'project', 'service_key', 'user']

DURABLE_MESSAGE_SENDER_TYPE_VALUES: set[DurableMessageSenderType] = { 'anon', 'execution', 'project', 'service_key', 'user',  }

def check_durable_message_sender_type(value: str) -> DurableMessageSenderType:
    if value in DURABLE_MESSAGE_SENDER_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DURABLE_MESSAGE_SENDER_TYPE_VALUES!r}")
