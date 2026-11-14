from typing import Literal

LavaflowLineageEvidenceConfidence = Literal['display', 'strong', 'weak']

LAVAFLOW_LINEAGE_EVIDENCE_CONFIDENCE_VALUES: set[LavaflowLineageEvidenceConfidence] = { 'display', 'strong', 'weak',  }

def check_lavaflow_lineage_evidence_confidence(value: str) -> LavaflowLineageEvidenceConfidence:
    if value in LAVAFLOW_LINEAGE_EVIDENCE_CONFIDENCE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_LINEAGE_EVIDENCE_CONFIDENCE_VALUES!r}")
