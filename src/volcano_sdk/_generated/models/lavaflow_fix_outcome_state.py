from typing import Literal

LavaflowFixOutcomeState = Literal['awaiting_deploy', 'effective', 'ineffective', 'regressed', 'reverted', 'watching']

LAVAFLOW_FIX_OUTCOME_STATE_VALUES: set[LavaflowFixOutcomeState] = { 'awaiting_deploy', 'effective', 'ineffective', 'regressed', 'reverted', 'watching',  }

def check_lavaflow_fix_outcome_state(value: str) -> LavaflowFixOutcomeState:
    if value in LAVAFLOW_FIX_OUTCOME_STATE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_FIX_OUTCOME_STATE_VALUES!r}")
