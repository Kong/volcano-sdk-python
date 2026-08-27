from typing import Literal

LiveLogLevel = Literal['debug', 'error', 'fatal', 'info', 'trace', 'warn']

LIVE_LOG_LEVEL_VALUES: set[LiveLogLevel] = { 'debug', 'error', 'fatal', 'info', 'trace', 'warn',  }

def check_live_log_level(value: str) -> LiveLogLevel:
    if value in LIVE_LOG_LEVEL_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIVE_LOG_LEVEL_VALUES!r}")
