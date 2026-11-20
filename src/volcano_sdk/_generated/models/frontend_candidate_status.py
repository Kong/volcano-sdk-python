from typing import Literal

FrontendCandidateStatus = Literal['creating', 'deleting', 'error', 'ready']

FRONTEND_CANDIDATE_STATUS_VALUES: set[FrontendCandidateStatus] = { 'creating', 'deleting', 'error', 'ready',  }

def check_frontend_candidate_status(value: str) -> FrontendCandidateStatus:
    if value in FRONTEND_CANDIDATE_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FRONTEND_CANDIDATE_STATUS_VALUES!r}")
