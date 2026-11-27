from typing import Literal

SandboxSessionNetworkRequestEgress = Literal['default', 'deny_all']

SANDBOX_SESSION_NETWORK_REQUEST_EGRESS_VALUES: set[SandboxSessionNetworkRequestEgress] = { 'default', 'deny_all',  }

def check_sandbox_session_network_request_egress(value: str) -> SandboxSessionNetworkRequestEgress:
    if value in SANDBOX_SESSION_NETWORK_REQUEST_EGRESS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SANDBOX_SESSION_NETWORK_REQUEST_EGRESS_VALUES!r}")
