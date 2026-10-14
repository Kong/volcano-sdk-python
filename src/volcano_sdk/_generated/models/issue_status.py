from typing import Literal

IssueStatus = Literal['ignored', 'open', 'resolved']

ISSUE_STATUS_VALUES: set[IssueStatus] = { 'ignored', 'open', 'resolved',  }

def check_issue_status(value: str) -> IssueStatus:
    if value in ISSUE_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {ISSUE_STATUS_VALUES!r}")
