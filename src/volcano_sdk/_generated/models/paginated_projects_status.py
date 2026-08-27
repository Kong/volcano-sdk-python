from typing import Literal

PaginatedProjectsStatus = Literal['active', 'failed', 'provisioning']

PAGINATED_PROJECTS_STATUS_VALUES: set[PaginatedProjectsStatus] = { 'active', 'failed', 'provisioning',  }

def check_paginated_projects_status(value: str) -> PaginatedProjectsStatus:
    if value in PAGINATED_PROJECTS_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PAGINATED_PROJECTS_STATUS_VALUES!r}")
