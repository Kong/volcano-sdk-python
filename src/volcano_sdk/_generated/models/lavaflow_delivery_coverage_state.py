from typing import Literal

LavaflowDeliveryCoverageState = Literal['merged', 'open']

LAVAFLOW_DELIVERY_COVERAGE_STATE_VALUES: set[LavaflowDeliveryCoverageState] = { 'merged', 'open',  }

def check_lavaflow_delivery_coverage_state(value: str) -> LavaflowDeliveryCoverageState:
    if value in LAVAFLOW_DELIVERY_COVERAGE_STATE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LAVAFLOW_DELIVERY_COVERAGE_STATE_VALUES!r}")
