from typing import Literal

LavaflowIssueSummarySeverity = Literal['critical', 'major', 'minor', 'nit']

LAVAFLOW_ISSUE_SUMMARY_SEVERITY_VALUES: set[LavaflowIssueSummarySeverity] = { 'critical', 'major', 'minor', 'nit',  }

def check_lavaflow_issue_summary_severity(value: str) -> LavaflowIssueSummarySeverity:
    if value in LAVAFLOW_ISSUE_SUMMARY_SEVERITY_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_ISSUE_SUMMARY_SEVERITY_VALUES!r}")
