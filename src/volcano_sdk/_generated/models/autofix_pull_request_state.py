from typing import Literal

AutofixPullRequestState = Literal['closed', 'merged', 'open']

AUTOFIX_PULL_REQUEST_STATE_VALUES: set[AutofixPullRequestState] = { 'closed', 'merged', 'open',  }

def check_autofix_pull_request_state(value: str) -> AutofixPullRequestState:
    if value in AUTOFIX_PULL_REQUEST_STATE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTOFIX_PULL_REQUEST_STATE_VALUES!r}")
