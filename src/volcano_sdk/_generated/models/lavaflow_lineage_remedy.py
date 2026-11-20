from typing import Literal

LavaflowLineageRemedy = Literal['fix', 'none', 'revert']

LAVAFLOW_LINEAGE_REMEDY_VALUES: set[LavaflowLineageRemedy] = { 'fix', 'none', 'revert',  }

def check_lavaflow_lineage_remedy(value: str) -> LavaflowLineageRemedy:
    if value in LAVAFLOW_LINEAGE_REMEDY_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_LINEAGE_REMEDY_VALUES!r}")
