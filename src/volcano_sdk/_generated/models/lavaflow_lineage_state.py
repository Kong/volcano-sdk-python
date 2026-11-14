from typing import Literal

LavaflowLineageState = Literal['active', 'held', 'settled']

LAVAFLOW_LINEAGE_STATE_VALUES: set[LavaflowLineageState] = { 'active', 'held', 'settled',  }

def check_lavaflow_lineage_state(value: str) -> LavaflowLineageState:
    if value in LAVAFLOW_LINEAGE_STATE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_LINEAGE_STATE_VALUES!r}")
