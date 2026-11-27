from typing import Literal

LavaflowDeliveryState = Literal['covered', 'pending', 'pr_created', 'stopped', 'terminal_miss', 'waiting_for_prerequisite']

LAVAFLOW_DELIVERY_STATE_VALUES: set[LavaflowDeliveryState] = { 'covered', 'pending', 'pr_created', 'stopped', 'terminal_miss', 'waiting_for_prerequisite',  }

def check_lavaflow_delivery_state(value: str) -> LavaflowDeliveryState:
    if value in LAVAFLOW_DELIVERY_STATE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_DELIVERY_STATE_VALUES!r}")
