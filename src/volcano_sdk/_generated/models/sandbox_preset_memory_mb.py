from typing import Literal

SandboxPresetMemoryMb = Literal[1024, 2048]

SANDBOX_PRESET_MEMORY_MB_VALUES: set[SandboxPresetMemoryMb] = { 1024, 2048,  }

def check_sandbox_preset_memory_mb(value: int) -> SandboxPresetMemoryMb:
    if value in SANDBOX_PRESET_MEMORY_MB_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SANDBOX_PRESET_MEMORY_MB_VALUES!r}")
