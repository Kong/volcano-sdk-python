from typing import Literal

FunctionProductionEnvironmentStatus = Literal['current', 'out_of_date']

FUNCTION_PRODUCTION_ENVIRONMENT_STATUS_VALUES: set[FunctionProductionEnvironmentStatus] = { 'current', 'out_of_date',  }

def check_function_production_environment_status(value: str) -> FunctionProductionEnvironmentStatus:
    if value in FUNCTION_PRODUCTION_ENVIRONMENT_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_PRODUCTION_ENVIRONMENT_STATUS_VALUES!r}")
