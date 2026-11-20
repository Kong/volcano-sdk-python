from typing import Literal

ProjectGitOwnerPushReason = Literal['no_push_permission', 'owner_not_connected', 'owner_reconnect_required', 'repository_access_lost']

PROJECT_GIT_OWNER_PUSH_REASON_VALUES: set[ProjectGitOwnerPushReason] = { 'no_push_permission', 'owner_not_connected', 'owner_reconnect_required', 'repository_access_lost',  }

def check_project_git_owner_push_reason(value: str) -> ProjectGitOwnerPushReason:
    if value in PROJECT_GIT_OWNER_PUSH_REASON_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_GIT_OWNER_PUSH_REASON_VALUES!r}")
