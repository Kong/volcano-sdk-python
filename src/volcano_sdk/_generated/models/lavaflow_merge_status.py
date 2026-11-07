from typing import Literal

LavaflowMergeStatus = Literal['held', 'merged', 'queued', 'stopped', 'waiting_for_checks']

LAVAFLOW_MERGE_STATUS_VALUES: set[LavaflowMergeStatus] = { 'held', 'merged', 'queued', 'stopped', 'waiting_for_checks',  }

def check_lavaflow_merge_status(value: str) -> LavaflowMergeStatus:
    if value in LAVAFLOW_MERGE_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_MERGE_STATUS_VALUES!r}")
