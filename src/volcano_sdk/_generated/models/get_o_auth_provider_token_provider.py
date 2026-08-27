from typing import Literal

GetOAuthProviderTokenProvider = Literal['apple', 'github', 'google', 'microsoft']

GET_O_AUTH_PROVIDER_TOKEN_PROVIDER_VALUES: set[GetOAuthProviderTokenProvider] = { 'apple', 'github', 'google', 'microsoft',  }

def check_get_o_auth_provider_token_provider(value: str) -> GetOAuthProviderTokenProvider:
    if value in GET_O_AUTH_PROVIDER_TOKEN_PROVIDER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_O_AUTH_PROVIDER_TOKEN_PROVIDER_VALUES!r}")
