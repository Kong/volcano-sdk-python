from typing import Literal

LavaflowReviewFindingSeverity = Literal['critical', 'major', 'minor', 'nit']

LAVAFLOW_REVIEW_FINDING_SEVERITY_VALUES: set[LavaflowReviewFindingSeverity] = { 'critical', 'major', 'minor', 'nit',  }

def check_lavaflow_review_finding_severity(value: str) -> LavaflowReviewFindingSeverity:
    if value in LAVAFLOW_REVIEW_FINDING_SEVERITY_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_REVIEW_FINDING_SEVERITY_VALUES!r}")
