from typing import Literal

ProjectConfigOAuthProviderProvider = Literal['apple', 'device', 'github', 'google', 'microsoft']

PROJECT_CONFIG_O_AUTH_PROVIDER_PROVIDER_VALUES: set[ProjectConfigOAuthProviderProvider] = { 'apple', 'device', 'github', 'google', 'microsoft',  }

def check_project_config_o_auth_provider_provider(value: str) -> ProjectConfigOAuthProviderProvider:
    if value in PROJECT_CONFIG_O_AUTH_PROVIDER_PROVIDER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_CONFIG_O_AUTH_PROVIDER_PROVIDER_VALUES!r}")
