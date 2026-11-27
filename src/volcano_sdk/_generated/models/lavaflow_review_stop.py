from typing import Literal

LavaflowReviewStop = Literal['budget_exhausted', 'context_limit', 'no_revision', 'reviewers_failed', 'rounds', 'timed_out', 'too_few_reviewers', 'unreadable']

LAVAFLOW_REVIEW_STOP_VALUES: set[LavaflowReviewStop] = { 'budget_exhausted', 'context_limit', 'no_revision', 'reviewers_failed', 'rounds', 'timed_out', 'too_few_reviewers', 'unreadable',  }

def check_lavaflow_review_stop(value: str) -> LavaflowReviewStop:
    if value in LAVAFLOW_REVIEW_STOP_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_REVIEW_STOP_VALUES!r}")
