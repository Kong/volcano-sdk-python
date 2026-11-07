from typing import Literal

ShareReleaseFunctionKind = Literal['durable', 'standard']

SHARE_RELEASE_FUNCTION_KIND_VALUES: set[ShareReleaseFunctionKind] = { 'durable', 'standard',  }

def check_share_release_function_kind(value: str) -> ShareReleaseFunctionKind:
    if value in SHARE_RELEASE_FUNCTION_KIND_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SHARE_RELEASE_FUNCTION_KIND_VALUES!r}")
