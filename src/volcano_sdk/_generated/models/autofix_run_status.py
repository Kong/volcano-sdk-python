from typing import Literal

AutofixRunStatus = Literal['canceled', 'failed', 'queued', 'running', 'succeeded']

AUTOFIX_RUN_STATUS_VALUES: set[AutofixRunStatus] = { 'canceled', 'failed', 'queued', 'running', 'succeeded',  }

def check_autofix_run_status(value: str) -> AutofixRunStatus:
    if value in AUTOFIX_RUN_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTOFIX_RUN_STATUS_VALUES!r}")
