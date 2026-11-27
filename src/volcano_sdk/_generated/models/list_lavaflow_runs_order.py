from typing import Literal

ListLavaflowRunsOrder = Literal['created_at.asc', 'created_at.desc', 'issue_events.desc']

LIST_LAVAFLOW_RUNS_ORDER_VALUES: set[ListLavaflowRunsOrder] = { 'created_at.asc', 'created_at.desc', 'issue_events.desc',  }

def check_list_lavaflow_runs_order(value: str) -> ListLavaflowRunsOrder:
    if value in LIST_LAVAFLOW_RUNS_ORDER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_LAVAFLOW_RUNS_ORDER_VALUES!r}")
