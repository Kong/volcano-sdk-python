from typing import Literal

ProjectMetricsMetric = Literal['availability', 'p95_latency', 'request_count', 'server_error_count']

PROJECT_METRICS_METRIC_VALUES: set[ProjectMetricsMetric] = { 'availability', 'p95_latency', 'request_count', 'server_error_count',  }

def check_project_metrics_metric(value: str) -> ProjectMetricsMetric:
    if value in PROJECT_METRICS_METRIC_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_METRICS_METRIC_VALUES!r}")
