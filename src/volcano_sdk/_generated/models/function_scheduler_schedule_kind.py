from typing import Literal

FunctionSchedulerScheduleKind = Literal['cron']

FUNCTION_SCHEDULER_SCHEDULE_KIND_VALUES: set[FunctionSchedulerScheduleKind] = { 'cron',  }

def check_function_scheduler_schedule_kind(value: str) -> FunctionSchedulerScheduleKind:
    if value in FUNCTION_SCHEDULER_SCHEDULE_KIND_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_SCHEDULER_SCHEDULE_KIND_VALUES!r}")
