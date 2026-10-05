from typing import Literal

CreateSandboxTemplateRequestMemoryMb = Literal[1024, 2048]

CREATE_SANDBOX_TEMPLATE_REQUEST_MEMORY_MB_VALUES: set[CreateSandboxTemplateRequestMemoryMb] = { 1024, 2048,  }

def check_create_sandbox_template_request_memory_mb(value: int) -> CreateSandboxTemplateRequestMemoryMb:
    if value in CREATE_SANDBOX_TEMPLATE_REQUEST_MEMORY_MB_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_SANDBOX_TEMPLATE_REQUEST_MEMORY_MB_VALUES!r}")
