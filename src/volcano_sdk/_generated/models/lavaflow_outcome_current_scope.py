from typing import Literal

LavaflowOutcomeCurrentScope = Literal['confirmed_code_quality']

LAVAFLOW_OUTCOME_CURRENT_SCOPE_VALUES: set[LavaflowOutcomeCurrentScope] = { 'confirmed_code_quality',  }

def check_lavaflow_outcome_current_scope(value: str) -> LavaflowOutcomeCurrentScope:
    if value in LAVAFLOW_OUTCOME_CURRENT_SCOPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_OUTCOME_CURRENT_SCOPE_VALUES!r}")
