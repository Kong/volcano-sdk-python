from typing import Literal

IssueSource = Literal['code_quality', 'report', 'runtime']

ISSUE_SOURCE_VALUES: set[IssueSource] = { 'code_quality', 'report', 'runtime',  }

def check_issue_source(value: str) -> IssueSource:
    if value in ISSUE_SOURCE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {ISSUE_SOURCE_VALUES!r}")
