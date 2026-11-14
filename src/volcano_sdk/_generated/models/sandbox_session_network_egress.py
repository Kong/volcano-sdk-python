from typing import Literal

SandboxSessionNetworkEgress = Literal['default', 'deny_all']

SANDBOX_SESSION_NETWORK_EGRESS_VALUES: set[SandboxSessionNetworkEgress] = { 'default', 'deny_all',  }

def check_sandbox_session_network_egress(value: str) -> SandboxSessionNetworkEgress:
    if value in SANDBOX_SESSION_NETWORK_EGRESS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SANDBOX_SESSION_NETWORK_EGRESS_VALUES!r}")
