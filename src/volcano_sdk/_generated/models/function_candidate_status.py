from typing import Literal

FunctionCandidateStatus = Literal['creating', 'deleting', 'error', 'ready']

FUNCTION_CANDIDATE_STATUS_VALUES: set[FunctionCandidateStatus] = { 'creating', 'deleting', 'error', 'ready',  }

def check_function_candidate_status(value: str) -> FunctionCandidateStatus:
    if value in FUNCTION_CANDIDATE_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_CANDIDATE_STATUS_VALUES!r}")
