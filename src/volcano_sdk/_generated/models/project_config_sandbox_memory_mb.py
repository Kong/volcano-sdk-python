from typing import Literal

ProjectConfigSandboxMemoryMb = Literal[1024, 2048]

PROJECT_CONFIG_SANDBOX_MEMORY_MB_VALUES: set[ProjectConfigSandboxMemoryMb] = { 1024, 2048,  }

def check_project_config_sandbox_memory_mb(value: int) -> ProjectConfigSandboxMemoryMb:
    if value in PROJECT_CONFIG_SANDBOX_MEMORY_MB_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_CONFIG_SANDBOX_MEMORY_MB_VALUES!r}")
