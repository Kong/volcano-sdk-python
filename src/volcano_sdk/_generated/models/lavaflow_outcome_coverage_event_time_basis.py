from typing import Literal

LavaflowOutcomeCoverageEventTimeBasis = Literal['confirmed_merge_time', 'first_recorded_live_confirmation', 'recorded_automatic_resolution']

LAVAFLOW_OUTCOME_COVERAGE_EVENT_TIME_BASIS_VALUES: set[LavaflowOutcomeCoverageEventTimeBasis] = { 'confirmed_merge_time', 'first_recorded_live_confirmation', 'recorded_automatic_resolution',  }

def check_lavaflow_outcome_coverage_event_time_basis(value: str) -> LavaflowOutcomeCoverageEventTimeBasis:
    if value in LAVAFLOW_OUTCOME_COVERAGE_EVENT_TIME_BASIS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_OUTCOME_COVERAGE_EVENT_TIME_BASIS_VALUES!r}")
