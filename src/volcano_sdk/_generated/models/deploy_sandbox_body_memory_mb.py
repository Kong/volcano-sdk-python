from typing import Literal

DeploySandboxBodyMemoryMb = Literal[1024, 2048]

DEPLOY_SANDBOX_BODY_MEMORY_MB_VALUES: set[DeploySandboxBodyMemoryMb] = { 1024, 2048,  }

def check_deploy_sandbox_body_memory_mb(value: int) -> DeploySandboxBodyMemoryMb:
    if value in DEPLOY_SANDBOX_BODY_MEMORY_MB_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DEPLOY_SANDBOX_BODY_MEMORY_MB_VALUES!r}")
