from typing import Literal

DeleteOAuthConfigProvider = Literal['apple', 'device', 'github', 'google', 'microsoft']

DELETE_O_AUTH_CONFIG_PROVIDER_VALUES: set[DeleteOAuthConfigProvider] = { 'apple', 'device', 'github', 'google', 'microsoft',  }

def check_delete_o_auth_config_provider(value: str) -> DeleteOAuthConfigProvider:
    if value in DELETE_O_AUTH_CONFIG_PROVIDER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DELETE_O_AUTH_CONFIG_PROVIDER_VALUES!r}")
