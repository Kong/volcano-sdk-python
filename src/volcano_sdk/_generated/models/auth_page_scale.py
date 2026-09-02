from typing import Literal

AuthPageScale = Literal['default', 'large', 'small']

AUTH_PAGE_SCALE_VALUES: set[AuthPageScale] = { 'default', 'large', 'small',  }

def check_auth_page_scale(value: str) -> AuthPageScale:
    if value in AUTH_PAGE_SCALE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_PAGE_SCALE_VALUES!r}")
