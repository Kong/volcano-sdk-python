from typing import Literal

ListLavaflowResourcesCategory = Literal['bug', 'configuration', 'dependency', 'external', 'improvement', 'performance', 'security', 'uncategorized']

LIST_LAVAFLOW_RESOURCES_CATEGORY_VALUES: set[ListLavaflowResourcesCategory] = { 'bug', 'configuration', 'dependency', 'external', 'improvement', 'performance', 'security', 'uncategorized',  }

def check_list_lavaflow_resources_category(value: str) -> ListLavaflowResourcesCategory:
    if value in LIST_LAVAFLOW_RESOURCES_CATEGORY_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_LAVAFLOW_RESOURCES_CATEGORY_VALUES!r}")
