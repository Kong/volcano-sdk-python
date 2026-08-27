from typing import Literal

ResourceReferenceType = Literal['database', 'frontend', 'function', 'project']

RESOURCE_REFERENCE_TYPE_VALUES: set[ResourceReferenceType] = { 'database', 'frontend', 'function', 'project',  }

def check_resource_reference_type(value: str) -> ResourceReferenceType:
    if value in RESOURCE_REFERENCE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {RESOURCE_REFERENCE_TYPE_VALUES!r}")
