from typing import Literal

LavaflowLineageConfidence = Literal['strong', 'weak']

LAVAFLOW_LINEAGE_CONFIDENCE_VALUES: set[LavaflowLineageConfidence] = { 'strong', 'weak',  }

def check_lavaflow_lineage_confidence(value: str) -> LavaflowLineageConfidence:
    if value in LAVAFLOW_LINEAGE_CONFIDENCE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_LINEAGE_CONFIDENCE_VALUES!r}")
