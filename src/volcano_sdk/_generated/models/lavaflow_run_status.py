from typing import Literal

LavaflowRunStatus = Literal['cancelled', 'completed', 'diagnosing', 'failed', 'fixing', 'pr_open', 'queued', 'reviewing']

LAVAFLOW_RUN_STATUS_VALUES: set[LavaflowRunStatus] = { 'cancelled', 'completed', 'diagnosing', 'failed', 'fixing', 'pr_open', 'queued', 'reviewing',  }

def check_lavaflow_run_status(value: str) -> LavaflowRunStatus:
    if value in LAVAFLOW_RUN_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_RUN_STATUS_VALUES!r}")
