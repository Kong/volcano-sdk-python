from typing import Literal

ProjectImportRunStatus = Literal['failed', 'pending', 'running', 'succeeded', 'superseded']

PROJECT_IMPORT_RUN_STATUS_VALUES: set[ProjectImportRunStatus] = { 'failed', 'pending', 'running', 'succeeded', 'superseded',  }

def check_project_import_run_status(value: str) -> ProjectImportRunStatus:
    if value in PROJECT_IMPORT_RUN_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_IMPORT_RUN_STATUS_VALUES!r}")
