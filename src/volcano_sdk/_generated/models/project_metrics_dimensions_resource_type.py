from typing import Literal

ProjectMetricsDimensionsResourceType = Literal['frontend', 'function']

PROJECT_METRICS_DIMENSIONS_RESOURCE_TYPE_VALUES: set[ProjectMetricsDimensionsResourceType] = { 'frontend', 'function',  }

def check_project_metrics_dimensions_resource_type(value: str) -> ProjectMetricsDimensionsResourceType:
    if value in PROJECT_METRICS_DIMENSIONS_RESOURCE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_METRICS_DIMENSIONS_RESOURCE_TYPE_VALUES!r}")
