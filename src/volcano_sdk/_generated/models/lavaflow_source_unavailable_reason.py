from typing import Literal

LavaflowSourceUnavailableReason = Literal['commit_not_on_production_branch', 'deployment_unattributed', 'no_commit', 'no_repository', 'other_repository', 'repository_unreadable', 'uncommitted_changes', 'unverified_commit']

LAVAFLOW_SOURCE_UNAVAILABLE_REASON_VALUES: set[LavaflowSourceUnavailableReason] = { 'commit_not_on_production_branch', 'deployment_unattributed', 'no_commit', 'no_repository', 'other_repository', 'repository_unreadable', 'uncommitted_changes', 'unverified_commit',  }

def check_lavaflow_source_unavailable_reason(value: str) -> LavaflowSourceUnavailableReason:
    if value in LAVAFLOW_SOURCE_UNAVAILABLE_REASON_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_SOURCE_UNAVAILABLE_REASON_VALUES!r}")
