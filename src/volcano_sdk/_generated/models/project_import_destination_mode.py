from typing import Literal

ProjectImportDestinationMode = Literal['create']

PROJECT_IMPORT_DESTINATION_MODE_VALUES: set[ProjectImportDestinationMode] = { 'create',  }

def check_project_import_destination_mode(value: str) -> ProjectImportDestinationMode:
    if value in PROJECT_IMPORT_DESTINATION_MODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_IMPORT_DESTINATION_MODE_VALUES!r}")
