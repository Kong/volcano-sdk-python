from typing import Literal

CallOAuthProviderAPIProvider = Literal['apple', 'github', 'google', 'microsoft']

CALL_O_AUTH_PROVIDER_API_PROVIDER_VALUES: set[CallOAuthProviderAPIProvider] = { 'apple', 'github', 'google', 'microsoft',  }

def check_call_o_auth_provider_api_provider(value: str) -> CallOAuthProviderAPIProvider:
    if value in CALL_O_AUTH_PROVIDER_API_PROVIDER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CALL_O_AUTH_PROVIDER_API_PROVIDER_VALUES!r}")
