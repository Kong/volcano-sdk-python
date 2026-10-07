from typing import Literal

DurableExecutionOperationType = Literal['callback', 'chained_invoke', 'context', 'execution', 'step', 'wait']

DURABLE_EXECUTION_OPERATION_TYPE_VALUES: set[DurableExecutionOperationType] = { 'callback', 'chained_invoke', 'context', 'execution', 'step', 'wait',  }

def check_durable_execution_operation_type(value: str) -> DurableExecutionOperationType:
    if value in DURABLE_EXECUTION_OPERATION_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DURABLE_EXECUTION_OPERATION_TYPE_VALUES!r}")
