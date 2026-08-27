from typing import Literal

ProjectImportDisposition = Literal['automatic', 'deferred', 'manual', 'unsupported']

PROJECT_IMPORT_DISPOSITION_VALUES: set[ProjectImportDisposition] = { 'automatic', 'deferred', 'manual', 'unsupported',  }

def check_project_import_disposition(value: str) -> ProjectImportDisposition:
    if value in PROJECT_IMPORT_DISPOSITION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_IMPORT_DISPOSITION_VALUES!r}")
