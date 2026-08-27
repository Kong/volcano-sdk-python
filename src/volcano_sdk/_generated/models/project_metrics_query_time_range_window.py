from typing import Literal

ProjectMetricsQueryTimeRangeWindow = Literal['1h', '24h', '30m', '7d']

PROJECT_METRICS_QUERY_TIME_RANGE_WINDOW_VALUES: set[ProjectMetricsQueryTimeRangeWindow] = { '1h', '24h', '30m', '7d',  }

def check_project_metrics_query_time_range_window(value: str) -> ProjectMetricsQueryTimeRangeWindow:
    if value in PROJECT_METRICS_QUERY_TIME_RANGE_WINDOW_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_METRICS_QUERY_TIME_RANGE_WINDOW_VALUES!r}")
