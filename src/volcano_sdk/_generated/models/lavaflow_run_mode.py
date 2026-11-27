from typing import Literal

LavaflowRunMode = Literal['code_quality', 'live']

LAVAFLOW_RUN_MODE_VALUES: set[LavaflowRunMode] = { 'code_quality', 'live',  }

def check_lavaflow_run_mode(value: str) -> LavaflowRunMode:
    if value in LAVAFLOW_RUN_MODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_RUN_MODE_VALUES!r}")
