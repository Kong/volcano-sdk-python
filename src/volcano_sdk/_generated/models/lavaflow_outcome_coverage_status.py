from typing import Literal

LavaflowOutcomeCoverageStatus = Literal['complete', 'partial', 'unavailable']

LAVAFLOW_OUTCOME_COVERAGE_STATUS_VALUES: set[LavaflowOutcomeCoverageStatus] = { 'complete', 'partial', 'unavailable',  }

def check_lavaflow_outcome_coverage_status(value: str) -> LavaflowOutcomeCoverageStatus:
    if value in LAVAFLOW_OUTCOME_COVERAGE_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_OUTCOME_COVERAGE_STATUS_VALUES!r}")
