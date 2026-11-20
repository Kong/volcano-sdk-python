from typing import Literal

IssueFindingSeverity = Literal['critical', 'major', 'minor', 'nit']

ISSUE_FINDING_SEVERITY_VALUES: set[IssueFindingSeverity] = { 'critical', 'major', 'minor', 'nit',  }

def check_issue_finding_severity(value: str) -> IssueFindingSeverity:
    if value in ISSUE_FINDING_SEVERITY_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {ISSUE_FINDING_SEVERITY_VALUES!r}")
