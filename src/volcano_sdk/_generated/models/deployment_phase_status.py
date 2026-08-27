from typing import Literal

DeploymentPhaseStatus = Literal['failed', 'in_progress', 'pending', 'skipped', 'succeeded']

DEPLOYMENT_PHASE_STATUS_VALUES: set[DeploymentPhaseStatus] = { 'failed', 'in_progress', 'pending', 'skipped', 'succeeded',  }

def check_deployment_phase_status(value: str) -> DeploymentPhaseStatus:
    if value in DEPLOYMENT_PHASE_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DEPLOYMENT_PHASE_STATUS_VALUES!r}")
