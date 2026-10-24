from typing import Literal

ProjectHealthResourceType = Literal['database', 'database_branch', 'frontend', 'function', 'project']

PROJECT_HEALTH_RESOURCE_TYPE_VALUES: set[ProjectHealthResourceType] = { 'database', 'database_branch', 'frontend', 'function', 'project',  }

def check_project_health_resource_type(value: str) -> ProjectHealthResourceType:
    if value in PROJECT_HEALTH_RESOURCE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_HEALTH_RESOURCE_TYPE_VALUES!r}")
