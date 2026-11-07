from typing import Literal

LavaflowLineageRelation = Literal['recurrence', 'regression']

LAVAFLOW_LINEAGE_RELATION_VALUES: set[LavaflowLineageRelation] = { 'recurrence', 'regression',  }

def check_lavaflow_lineage_relation(value: str) -> LavaflowLineageRelation:
    if value in LAVAFLOW_LINEAGE_RELATION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_LINEAGE_RELATION_VALUES!r}")
