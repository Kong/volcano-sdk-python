from typing import Literal

AikidoSeverity = Literal['critical', 'high', 'low', 'medium']

AIKIDO_SEVERITY_VALUES: set[AikidoSeverity] = { 'critical', 'high', 'low', 'medium',  }

def check_aikido_severity(value: str) -> AikidoSeverity:
    if value in AIKIDO_SEVERITY_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AIKIDO_SEVERITY_VALUES!r}")
