from typing import Literal

ProjectMetricsDataStatus = Literal['complete', 'no_data', 'partial']

PROJECT_METRICS_DATA_STATUS_VALUES: set[ProjectMetricsDataStatus] = { 'complete', 'no_data', 'partial',  }

def check_project_metrics_data_status(value: str) -> ProjectMetricsDataStatus:
    if value in PROJECT_METRICS_DATA_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_METRICS_DATA_STATUS_VALUES!r}")
