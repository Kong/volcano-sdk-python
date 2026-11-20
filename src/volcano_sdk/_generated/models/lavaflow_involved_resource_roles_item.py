from typing import Literal

LavaflowInvolvedResourceRolesItem = Literal['cause', 'fix', 'issue']

LAVAFLOW_INVOLVED_RESOURCE_ROLES_ITEM_VALUES: set[LavaflowInvolvedResourceRolesItem] = { 'cause', 'fix', 'issue',  }

def check_lavaflow_involved_resource_roles_item(value: str) -> LavaflowInvolvedResourceRolesItem:
    if value in LAVAFLOW_INVOLVED_RESOURCE_ROLES_ITEM_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_INVOLVED_RESOURCE_ROLES_ITEM_VALUES!r}")
