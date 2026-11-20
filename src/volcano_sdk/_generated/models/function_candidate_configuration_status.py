from typing import Literal

FunctionCandidateConfigurationStatus = Literal['changed', 'current']

FUNCTION_CANDIDATE_CONFIGURATION_STATUS_VALUES: set[FunctionCandidateConfigurationStatus] = { 'changed', 'current',  }

def check_function_candidate_configuration_status(value: str) -> FunctionCandidateConfigurationStatus:
    if value in FUNCTION_CANDIDATE_CONFIGURATION_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_CANDIDATE_CONFIGURATION_STATUS_VALUES!r}")
