from typing import Literal

LavaflowScanSource = Literal['deployment']

LAVAFLOW_SCAN_SOURCE_VALUES: set[LavaflowScanSource] = { 'deployment',  }

def check_lavaflow_scan_source(value: str) -> LavaflowScanSource:
    if value in LAVAFLOW_SCAN_SOURCE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_SCAN_SOURCE_VALUES!r}")
