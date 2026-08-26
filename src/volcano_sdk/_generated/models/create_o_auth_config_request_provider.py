from typing import Literal

CreateOAuthConfigRequestProvider = Literal['apple', 'device', 'github', 'google', 'microsoft']

CREATE_O_AUTH_CONFIG_REQUEST_PROVIDER_VALUES: set[CreateOAuthConfigRequestProvider] = { 'apple', 'device', 'github', 'google', 'microsoft',  }

def check_create_o_auth_config_request_provider(value: str) -> CreateOAuthConfigRequestProvider:
    if value in CREATE_O_AUTH_CONFIG_REQUEST_PROVIDER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_O_AUTH_CONFIG_REQUEST_PROVIDER_VALUES!r}")
