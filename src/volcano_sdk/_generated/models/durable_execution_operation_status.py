from typing import Literal

DurableExecutionOperationStatus = Literal['cancelled', 'failed', 'retrying', 'running', 'stopped', 'succeeded', 'timed_out', 'unknown', 'waiting']

DURABLE_EXECUTION_OPERATION_STATUS_VALUES: set[DurableExecutionOperationStatus] = { 'cancelled', 'failed', 'retrying', 'running', 'stopped', 'succeeded', 'timed_out', 'unknown', 'waiting',  }

def check_durable_execution_operation_status(value: str) -> DurableExecutionOperationStatus:
    if value in DURABLE_EXECUTION_OPERATION_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DURABLE_EXECUTION_OPERATION_STATUS_VALUES!r}")
