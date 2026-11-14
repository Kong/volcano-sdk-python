from typing import Literal

SchedulerFailureNotifyOn = Literal['consecutive_failures', 'first_failure']

SCHEDULER_FAILURE_NOTIFY_ON_VALUES: set[SchedulerFailureNotifyOn] = { 'consecutive_failures', 'first_failure',  }

def check_scheduler_failure_notify_on(value: str) -> SchedulerFailureNotifyOn:
    if value in SCHEDULER_FAILURE_NOTIFY_ON_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SCHEDULER_FAILURE_NOTIFY_ON_VALUES!r}")
