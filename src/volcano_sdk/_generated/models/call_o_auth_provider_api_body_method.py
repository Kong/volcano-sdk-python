from typing import Literal

CallOAuthProviderApiBodyMethod = Literal['GET', 'POST']

CALL_O_AUTH_PROVIDER_API_BODY_METHOD_VALUES: set[CallOAuthProviderApiBodyMethod] = { 'GET', 'POST',  }

def check_call_o_auth_provider_api_body_method(value: str) -> CallOAuthProviderApiBodyMethod:
    if value in CALL_O_AUTH_PROVIDER_API_BODY_METHOD_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CALL_O_AUTH_PROVIDER_API_BODY_METHOD_VALUES!r}")
