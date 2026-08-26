from typing import Literal

ProjectHealthDataStatus = Literal['complete', 'no_data', 'partial', 'stale']

PROJECT_HEALTH_DATA_STATUS_VALUES: set[ProjectHealthDataStatus] = { 'complete', 'no_data', 'partial', 'stale',  }

def check_project_health_data_status(value: str) -> ProjectHealthDataStatus:
    if value in PROJECT_HEALTH_DATA_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_HEALTH_DATA_STATUS_VALUES!r}")
