from typing import Literal

AuthPageDensity = Literal['comfortable', 'compact', 'spacious']

AUTH_PAGE_DENSITY_VALUES: set[AuthPageDensity] = { 'comfortable', 'compact', 'spacious',  }

def check_auth_page_density(value: str) -> AuthPageDensity:
    if value in AUTH_PAGE_DENSITY_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_PAGE_DENSITY_VALUES!r}")
