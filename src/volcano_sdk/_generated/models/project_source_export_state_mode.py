from typing import Literal

ProjectSourceExportStateMode = Literal['git', 'git_exporting', 'git_pending', 'platform']

PROJECT_SOURCE_EXPORT_STATE_MODE_VALUES: set[ProjectSourceExportStateMode] = { 'git', 'git_exporting', 'git_pending', 'platform',  }

def check_project_source_export_state_mode(value: str) -> ProjectSourceExportStateMode:
    if value in PROJECT_SOURCE_EXPORT_STATE_MODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_SOURCE_EXPORT_STATE_MODE_VALUES!r}")
