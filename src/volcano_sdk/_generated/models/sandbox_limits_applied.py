from typing import Literal

SandboxLimitsApplied = Literal['enforced', 'not_enforced', 'unknown']

SANDBOX_LIMITS_APPLIED_VALUES: set[SandboxLimitsApplied] = { 'enforced', 'not_enforced', 'unknown',  }

def check_sandbox_limits_applied(value: str) -> SandboxLimitsApplied:
    if value in SANDBOX_LIMITS_APPLIED_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SANDBOX_LIMITS_APPLIED_VALUES!r}")
