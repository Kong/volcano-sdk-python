"""Generated auth account operation adapters."""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
)

import httpx

from ._generated.api.authentication.auth_delete_all_my_sessions import (
    request_kwargs as delete_all_my_sessions_kwargs,
)
from ._generated.api.authentication.auth_delete_my_session import (
    request_kwargs as delete_my_session_kwargs,
)
from ._generated.api.authentication.auth_get_my_sessions import (
    request_kwargs as get_my_sessions_kwargs,
)
from ._generated.api.o_auth_authentication import auth_o_auth_exchange
from ._generated.api.o_auth_authentication.auth_link_o_auth_provider import (
    request_kwargs as link_oauth_provider_kwargs,
)
from ._generated.api.o_auth_authentication.auth_list_o_auth_providers import (
    request_kwargs as list_oauth_providers_kwargs,
)
from ._generated.api.o_auth_authentication.auth_o_auth_authorize import (
    request_kwargs as oauth_authorize_kwargs,
)
from ._generated.api.o_auth_authentication.auth_unlink_o_auth_provider import (
    request_kwargs as unlink_oauth_provider_kwargs,
)
from ._generated.api.o_auth_authentication.call_o_auth_provider_api import (
    request_kwargs as call_oauth_provider_api_kwargs,
)
from ._generated.api.o_auth_authentication.get_o_auth_provider_token import (
    request_kwargs as get_oauth_provider_token_kwargs,
)
from ._generated.api.o_auth_authentication.refresh_o_auth_provider_token import (
    request_kwargs as refresh_oauth_provider_token_kwargs,
)
from ._generated.models.auth_get_my_sessions_response_200 import (
    AuthGetMySessionsResponse200,
)
from ._generated.models.auth_link_o_auth_provider_response_200 import (
    AuthLinkOAuthProviderResponse200,
)
from ._generated.models.auth_list_o_auth_providers_response_200 import (
    AuthListOAuthProvidersResponse200,
)
from ._generated.models.auth_o_auth_exchange_body import AuthOAuthExchangeBody
from ._generated.models.call_o_auth_provider_api_body import CallOAuthProviderAPIBody
from ._generated.models.call_o_auth_provider_api_response_200 import (
    CallOAuthProviderAPIResponse200,
)
from ._generated.models.get_o_auth_provider_token_response_200 import (
    GetOAuthProviderTokenResponse200,
)
from ._generated.models.refresh_o_auth_provider_token_response_200 import (
    RefreshOAuthProviderTokenResponse200,
)
from ._transport_base import TransportBase
from ._transport_response import (
    generated_request,
    json_object,
    parsed_response,
    plain_json,
    unparsed_response,
)
from ._transport_types import (
    HTTP_OK,
    MALFORMED_LINKED_OAUTH_PROVIDERS,
    MALFORMED_OAUTH_API_RESPONSE,
    MALFORMED_OAUTH_LINK,
    MALFORMED_OAUTH_STATUS,
    MALFORMED_SESSION_PAGE,
    GeneratedTransportResponse,
    TransportResponse,
)
from .errors import (
    VolcanoError,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

    from ._generated.models.auth_link_o_auth_provider_provider import (
        AuthLinkOAuthProviderProvider,
    )
    from ._generated.models.auth_o_auth_authorize_provider import (
        AuthOAuthAuthorizeProvider,
    )
    from ._generated.models.auth_unlink_o_auth_provider_provider import (
        AuthUnlinkOAuthProviderProvider,
    )
    from ._generated.models.call_o_auth_provider_api_provider import (
        CallOAuthProviderAPIProvider,
    )
    from ._generated.models.get_o_auth_provider_token_provider import (
        GetOAuthProviderTokenProvider,
    )
    from ._generated.models.refresh_o_auth_provider_token_provider import (
        RefreshOAuthProviderTokenProvider,
    )
    from .models import JSONValue


class AuthAccountTransport(TransportBase):
    """Adapt generated auth account operations to the SDK transport."""

    def auth_delete_all_my_sessions(
        self,
        *,
        authorization: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = generated_request(client, delete_all_my_sessions_kwargs())
        return unparsed_response(response)

    def auth_delete_my_session(
        self,
        *,
        authorization: str,
        session_id: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = generated_request(
                client, delete_my_session_kwargs(session_id=session_id)
            )
        return unparsed_response(response)

    def auth_get_my_sessions(
        self,
        *,
        authorization: str,
        page: int,
        limit: int,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = generated_request(
                client, get_my_sessions_kwargs(page=page, limit=limit)
            )
        if response.status_code != HTTP_OK:
            return unparsed_response(response)
        try:
            payload = AuthGetMySessionsResponse200.from_dict(json_object(response))
        except (
            AttributeError,
            KeyError,
            TypeError,
            UnicodeDecodeError,
            ValueError,
        ) as error:
            raise VolcanoError(MALFORMED_SESSION_PAGE) from error
        return GeneratedTransportResponse(
            status_code=response.status_code,
            payload=payload,
            content=response.content,
            headers=dict(response.headers),
        )

    def auth_list_oauth_providers(
        self,
        *,
        authorization: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = generated_request(client, list_oauth_providers_kwargs())
        if response.status_code != HTTP_OK:
            return unparsed_response(response)
        try:
            payload = AuthListOAuthProvidersResponse200.from_dict(json_object(response))
        except (
            AttributeError,
            KeyError,
            TypeError,
            UnicodeDecodeError,
            ValueError,
        ) as error:
            raise VolcanoError(MALFORMED_LINKED_OAUTH_PROVIDERS) from error
        return GeneratedTransportResponse(
            status_code=response.status_code,
            payload=payload,
            content=response.content,
            headers=dict(response.headers),
        )

    def auth_oauth_authorization_url(
        self,
        *,
        anon_key: str,
        provider: AuthOAuthAuthorizeProvider,
        redirect_url: str,
        client_state: str,
    ) -> str:
        request = oauth_authorize_kwargs(
            provider,
            anon_key=anon_key,
            redirect_url=redirect_url,
            client_state=client_state,
            response_mode="code",
        )
        return str(
            httpx.URL(
                f"{self._api_url}{request['url']}",
                params=request["params"],
            )
        )

    def auth_oauth_exchange(
        self,
        *,
        authorization: str,
        code: str,
        redirect_url: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = auth_o_auth_exchange.sync_detailed(
                client=client,
                body=AuthOAuthExchangeBody(code=code, redirect_url=redirect_url),
            )
        return parsed_response(response)

    def auth_link_oauth_provider(
        self,
        *,
        authorization: str,
        provider: AuthLinkOAuthProviderProvider,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = generated_request(client, link_oauth_provider_kwargs(provider))
        if response.status_code != HTTP_OK:
            return unparsed_response(response)
        try:
            payload = AuthLinkOAuthProviderResponse200.from_dict(json_object(response))
        except (
            AttributeError,
            KeyError,
            TypeError,
            UnicodeDecodeError,
            ValueError,
        ) as error:
            raise VolcanoError(MALFORMED_OAUTH_LINK) from error
        return GeneratedTransportResponse(
            status_code=response.status_code,
            payload=payload,
            content=response.content,
            headers=dict(response.headers),
        )

    def auth_unlink_oauth_provider(
        self,
        *,
        authorization: str,
        provider: AuthUnlinkOAuthProviderProvider,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = generated_request(client, unlink_oauth_provider_kwargs(provider))
        return unparsed_response(response)

    def auth_get_oauth_provider_token(
        self,
        *,
        authorization: str,
        provider: GetOAuthProviderTokenProvider,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = generated_request(
                client, get_oauth_provider_token_kwargs(provider)
            )
        if response.status_code != HTTP_OK:
            return unparsed_response(response)
        try:
            payload = GetOAuthProviderTokenResponse200.from_dict(json_object(response))
        except (
            AttributeError,
            KeyError,
            TypeError,
            UnicodeDecodeError,
            ValueError,
        ) as error:
            raise VolcanoError(MALFORMED_OAUTH_STATUS) from error
        return GeneratedTransportResponse(
            status_code=response.status_code,
            payload=payload,
            content=response.content,
            headers=dict(response.headers),
        )

    def auth_refresh_oauth_provider_token(
        self,
        *,
        authorization: str,
        provider: RefreshOAuthProviderTokenProvider,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = generated_request(
                client, refresh_oauth_provider_token_kwargs(provider)
            )
        if response.status_code != HTTP_OK:
            return unparsed_response(response)
        try:
            payload = RefreshOAuthProviderTokenResponse200.from_dict(
                json_object(response)
            )
        except (
            AttributeError,
            KeyError,
            TypeError,
            UnicodeDecodeError,
            ValueError,
        ) as error:
            raise VolcanoError(MALFORMED_OAUTH_STATUS) from error
        return GeneratedTransportResponse(
            status_code=response.status_code,
            payload=payload,
            content=response.content,
            headers=dict(response.headers),
        )

    def auth_call_oauth_api(
        self,
        *,
        authorization: str,
        provider: CallOAuthProviderAPIProvider,
        endpoint: str,
        method: str,
        body: Mapping[str, JSONValue] | None,
    ) -> TransportResponse:
        request_values: dict[str, object] = {"endpoint": endpoint, "method": method}
        if body is not None:
            request_values["body"] = plain_json(body)
        request_body = CallOAuthProviderAPIBody.from_dict(request_values)
        with self._client(authorization) as client:
            response = generated_request(
                client, call_oauth_provider_api_kwargs(provider, body=request_body)
            )
        if response.status_code != HTTP_OK:
            return unparsed_response(response)
        try:
            payload = CallOAuthProviderAPIResponse200.from_dict(json_object(response))
        except (
            AttributeError,
            KeyError,
            TypeError,
            UnicodeDecodeError,
            ValueError,
        ) as error:
            raise VolcanoError(MALFORMED_OAUTH_API_RESPONSE) from error
        return GeneratedTransportResponse(
            status_code=response.status_code,
            payload=payload,
            content=response.content,
            headers=dict(response.headers),
        )
