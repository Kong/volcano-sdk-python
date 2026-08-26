from typing import Literal

AuthLinkOAuthProviderProvider = Literal['apple', 'github', 'google', 'microsoft']

AUTH_LINK_O_AUTH_PROVIDER_PROVIDER_VALUES: set[AuthLinkOAuthProviderProvider] = { 'apple', 'github', 'google', 'microsoft',  }

def check_auth_link_o_auth_provider_provider(value: str) -> AuthLinkOAuthProviderProvider:
    if value in AUTH_LINK_O_AUTH_PROVIDER_PROVIDER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_LINK_O_AUTH_PROVIDER_PROVIDER_VALUES!r}")
