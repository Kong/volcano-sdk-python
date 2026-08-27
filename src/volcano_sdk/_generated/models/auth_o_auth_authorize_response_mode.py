from typing import Literal

AuthOAuthAuthorizeResponseMode = Literal['code']

AUTH_O_AUTH_AUTHORIZE_RESPONSE_MODE_VALUES: set[AuthOAuthAuthorizeResponseMode] = { 'code',  }

def check_auth_o_auth_authorize_response_mode(value: str) -> AuthOAuthAuthorizeResponseMode:
    if value in AUTH_O_AUTH_AUTHORIZE_RESPONSE_MODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_O_AUTH_AUTHORIZE_RESPONSE_MODE_VALUES!r}")
