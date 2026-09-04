from typing import Literal

ListProjectsIncludeItem = Literal['git_connection', 'health']

LIST_PROJECTS_INCLUDE_ITEM_VALUES: set[ListProjectsIncludeItem] = { 'git_connection', 'health',  }

def check_list_projects_include_item(value: str) -> ListProjectsIncludeItem:
    if value in LIST_PROJECTS_INCLUDE_ITEM_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_PROJECTS_INCLUDE_ITEM_VALUES!r}")
