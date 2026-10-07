from typing import Literal

DurableExecutionOperationAttemptStatus = Literal['failed', 'running', 'succeeded']

DURABLE_EXECUTION_OPERATION_ATTEMPT_STATUS_VALUES: set[DurableExecutionOperationAttemptStatus] = { 'failed', 'running', 'succeeded',  }

def check_durable_execution_operation_attempt_status(value: str) -> DurableExecutionOperationAttemptStatus:
    if value in DURABLE_EXECUTION_OPERATION_ATTEMPT_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DURABLE_EXECUTION_OPERATION_ATTEMPT_STATUS_VALUES!r}")
