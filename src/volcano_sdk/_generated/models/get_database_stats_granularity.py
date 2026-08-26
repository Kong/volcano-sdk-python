from typing import Literal

GetDatabaseStatsGranularity = Literal['daily', 'hourly', 'monthly']

GET_DATABASE_STATS_GRANULARITY_VALUES: set[GetDatabaseStatsGranularity] = { 'daily', 'hourly', 'monthly',  }

def check_get_database_stats_granularity(value: str) -> GetDatabaseStatsGranularity:
    if value in GET_DATABASE_STATS_GRANULARITY_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_DATABASE_STATS_GRANULARITY_VALUES!r}")
