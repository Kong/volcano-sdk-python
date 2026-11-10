from typing import Literal

LavaflowAutonomy = Literal['diagnose_only', 'merge', 'open_pr']

LAVAFLOW_AUTONOMY_VALUES: set[LavaflowAutonomy] = { 'diagnose_only', 'merge', 'open_pr',  }

def check_lavaflow_autonomy(value: str) -> LavaflowAutonomy:
    if value in LAVAFLOW_AUTONOMY_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_AUTONOMY_VALUES!r}")
