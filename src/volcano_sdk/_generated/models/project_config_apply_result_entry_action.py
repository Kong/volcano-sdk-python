from typing import Literal

ProjectConfigApplyResultEntryAction = Literal['created', 'deleted', 'error', 'unchanged', 'updated']

PROJECT_CONFIG_APPLY_RESULT_ENTRY_ACTION_VALUES: set[ProjectConfigApplyResultEntryAction] = { 'created', 'deleted', 'error', 'unchanged', 'updated',  }

def check_project_config_apply_result_entry_action(value: str) -> ProjectConfigApplyResultEntryAction:
    if value in PROJECT_CONFIG_APPLY_RESULT_ENTRY_ACTION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_CONFIG_APPLY_RESULT_ENTRY_ACTION_VALUES!r}")
