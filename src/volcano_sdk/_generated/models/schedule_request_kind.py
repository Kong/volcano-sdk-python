from typing import Literal

ScheduleRequestKind = Literal['cron']

SCHEDULE_REQUEST_KIND_VALUES: set[ScheduleRequestKind] = { 'cron',  }

def check_schedule_request_kind(value: str) -> ScheduleRequestKind:
    if value in SCHEDULE_REQUEST_KIND_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SCHEDULE_REQUEST_KIND_VALUES!r}")
