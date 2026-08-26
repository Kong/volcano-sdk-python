from typing import Literal

ProjectMetricsUnit = Literal['count', 'ratio', 'seconds']

PROJECT_METRICS_UNIT_VALUES: set[ProjectMetricsUnit] = { 'count', 'ratio', 'seconds',  }

def check_project_metrics_unit(value: str) -> ProjectMetricsUnit:
    if value in PROJECT_METRICS_UNIT_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_METRICS_UNIT_VALUES!r}")
