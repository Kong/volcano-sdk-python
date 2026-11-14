from typing import Literal

FunctionServingActivationStatus = Literal['applied']

FUNCTION_SERVING_ACTIVATION_STATUS_VALUES: set[FunctionServingActivationStatus] = { 'applied',  }

def check_function_serving_activation_status(value: str) -> FunctionServingActivationStatus:
    if value in FUNCTION_SERVING_ACTIVATION_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_SERVING_ACTIVATION_STATUS_VALUES!r}")
