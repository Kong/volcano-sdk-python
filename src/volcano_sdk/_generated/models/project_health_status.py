from typing import Literal

ProjectHealthStatus = Literal['critical', 'degraded', 'empty', 'healthy', 'needs_attention', 'unknown']

PROJECT_HEALTH_STATUS_VALUES: set[ProjectHealthStatus] = { 'critical', 'degraded', 'empty', 'healthy', 'needs_attention', 'unknown',  }

def check_project_health_status(value: str) -> ProjectHealthStatus:
    if value in PROJECT_HEALTH_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_HEALTH_STATUS_VALUES!r}")
