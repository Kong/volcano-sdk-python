from typing import Literal

PublishSandboxPresetRequestMemoryMb = Literal[1024, 2048]

PUBLISH_SANDBOX_PRESET_REQUEST_MEMORY_MB_VALUES: set[PublishSandboxPresetRequestMemoryMb] = { 1024, 2048,  }

def check_publish_sandbox_preset_request_memory_mb(value: int) -> PublishSandboxPresetRequestMemoryMb:
    if value in PUBLISH_SANDBOX_PRESET_REQUEST_MEMORY_MB_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PUBLISH_SANDBOX_PRESET_REQUEST_MEMORY_MB_VALUES!r}")
