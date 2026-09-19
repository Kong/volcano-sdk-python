from typing import Literal

DurableExecutionStatus = Literal['failed', 'pending', 'running', 'stopped', 'succeeded', 'timed_out', 'unknown']

DURABLE_EXECUTION_STATUS_VALUES: set[DurableExecutionStatus] = { 'failed', 'pending', 'running', 'stopped', 'succeeded', 'timed_out', 'unknown',  }

def check_durable_execution_status(value: str) -> DurableExecutionStatus:
    if value in DURABLE_EXECUTION_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DURABLE_EXECUTION_STATUS_VALUES!r}")
