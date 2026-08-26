from typing import Literal

RenderDefaultManagedAuthPageAction = Literal['device', 'forgot-password', 'login', 'signup']

RENDER_DEFAULT_MANAGED_AUTH_PAGE_ACTION_VALUES: set[RenderDefaultManagedAuthPageAction] = { 'device', 'forgot-password', 'login', 'signup',  }

def check_render_default_managed_auth_page_action(value: str) -> RenderDefaultManagedAuthPageAction:
    if value in RENDER_DEFAULT_MANAGED_AUTH_PAGE_ACTION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {RENDER_DEFAULT_MANAGED_AUTH_PAGE_ACTION_VALUES!r}")
