from typing import Literal

RefreshOAuthProviderTokenProvider = Literal['apple', 'github', 'google', 'microsoft']

REFRESH_O_AUTH_PROVIDER_TOKEN_PROVIDER_VALUES: set[RefreshOAuthProviderTokenProvider] = { 'apple', 'github', 'google', 'microsoft',  }

def check_refresh_o_auth_provider_token_provider(value: str) -> RefreshOAuthProviderTokenProvider:
    if value in REFRESH_O_AUTH_PROVIDER_TOKEN_PROVIDER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {REFRESH_O_AUTH_PROVIDER_TOKEN_PROVIDER_VALUES!r}")
