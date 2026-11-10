from typing import Literal

ConnectorType = Literal['slack']

CONNECTOR_TYPE_VALUES: set[ConnectorType] = { 'slack',  }

def check_connector_type(value: str) -> ConnectorType:
    if value in CONNECTOR_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CONNECTOR_TYPE_VALUES!r}")
