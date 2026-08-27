from typing import Literal

ProjectImportImpact = Literal['blocking', 'none', 'warning']

PROJECT_IMPORT_IMPACT_VALUES: set[ProjectImportImpact] = { 'blocking', 'none', 'warning',  }

def check_project_import_impact(value: str) -> ProjectImportImpact:
    if value in PROJECT_IMPORT_IMPACT_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_IMPORT_IMPACT_VALUES!r}")
