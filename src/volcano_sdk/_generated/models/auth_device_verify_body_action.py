from typing import Literal

AuthDeviceVerifyBodyAction = Literal['approve', 'deny']

AUTH_DEVICE_VERIFY_BODY_ACTION_VALUES: set[AuthDeviceVerifyBodyAction] = { 'approve', 'deny',  }

def check_auth_device_verify_body_action(value: str) -> AuthDeviceVerifyBodyAction:
    if value in AUTH_DEVICE_VERIFY_BODY_ACTION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_DEVICE_VERIFY_BODY_ACTION_VALUES!r}")
