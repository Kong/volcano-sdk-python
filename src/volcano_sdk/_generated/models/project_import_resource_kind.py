from typing import Literal

ProjectImportResourceKind = Literal['domain', 'frontend', 'git_repository', 'project', 'variable']

PROJECT_IMPORT_RESOURCE_KIND_VALUES: set[ProjectImportResourceKind] = { 'domain', 'frontend', 'git_repository', 'project', 'variable',  }

def check_project_import_resource_kind(value: str) -> ProjectImportResourceKind:
    if value in PROJECT_IMPORT_RESOURCE_KIND_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_IMPORT_RESOURCE_KIND_VALUES!r}")
