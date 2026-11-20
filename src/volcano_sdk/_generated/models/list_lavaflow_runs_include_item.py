from typing import Literal

ListLavaflowRunsIncludeItem = Literal['counts']

LIST_LAVAFLOW_RUNS_INCLUDE_ITEM_VALUES: set[ListLavaflowRunsIncludeItem] = { 'counts',  }

def check_list_lavaflow_runs_include_item(value: str) -> ListLavaflowRunsIncludeItem:
    if value in LIST_LAVAFLOW_RUNS_INCLUDE_ITEM_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_LAVAFLOW_RUNS_INCLUDE_ITEM_VALUES!r}")
