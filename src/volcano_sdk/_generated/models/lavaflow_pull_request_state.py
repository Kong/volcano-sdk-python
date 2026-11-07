from typing import Literal

LavaflowPullRequestState = Literal['closed', 'merged', 'open']

LAVAFLOW_PULL_REQUEST_STATE_VALUES: set[LavaflowPullRequestState] = { 'closed', 'merged', 'open',  }

def check_lavaflow_pull_request_state(value: str) -> LavaflowPullRequestState:
    if value in LAVAFLOW_PULL_REQUEST_STATE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_PULL_REQUEST_STATE_VALUES!r}")
