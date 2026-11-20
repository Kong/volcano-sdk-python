from typing import Literal

ConnectorCreateType = Literal['aikido']

CONNECTOR_CREATE_TYPE_VALUES: set[ConnectorCreateType] = { 'aikido',  }

def check_connector_create_type(value: str) -> ConnectorCreateType:
    if value in CONNECTOR_CREATE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CONNECTOR_CREATE_TYPE_VALUES!r}")
