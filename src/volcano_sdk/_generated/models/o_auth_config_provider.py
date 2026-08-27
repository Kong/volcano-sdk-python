from typing import Literal

OAuthConfigProvider = Literal['apple', 'device', 'github', 'google', 'microsoft']

O_AUTH_CONFIG_PROVIDER_VALUES: set[OAuthConfigProvider] = { 'apple', 'device', 'github', 'google', 'microsoft',  }

def check_o_auth_config_provider(value: str) -> OAuthConfigProvider:
    if value in O_AUTH_CONFIG_PROVIDER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {O_AUTH_CONFIG_PROVIDER_VALUES!r}")
