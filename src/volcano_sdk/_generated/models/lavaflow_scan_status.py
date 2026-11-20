from typing import Literal

LavaflowScanStatus = Literal['cancelled', 'completed', 'failed', 'running', 'waiting']

LAVAFLOW_SCAN_STATUS_VALUES: set[LavaflowScanStatus] = { 'cancelled', 'completed', 'failed', 'running', 'waiting',  }

def check_lavaflow_scan_status(value: str) -> LavaflowScanStatus:
    if value in LAVAFLOW_SCAN_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_SCAN_STATUS_VALUES!r}")
