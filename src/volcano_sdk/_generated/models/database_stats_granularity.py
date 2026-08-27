from typing import Literal

DatabaseStatsGranularity = Literal['daily', 'hourly', 'monthly']

DATABASE_STATS_GRANULARITY_VALUES: set[DatabaseStatsGranularity] = { 'daily', 'hourly', 'monthly',  }

def check_database_stats_granularity(value: str) -> DatabaseStatsGranularity:
    if value in DATABASE_STATS_GRANULARITY_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATABASE_STATS_GRANULARITY_VALUES!r}")
