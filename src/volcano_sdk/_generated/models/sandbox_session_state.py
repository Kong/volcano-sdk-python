from typing import Literal

SandboxSessionState = Literal['resuming', 'running', 'starting', 'suspended', 'suspending', 'terminated', 'terminating', 'unknown']

SANDBOX_SESSION_STATE_VALUES: set[SandboxSessionState] = { 'resuming', 'running', 'starting', 'suspended', 'suspending', 'terminated', 'terminating', 'unknown',  }

def check_sandbox_session_state(value: str) -> SandboxSessionState:
    if value in SANDBOX_SESSION_STATE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SANDBOX_SESSION_STATE_VALUES!r}")
