from typing import Literal

AuthLinkOAuthProviderResponseMode = Literal['code']

AUTH_LINK_O_AUTH_PROVIDER_RESPONSE_MODE_VALUES: set[AuthLinkOAuthProviderResponseMode] = { 'code',  }

def check_auth_link_o_auth_provider_response_mode(value: str) -> AuthLinkOAuthProviderResponseMode:
    if value in AUTH_LINK_O_AUTH_PROVIDER_RESPONSE_MODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_LINK_O_AUTH_PROVIDER_RESPONSE_MODE_VALUES!r}")
