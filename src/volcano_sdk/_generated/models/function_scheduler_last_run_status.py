from typing import Literal

FunctionSchedulerLastRunStatus = Literal['failed', 'succeeded']

FUNCTION_SCHEDULER_LAST_RUN_STATUS_VALUES: set[FunctionSchedulerLastRunStatus] = { 'failed', 'succeeded',  }

def check_function_scheduler_last_run_status(value: str) -> FunctionSchedulerLastRunStatus:
    if value in FUNCTION_SCHEDULER_LAST_RUN_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_SCHEDULER_LAST_RUN_STATUS_VALUES!r}")
