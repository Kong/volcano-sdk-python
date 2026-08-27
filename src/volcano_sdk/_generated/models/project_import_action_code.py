from typing import Literal

ProjectImportActionCode = Literal['frontend.configure', 'git.connect', 'project.create', 'variable.set']

PROJECT_IMPORT_ACTION_CODE_VALUES: set[ProjectImportActionCode] = { 'frontend.configure', 'git.connect', 'project.create', 'variable.set',  }

def check_project_import_action_code(value: str) -> ProjectImportActionCode:
    if value in PROJECT_IMPORT_ACTION_CODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_IMPORT_ACTION_CODE_VALUES!r}")
