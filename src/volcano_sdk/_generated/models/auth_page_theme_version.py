from typing import Literal

AuthPageThemeVersion = Literal[1]

AUTH_PAGE_THEME_VERSION_VALUES: set[AuthPageThemeVersion] = { 1,  }

def check_auth_page_theme_version(value: int) -> AuthPageThemeVersion:
    if value in AUTH_PAGE_THEME_VERSION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_PAGE_THEME_VERSION_VALUES!r}")
