from typing import Literal

ListLavaflowRunsPullRequestState = Literal['closed', 'merged', 'none', 'open']

LIST_LAVAFLOW_RUNS_PULL_REQUEST_STATE_VALUES: set[ListLavaflowRunsPullRequestState] = { 'closed', 'merged', 'none', 'open',  }

def check_list_lavaflow_runs_pull_request_state(value: str) -> ListLavaflowRunsPullRequestState:
    if value in LIST_LAVAFLOW_RUNS_PULL_REQUEST_STATE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_LAVAFLOW_RUNS_PULL_REQUEST_STATE_VALUES!r}")
