from typing import Literal

AuthPageRadius = Literal['large', 'medium', 'none', 'small']

AUTH_PAGE_RADIUS_VALUES: set[AuthPageRadius] = { 'large', 'medium', 'none', 'small',  }

def check_auth_page_radius(value: str) -> AuthPageRadius:
    if value in AUTH_PAGE_RADIUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_PAGE_RADIUS_VALUES!r}")
