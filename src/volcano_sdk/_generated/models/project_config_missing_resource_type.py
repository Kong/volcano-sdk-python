from typing import Literal

ProjectConfigMissingResourceType = Literal['bucket', 'database', 'frontend', 'function']

PROJECT_CONFIG_MISSING_RESOURCE_TYPE_VALUES: set[ProjectConfigMissingResourceType] = { 'bucket', 'database', 'frontend', 'function',  }

def check_project_config_missing_resource_type(value: str) -> ProjectConfigMissingResourceType:
    if value in PROJECT_CONFIG_MISSING_RESOURCE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_CONFIG_MISSING_RESOURCE_TYPE_VALUES!r}")
