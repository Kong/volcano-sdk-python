from typing import Literal

HostedRenderablePageType = Literal['reset-password']

HOSTED_RENDERABLE_PAGE_TYPE_VALUES: set[HostedRenderablePageType] = { 'reset-password',  }

def check_hosted_renderable_page_type(value: str) -> HostedRenderablePageType:
    if value in HOSTED_RENDERABLE_PAGE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {HOSTED_RENDERABLE_PAGE_TYPE_VALUES!r}")
