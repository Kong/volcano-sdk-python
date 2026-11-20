from typing import Literal

FunctionCandidateDeploymentOperation = Literal['deploy', 'redeploy']

FUNCTION_CANDIDATE_DEPLOYMENT_OPERATION_VALUES: set[FunctionCandidateDeploymentOperation] = { 'deploy', 'redeploy',  }

def check_function_candidate_deployment_operation(value: str) -> FunctionCandidateDeploymentOperation:
    if value in FUNCTION_CANDIDATE_DEPLOYMENT_OPERATION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_CANDIDATE_DEPLOYMENT_OPERATION_VALUES!r}")
