from typing import Literal

LogDeploymentStage = Literal['compile', 'publish']

LOG_DEPLOYMENT_STAGE_VALUES: set[LogDeploymentStage] = { 'compile', 'publish',  }

def check_log_deployment_stage(value: str) -> LogDeploymentStage:
    if value in LOG_DEPLOYMENT_STAGE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LOG_DEPLOYMENT_STAGE_VALUES!r}")
