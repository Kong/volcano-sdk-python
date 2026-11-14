from typing import Literal

FunctionServingActivationKind = Literal['deploy', 'promotion', 'rollback']

FUNCTION_SERVING_ACTIVATION_KIND_VALUES: set[FunctionServingActivationKind] = { 'deploy', 'promotion', 'rollback',  }

def check_function_serving_activation_kind(value: str) -> FunctionServingActivationKind:
    if value in FUNCTION_SERVING_ACTIVATION_KIND_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FUNCTION_SERVING_ACTIVATION_KIND_VALUES!r}")
