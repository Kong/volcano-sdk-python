from typing import Literal

CreateSandboxTemplateRequestPreset = Literal['node22', 'python3.12']

CREATE_SANDBOX_TEMPLATE_REQUEST_PRESET_VALUES: set[CreateSandboxTemplateRequestPreset] = { 'node22', 'python3.12',  }

def check_create_sandbox_template_request_preset(value: str) -> CreateSandboxTemplateRequestPreset:
    if value in CREATE_SANDBOX_TEMPLATE_REQUEST_PRESET_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_SANDBOX_TEMPLATE_REQUEST_PRESET_VALUES!r}")
