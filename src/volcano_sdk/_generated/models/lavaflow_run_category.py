from typing import Literal

LavaflowRunCategory = Literal['bug', 'configuration', 'dependency', 'external', 'improvement', 'performance', 'security']

LAVAFLOW_RUN_CATEGORY_VALUES: set[LavaflowRunCategory] = { 'bug', 'configuration', 'dependency', 'external', 'improvement', 'performance', 'security',  }

def check_lavaflow_run_category(value: str) -> LavaflowRunCategory:
    if value in LAVAFLOW_RUN_CATEGORY_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_RUN_CATEGORY_VALUES!r}")
