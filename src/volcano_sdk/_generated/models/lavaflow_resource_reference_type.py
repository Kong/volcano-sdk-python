from typing import Literal

LavaflowResourceReferenceType = Literal['durable_function', 'frontend', 'function', 'project']

LAVAFLOW_RESOURCE_REFERENCE_TYPE_VALUES: set[LavaflowResourceReferenceType] = { 'durable_function', 'frontend', 'function', 'project',  }

def check_lavaflow_resource_reference_type(value: str) -> LavaflowResourceReferenceType:
    if value in LAVAFLOW_RESOURCE_REFERENCE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_RESOURCE_REFERENCE_TYPE_VALUES!r}")
