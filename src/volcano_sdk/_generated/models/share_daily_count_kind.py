from typing import Literal

ShareDailyCountKind = Literal['accepted', 'click', 'confirm', 'failed', 'preview', 'ready']

SHARE_DAILY_COUNT_KIND_VALUES: set[ShareDailyCountKind] = { 'accepted', 'click', 'confirm', 'failed', 'preview', 'ready',  }

def check_share_daily_count_kind(value: str) -> ShareDailyCountKind:
    if value in SHARE_DAILY_COUNT_KIND_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SHARE_DAILY_COUNT_KIND_VALUES!r}")
