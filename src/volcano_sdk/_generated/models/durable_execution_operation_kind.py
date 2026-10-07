from typing import Literal

DurableExecutionOperationKind = Literal['callback', 'child', 'execution', 'invoke', 'map', 'map_item', 'parallel', 'parallel_branch', 'step', 'wait', 'wait_until']

DURABLE_EXECUTION_OPERATION_KIND_VALUES: set[DurableExecutionOperationKind] = { 'callback', 'child', 'execution', 'invoke', 'map', 'map_item', 'parallel', 'parallel_branch', 'step', 'wait', 'wait_until',  }

def check_durable_execution_operation_kind(value: str) -> DurableExecutionOperationKind:
    if value in DURABLE_EXECUTION_OPERATION_KIND_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DURABLE_EXECUTION_OPERATION_KIND_VALUES!r}")
