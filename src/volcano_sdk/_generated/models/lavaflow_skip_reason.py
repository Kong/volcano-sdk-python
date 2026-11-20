from typing import Literal

LavaflowSkipReason = Literal['convention_unsatisfiable', 'diagnose_only', 'duplicate_in_repository', 'lineage_cap', 'lineage_held', 'low_confidence', 'no_patch', 'not_fixable', 'permission_missing', 'possible_credential', 'possible_personal_data', 'publish_failed', 'pull_request_open', 'repository_changed', 'review_unresolved', 'security_finding', 'source_unavailable', 'ungated_workflows']

LAVAFLOW_SKIP_REASON_VALUES: set[LavaflowSkipReason] = { 'convention_unsatisfiable', 'diagnose_only', 'duplicate_in_repository', 'lineage_cap', 'lineage_held', 'low_confidence', 'no_patch', 'not_fixable', 'permission_missing', 'possible_credential', 'possible_personal_data', 'publish_failed', 'pull_request_open', 'repository_changed', 'review_unresolved', 'security_finding', 'source_unavailable', 'ungated_workflows',  }

def check_lavaflow_skip_reason(value: str) -> LavaflowSkipReason:
    if value in LAVAFLOW_SKIP_REASON_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_SKIP_REASON_VALUES!r}")
