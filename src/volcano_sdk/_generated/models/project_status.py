from typing import Literal

ProjectStatus = Literal['active', 'deleting', 'failed']

PROJECT_STATUS_VALUES: set[ProjectStatus] = { 'active', 'deleting', 'failed',  }

def check_project_status(value: str) -> ProjectStatus:
    if value in PROJECT_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_STATUS_VALUES!r}")
