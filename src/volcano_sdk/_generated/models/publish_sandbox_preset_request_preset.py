from typing import Literal

PublishSandboxPresetRequestPreset = Literal['node22', 'python3.12']

PUBLISH_SANDBOX_PRESET_REQUEST_PRESET_VALUES: set[PublishSandboxPresetRequestPreset] = { 'node22', 'python3.12',  }

def check_publish_sandbox_preset_request_preset(value: str) -> PublishSandboxPresetRequestPreset:
    if value in PUBLISH_SANDBOX_PRESET_REQUEST_PRESET_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PUBLISH_SANDBOX_PRESET_REQUEST_PRESET_VALUES!r}")
