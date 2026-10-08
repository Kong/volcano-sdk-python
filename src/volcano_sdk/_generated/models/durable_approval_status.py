from typing import Literal

DurableApprovalStatus = Literal['approved', 'cancelled', 'denied', 'expired', 'pending']

DURABLE_APPROVAL_STATUS_VALUES: set[DurableApprovalStatus] = { 'approved', 'cancelled', 'denied', 'expired', 'pending',  }

def check_durable_approval_status(value: str) -> DurableApprovalStatus:
    if value in DURABLE_APPROVAL_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DURABLE_APPROVAL_STATUS_VALUES!r}")
