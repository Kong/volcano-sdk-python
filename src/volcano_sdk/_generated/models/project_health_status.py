from typing import Literal

ProjectHealthStatus = Literal['critical', 'degraded', 'healthy', 'unknown']

PROJECT_HEALTH_STATUS_VALUES: set[ProjectHealthStatus] = { 'critical', 'degraded', 'healthy', 'unknown',  }

def check_project_health_status(value: str) -> ProjectHealthStatus:
    if value in PROJECT_HEALTH_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_HEALTH_STATUS_VALUES!r}")
