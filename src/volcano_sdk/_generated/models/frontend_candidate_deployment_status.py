from typing import Literal

FrontendCandidateDeploymentStatus = Literal['active', 'failed', 'provisioning']

FRONTEND_CANDIDATE_DEPLOYMENT_STATUS_VALUES: set[FrontendCandidateDeploymentStatus] = { 'active', 'failed', 'provisioning',  }

def check_frontend_candidate_deployment_status(value: str) -> FrontendCandidateDeploymentStatus:
    if value in FRONTEND_CANDIDATE_DEPLOYMENT_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FRONTEND_CANDIDATE_DEPLOYMENT_STATUS_VALUES!r}")
