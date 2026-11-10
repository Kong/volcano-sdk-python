from typing import Literal

LavaflowDraftReason = Literal['converted_to_draft', 'open_pr', 'review_unresolved']

LAVAFLOW_DRAFT_REASON_VALUES: set[LavaflowDraftReason] = { 'converted_to_draft', 'open_pr', 'review_unresolved',  }

def check_lavaflow_draft_reason(value: str) -> LavaflowDraftReason:
    if value in LAVAFLOW_DRAFT_REASON_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_DRAFT_REASON_VALUES!r}")
