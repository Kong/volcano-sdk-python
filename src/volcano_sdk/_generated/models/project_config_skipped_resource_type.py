from typing import Literal

ProjectConfigSkippedResourceType = Literal['bucket', 'database', 'frontend', 'function']

PROJECT_CONFIG_SKIPPED_RESOURCE_TYPE_VALUES: set[ProjectConfigSkippedResourceType] = { 'bucket', 'database', 'frontend', 'function',  }

def check_project_config_skipped_resource_type(value: str) -> ProjectConfigSkippedResourceType:
    if value in PROJECT_CONFIG_SKIPPED_RESOURCE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_CONFIG_SKIPPED_RESOURCE_TYPE_VALUES!r}")
