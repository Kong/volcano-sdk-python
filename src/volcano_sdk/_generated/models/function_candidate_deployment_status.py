from typing import Literal

FunctionCandidateDeploymentStatus = Literal['active', 'failed', 'provisioning']

FUNCTION_CANDIDATE_DEPLOYMENT_STATUS_VALUES: set[FunctionCandidateDeploymentStatus] = { 'active', 'failed', 'provisioning',  }

def check_function_candidate_deployment_status(value: str) -> FunctionCandidateDeploymentStatus:
    if value in FUNCTION_CANDIDATE_DEPLOYMENT_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_CANDIDATE_DEPLOYMENT_STATUS_VALUES!r}")
