from typing import Literal

AuthInsightsInterval = Literal['day', 'month', 'week']

AUTH_INSIGHTS_INTERVAL_VALUES: set[AuthInsightsInterval] = { 'day', 'month', 'week',  }

def check_auth_insights_interval(value: str) -> AuthInsightsInterval:
    if value in AUTH_INSIGHTS_INTERVAL_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_INSIGHTS_INTERVAL_VALUES!r}")
