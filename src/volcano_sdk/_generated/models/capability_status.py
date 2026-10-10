from typing import Literal

CapabilityStatus = Literal['available', 'unavailable']

CAPABILITY_STATUS_VALUES: set[CapabilityStatus] = { 'available', 'unavailable',  }

def check_capability_status(value: str) -> CapabilityStatus:
    if value in CAPABILITY_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CAPABILITY_STATUS_VALUES!r}")
