from typing import Literal

ProjectMetricsGroupBy = Literal['region', 'resource_type']

PROJECT_METRICS_GROUP_BY_VALUES: set[ProjectMetricsGroupBy] = { 'region', 'resource_type',  }

def check_project_metrics_group_by(value: str) -> ProjectMetricsGroupBy:
    if value in PROJECT_METRICS_GROUP_BY_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_METRICS_GROUP_BY_VALUES!r}")
