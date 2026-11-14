from typing import Literal

AikidoRegion = Literal['au', 'eu', 'me', 'us']

AIKIDO_REGION_VALUES: set[AikidoRegion] = { 'au', 'eu', 'me', 'us',  }

def check_aikido_region(value: str) -> AikidoRegion:
    if value in AIKIDO_REGION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AIKIDO_REGION_VALUES!r}")
