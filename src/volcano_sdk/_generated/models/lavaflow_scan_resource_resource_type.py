from typing import Literal

LavaflowScanResourceResourceType = Literal['frontend', 'function']

LAVAFLOW_SCAN_RESOURCE_RESOURCE_TYPE_VALUES: set[LavaflowScanResourceResourceType] = { 'frontend', 'function',  }

def check_lavaflow_scan_resource_resource_type(value: str) -> LavaflowScanResourceResourceType:
    if value in LAVAFLOW_SCAN_RESOURCE_RESOURCE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_SCAN_RESOURCE_RESOURCE_TYPE_VALUES!r}")
