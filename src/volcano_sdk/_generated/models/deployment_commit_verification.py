from typing import Literal

DeploymentCommitVerification = Literal['files', 'none', 'repository']

DEPLOYMENT_COMMIT_VERIFICATION_VALUES: set[DeploymentCommitVerification] = { 'files', 'none', 'repository',  }

def check_deployment_commit_verification(value: str) -> DeploymentCommitVerification:
    if value in DEPLOYMENT_COMMIT_VERIFICATION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DEPLOYMENT_COMMIT_VERIFICATION_VALUES!r}")
