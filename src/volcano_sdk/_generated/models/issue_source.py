from typing import Literal

IssueSource = Literal['build', 'code_quality', 'report', 'request', 'runtime']

ISSUE_SOURCE_VALUES: set[IssueSource] = { 'build', 'code_quality', 'report', 'request', 'runtime',  }

def check_issue_source(value: str) -> IssueSource:
    if value in ISSUE_SOURCE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {ISSUE_SOURCE_VALUES!r}")
