from typing import Literal

FrontendCandidateConfigurationStatus = Literal['changed', 'current']

FRONTEND_CANDIDATE_CONFIGURATION_STATUS_VALUES: set[FrontendCandidateConfigurationStatus] = { 'changed', 'current',  }

def check_frontend_candidate_configuration_status(value: str) -> FrontendCandidateConfigurationStatus:
    if value in FRONTEND_CANDIDATE_CONFIGURATION_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FRONTEND_CANDIDATE_CONFIGURATION_STATUS_VALUES!r}")
