from typing import Literal

ListLavaflowRunsCategory = Literal['bug', 'configuration', 'dependency', 'external', 'improvement', 'performance', 'security', 'uncategorized']

LIST_LAVAFLOW_RUNS_CATEGORY_VALUES: set[ListLavaflowRunsCategory] = { 'bug', 'configuration', 'dependency', 'external', 'improvement', 'performance', 'security', 'uncategorized',  }

def check_list_lavaflow_runs_category(value: str) -> ListLavaflowRunsCategory:
    if value in LIST_LAVAFLOW_RUNS_CATEGORY_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_LAVAFLOW_RUNS_CATEGORY_VALUES!r}")
