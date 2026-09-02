from typing import Literal

AuthPageFont = Literal['geometric', 'humanist', 'mono', 'slab', 'system']

AUTH_PAGE_FONT_VALUES: set[AuthPageFont] = { 'geometric', 'humanist', 'mono', 'slab', 'system',  }

def check_auth_page_font(value: str) -> AuthPageFont:
    if value in AUTH_PAGE_FONT_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_PAGE_FONT_VALUES!r}")
