from typing import Literal

ProjectImportTarget = Literal['production']

PROJECT_IMPORT_TARGET_VALUES: set[ProjectImportTarget] = { 'production',  }

def check_project_import_target(value: str) -> ProjectImportTarget:
    if value in PROJECT_IMPORT_TARGET_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_IMPORT_TARGET_VALUES!r}")
