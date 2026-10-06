from typing import Literal

CallOAuthProviderApiResponse200Provider = Literal['apple', 'github', 'google', 'microsoft']

CALL_O_AUTH_PROVIDER_API_RESPONSE_200_PROVIDER_VALUES: set[CallOAuthProviderApiResponse200Provider] = { 'apple', 'github', 'google', 'microsoft',  }

def check_call_o_auth_provider_api_response_200_provider(value: str) -> CallOAuthProviderApiResponse200Provider:
    if value in CALL_O_AUTH_PROVIDER_API_RESPONSE_200_PROVIDER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CALL_O_AUTH_PROVIDER_API_RESPONSE_200_PROVIDER_VALUES!r}")
