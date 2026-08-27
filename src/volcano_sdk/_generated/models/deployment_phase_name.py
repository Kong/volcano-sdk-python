from typing import Literal

DeploymentPhaseName = Literal['build', 'checkout', 'image', 'provisioning', 'queue', 'rollout', 'verification']

DEPLOYMENT_PHASE_NAME_VALUES: set[DeploymentPhaseName] = { 'build', 'checkout', 'image', 'provisioning', 'queue', 'rollout', 'verification',  }

def check_deployment_phase_name(value: str) -> DeploymentPhaseName:
    if value in DEPLOYMENT_PHASE_NAME_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DEPLOYMENT_PHASE_NAME_VALUES!r}")
