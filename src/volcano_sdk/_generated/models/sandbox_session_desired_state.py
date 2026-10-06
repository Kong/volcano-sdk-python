from typing import Literal

SandboxSessionDesiredState = Literal['running', 'suspended', 'terminated']

SANDBOX_SESSION_DESIRED_STATE_VALUES: set[SandboxSessionDesiredState] = { 'running', 'suspended', 'terminated',  }

def check_sandbox_session_desired_state(value: str) -> SandboxSessionDesiredState:
    if value in SANDBOX_SESSION_DESIRED_STATE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SANDBOX_SESSION_DESIRED_STATE_VALUES!r}")
