from typing import Literal

AuthPageLayout = Literal['centered', 'split-left', 'split-right']

AUTH_PAGE_LAYOUT_VALUES: set[AuthPageLayout] = { 'centered', 'split-left', 'split-right',  }

def check_auth_page_layout(value: str) -> AuthPageLayout:
    if value in AUTH_PAGE_LAYOUT_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_PAGE_LAYOUT_VALUES!r}")
