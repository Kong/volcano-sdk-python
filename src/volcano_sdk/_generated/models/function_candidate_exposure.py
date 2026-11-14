from typing import Literal

FunctionCandidateExposure = Literal['private']

FUNCTION_CANDIDATE_EXPOSURE_VALUES: set[FunctionCandidateExposure] = { 'private',  }

def check_function_candidate_exposure(value: str) -> FunctionCandidateExposure:
    if value in FUNCTION_CANDIDATE_EXPOSURE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_CANDIDATE_EXPOSURE_VALUES!r}")
