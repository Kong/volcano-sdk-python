from typing import Literal

AuthDeviceTokenBodyGrantType = Literal['urn:ietf:params:oauth:grant-type:device_code']

AUTH_DEVICE_TOKEN_BODY_GRANT_TYPE_VALUES: set[AuthDeviceTokenBodyGrantType] = { 'urn:ietf:params:oauth:grant-type:device_code',  }

def check_auth_device_token_body_grant_type(value: str) -> AuthDeviceTokenBodyGrantType:
    if value in AUTH_DEVICE_TOKEN_BODY_GRANT_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_DEVICE_TOKEN_BODY_GRANT_TYPE_VALUES!r}")
