from typing import Literal

UpdateOAuthConfigProvider = Literal['apple', 'device', 'github', 'google', 'microsoft']

UPDATE_O_AUTH_CONFIG_PROVIDER_VALUES: set[UpdateOAuthConfigProvider] = { 'apple', 'device', 'github', 'google', 'microsoft',  }

def check_update_o_auth_config_provider(value: str) -> UpdateOAuthConfigProvider:
    if value in UPDATE_O_AUTH_CONFIG_PROVIDER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {UPDATE_O_AUTH_CONFIG_PROVIDER_VALUES!r}")
