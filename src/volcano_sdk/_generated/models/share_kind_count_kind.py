from typing import Literal

ShareKindCountKind = Literal['accepted', 'click', 'confirm', 'failed', 'preview', 'ready']

SHARE_KIND_COUNT_KIND_VALUES: set[ShareKindCountKind] = { 'accepted', 'click', 'confirm', 'failed', 'preview', 'ready',  }

def check_share_kind_count_kind(value: str) -> ShareKindCountKind:
    if value in SHARE_KIND_COUNT_KIND_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SHARE_KIND_COUNT_KIND_VALUES!r}")
