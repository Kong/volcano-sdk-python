from typing import Literal

AuthUnlinkOAuthProviderProvider = Literal['apple', 'github', 'google', 'microsoft']

AUTH_UNLINK_O_AUTH_PROVIDER_PROVIDER_VALUES: set[AuthUnlinkOAuthProviderProvider] = { 'apple', 'github', 'google', 'microsoft',  }

def check_auth_unlink_o_auth_provider_provider(value: str) -> AuthUnlinkOAuthProviderProvider:
    if value in AUTH_UNLINK_O_AUTH_PROVIDER_PROVIDER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_UNLINK_O_AUTH_PROVIDER_PROVIDER_VALUES!r}")
