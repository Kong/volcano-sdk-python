from typing import Literal

GetLavaflowStatsCategory = Literal['bug', 'configuration', 'dependency', 'external', 'improvement', 'performance', 'security', 'uncategorized']

GET_LAVAFLOW_STATS_CATEGORY_VALUES: set[GetLavaflowStatsCategory] = { 'bug', 'configuration', 'dependency', 'external', 'improvement', 'performance', 'security', 'uncategorized',  }

def check_get_lavaflow_stats_category(value: str) -> GetLavaflowStatsCategory:
    if value in GET_LAVAFLOW_STATS_CATEGORY_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_LAVAFLOW_STATS_CATEGORY_VALUES!r}")
