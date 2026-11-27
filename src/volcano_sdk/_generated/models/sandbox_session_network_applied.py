from typing import Literal

SandboxSessionNetworkApplied = Literal['default', 'deny_all', 'unknown']

SANDBOX_SESSION_NETWORK_APPLIED_VALUES: set[SandboxSessionNetworkApplied] = { 'default', 'deny_all', 'unknown',  }

def check_sandbox_session_network_applied(value: str) -> SandboxSessionNetworkApplied:
    if value in SANDBOX_SESSION_NETWORK_APPLIED_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SANDBOX_SESSION_NETWORK_APPLIED_VALUES!r}")
