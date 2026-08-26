from typing import Literal

GetOAuthConfigProvider = Literal['apple', 'device', 'github', 'google', 'microsoft']

GET_O_AUTH_CONFIG_PROVIDER_VALUES: set[GetOAuthConfigProvider] = { 'apple', 'device', 'github', 'google', 'microsoft',  }

def check_get_o_auth_config_provider(value: str) -> GetOAuthConfigProvider:
    if value in GET_O_AUTH_CONFIG_PROVIDER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_O_AUTH_CONFIG_PROVIDER_VALUES!r}")
