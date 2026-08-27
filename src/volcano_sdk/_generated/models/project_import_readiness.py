from typing import Literal

ProjectImportReadiness = Literal['blocked', 'importable', 'needs_input']

PROJECT_IMPORT_READINESS_VALUES: set[ProjectImportReadiness] = { 'blocked', 'importable', 'needs_input',  }

def check_project_import_readiness(value: str) -> ProjectImportReadiness:
    if value in PROJECT_IMPORT_READINESS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_IMPORT_READINESS_VALUES!r}")
