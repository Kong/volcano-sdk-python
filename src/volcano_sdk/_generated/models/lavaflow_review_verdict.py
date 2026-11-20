from typing import Literal

LavaflowReviewVerdict = Literal['blocked', 'changes_requested', 'error', 'passed']

LAVAFLOW_REVIEW_VERDICT_VALUES: set[LavaflowReviewVerdict] = { 'blocked', 'changes_requested', 'error', 'passed',  }

def check_lavaflow_review_verdict(value: str) -> LavaflowReviewVerdict:
    if value in LAVAFLOW_REVIEW_VERDICT_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_REVIEW_VERDICT_VALUES!r}")
