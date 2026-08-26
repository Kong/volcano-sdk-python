from typing import Literal

DeploymentProgressCurrentPhase = Literal['build', 'checkout', 'image', 'provisioning', 'queue', 'rollout', 'verification']

DEPLOYMENT_PROGRESS_CURRENT_PHASE_VALUES: set[DeploymentProgressCurrentPhase] = { 'build', 'checkout', 'image', 'provisioning', 'queue', 'rollout', 'verification',  }

def check_deployment_progress_current_phase(value: str) -> DeploymentProgressCurrentPhase:
    if value in DEPLOYMENT_PROGRESS_CURRENT_PHASE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DEPLOYMENT_PROGRESS_CURRENT_PHASE_VALUES!r}")
