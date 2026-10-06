from typing import Literal

SandboxTemplateStatus = Literal['deleting', 'ready', 'unavailable']

SANDBOX_TEMPLATE_STATUS_VALUES: set[SandboxTemplateStatus] = { 'deleting', 'ready', 'unavailable',  }

def check_sandbox_template_status(value: str) -> SandboxTemplateStatus:
    if value in SANDBOX_TEMPLATE_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SANDBOX_TEMPLATE_STATUS_VALUES!r}")
