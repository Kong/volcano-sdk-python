from typing import Literal

FunctionSchedulerHealth = Literal['failing', 'healthy']

FUNCTION_SCHEDULER_HEALTH_VALUES: set[FunctionSchedulerHealth] = { 'failing', 'healthy',  }

def check_function_scheduler_health(value: str) -> FunctionSchedulerHealth:
    if value in FUNCTION_SCHEDULER_HEALTH_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_SCHEDULER_HEALTH_VALUES!r}")
