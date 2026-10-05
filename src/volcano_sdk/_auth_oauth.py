"""Hosted authentication and OAuth provider operations."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Literal
from urllib.parse import quote, urlencode

from ._auth_base import AuthBase
from ._auth_values import (
    HOSTED_AUTH_ACTIONS,
    INVALID_AUTH_TRANSPORT,
    NO_ACTIVE_SESSION,
    PATH_SEGMENT_SAFE,
    UNSUPPORTED_HOSTED_AUTH_ACTION,
    copy_complete_session,
    hosted_auth_parameter,
    linked_oauth_providers_from_payload,
    oauth_api_data_from_payload,
    oauth_api_method,
    oauth_link_from_payload,
    oauth_parameter,
    oauth_provider_name,
    oauth_provider_token_status_from_payload,
    oauth_state,
    session_from_payload,
    validate_hosted_auth_callback_state,
    validate_oauth_callback_state,
)
from ._transport import (
    AuthCallOAuthAPITransport,
    AuthGetOAuthProviderTokenTransport,
    AuthLinkOAuthProviderTransport,
    AuthListOAuthProvidersTransport,
    AuthOAuthAuthorizationURLTransport,
    AuthOAuthExchangeTransport,
    AuthRefreshOAuthProviderTokenTransport,
    AuthUnlinkOAuthProviderTransport,
    invoke,
    response_payload,
)
from .errors import (
    AuthenticationError,
    SessionChangedError,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

    from .models import (
        JSONValue,
        LinkedOAuthProvider,
        OAuthProviderName,
        OAuthProviderTokenStatus,
        Session,
    )


class OAuthAuth(AuthBase):
    """Hosted authentication and OAuth provider operations."""

    def list_linked_oauth_providers(self) -> tuple[LinkedOAuthProvider, ...]:
        """List OAuth providers linked to the current account.

        Returns:
            An immutable tuple of linked provider records.

        Raises:
            AuthenticationError: There is no active session.
            TypeError: The transport does not support this authentication operation.

        """
        binding = self._client.capture_session_binding()
        if binding[2] is None:
            raise AuthenticationError(NO_ACTIVE_SESSION)
        transport = self._client.transport()
        if not isinstance(transport, AuthListOAuthProvidersTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        response = self._requests.request(
            lambda access_token: invoke(
                transport.auth_list_oauth_providers,
                authorization=access_token,
            ),
            binding=binding,
        )
        result = linked_oauth_providers_from_payload(response_payload(response, 200))
        _ = self._requests.owned_session(binding)
        return result

    def get_hosted_auth_url(
        self,
        *,
        project_id: str,
        state: str,
        action: Literal["login", "signup", "forgot-password"] = "login",
    ) -> str:
        """Build a managed hosted-auth URL without navigating or persisting state.

        Returns:
            The hosted-auth URL containing the action and caller state.

        Raises:
            ValueError: A parameter is empty or the action is unsupported.

        """
        project = hosted_auth_parameter(project_id).strip()
        auth_state = hosted_auth_parameter(state)
        if action not in HOSTED_AUTH_ACTIONS:
            raise ValueError(UNSUPPORTED_HOSTED_AUTH_ACTION)
        query = urlencode(
            {
                "action": action,
                "anon_key": self._client.anon_token(),
                "state": auth_state,
            }
        )
        project_path = quote(project, safe=PATH_SEGMENT_SAFE)
        return (
            f"{self._client.api_base_url()}/projects/{project_path}/auth/hosted?{query}"
        )

    def adopt_hosted_auth_session(
        self,
        session: Session,
        *,
        state: str,
        expected_state: str,
    ) -> Session:
        """Validate returned hosted-auth state before storing its session.

        Returns:
            The copied session stored after validating callback state.

        """
        validate_hosted_auth_callback_state(state, expected_state)
        owned = copy_complete_session(session)
        self._client.set_session(owned, event="SIGNED_IN")
        return owned

    def sign_in_with_oauth(
        self,
        *,
        provider: OAuthProviderName,
        redirect_to: str,
        state: str,
    ) -> str:
        """Return the URL that starts an OAuth sign-in flow.

        Returns:
            The provider authorization URL containing the caller state.

        Raises:
            TypeError: The transport cannot start an OAuth sign-in flow.

        """
        provider_name = oauth_provider_name(provider)
        transport = self._client.transport()
        if not isinstance(transport, AuthOAuthAuthorizationURLTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        return transport.auth_oauth_authorization_url(
            anon_key=self._client.anon_token(),
            provider=provider_name,
            redirect_url=oauth_parameter(redirect_to),
            client_state=oauth_state(state),
        )

    def exchange_oauth_code(
        self,
        *,
        code: str,
        redirect_to: str,
        state: str,
        expected_state: str,
    ) -> Session:
        """Validate callback state, exchange a code, and store the session.

        Returns:
            The exchanged session stored by the client.

        Raises:
            SessionChangedError: The local session changed during the exchange.
            TypeError: The transport does not support this authentication operation.

        """
        validate_oauth_callback_state(state, expected_state)
        generation, _ = self._client.capture_session()
        transport = self._client.transport()
        if not isinstance(transport, AuthOAuthExchangeTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        response = invoke(
            transport.auth_oauth_exchange,
            authorization=self._client.anon_token(),
            code=oauth_parameter(code),
            redirect_url=oauth_parameter(redirect_to),
        )
        session = session_from_payload(response_payload(response, 200))
        if not self._client.set_session_if_current(
            session, generation, event="SIGNED_IN"
        ):
            raise SessionChangedError
        return session

    def link_oauth_provider(self, *, provider: OAuthProviderName) -> str:
        """Return the authorization URL for linking an OAuth provider.

        Returns:
            The authorization URL for linking the requested provider.

        Raises:
            AuthenticationError: There is no active session.
            TypeError: The transport does not support this authentication operation.

        """
        provider_name = oauth_provider_name(provider)
        binding = self._client.capture_session_binding()
        if binding[2] is None:
            raise AuthenticationError(NO_ACTIVE_SESSION)
        transport = self._client.transport()
        if not isinstance(transport, AuthLinkOAuthProviderTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        response = self._requests.request(
            lambda access_token: invoke(
                transport.auth_link_oauth_provider,
                authorization=access_token,
                provider=provider_name,
            ),
            binding=binding,
        )
        result = oauth_link_from_payload(response_payload(response, 200))
        _ = self._requests.owned_session(binding)
        return result

    def unlink_oauth_provider(self, *, provider: OAuthProviderName) -> None:
        """Unlink an OAuth provider from the current account.

        Raises:
            AuthenticationError: There is no active session.
            TypeError: The transport cannot unlink an OAuth provider.

        """
        provider_name = oauth_provider_name(provider)
        binding = self._client.capture_session_binding()
        if binding[2] is None:
            raise AuthenticationError(NO_ACTIVE_SESSION)
        transport = self._client.transport()
        if not isinstance(transport, AuthUnlinkOAuthProviderTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        response = self._requests.request(
            lambda access_token: invoke(
                transport.auth_unlink_oauth_provider,
                authorization=access_token,
                provider=provider_name,
            ),
            binding=binding,
        )
        _ = response_payload(response, 204)
        _ = self._requests.owned_session(binding)

    def get_oauth_provider_token(
        self,
        *,
        provider: OAuthProviderName,
    ) -> OAuthProviderTokenStatus:
        """Return validity metadata for a server-held OAuth provider token.

        Returns:
            Validity metadata without exposing the provider token.

        Raises:
            AuthenticationError: There is no active session.
            TypeError: The transport cannot read OAuth provider token status.

        """
        provider_name = oauth_provider_name(provider)
        binding = self._client.capture_session_binding()
        if binding[2] is None:
            raise AuthenticationError(NO_ACTIVE_SESSION)
        transport = self._client.transport()
        if not isinstance(transport, AuthGetOAuthProviderTokenTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        response = self._requests.request(
            lambda access_token: invoke(
                transport.auth_get_oauth_provider_token,
                authorization=access_token,
                provider=provider_name,
            ),
            binding=binding,
        )
        result = oauth_provider_token_status_from_payload(
            response_payload(response, 200)
        )
        _ = self._requests.owned_session(binding)
        return result

    def refresh_oauth_provider_token(
        self,
        *,
        provider: OAuthProviderName,
    ) -> OAuthProviderTokenStatus:
        """Refresh a server-held OAuth provider token and return its status.

        Returns:
            Validity metadata for the refreshed provider token.

        Raises:
            AuthenticationError: There is no active session.
            TypeError: The transport cannot refresh an OAuth provider token.

        """
        provider_name = oauth_provider_name(provider)
        binding = self._client.capture_session_binding()
        if binding[2] is None:
            raise AuthenticationError(NO_ACTIVE_SESSION)
        transport = self._client.transport()
        if not isinstance(transport, AuthRefreshOAuthProviderTokenTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        response = self._requests.request(
            lambda access_token: invoke(
                transport.auth_refresh_oauth_provider_token,
                authorization=access_token,
                provider=provider_name,
            ),
            binding=binding,
        )
        result = oauth_provider_token_status_from_payload(
            response_payload(response, 200)
        )
        _ = self._requests.owned_session(binding)
        return result

    def call_oauth_api(
        self,
        *,
        provider: OAuthProviderName,
        endpoint: str,
        method: Literal["GET", "POST"] = "GET",
        body: Mapping[str, JSONValue] | None = None,
    ) -> JSONValue:
        """Call a provider API through Volcano's fixed-host server proxy.

        Returns:
            The provider response as an immutable JSON value.

        Raises:
            AuthenticationError: There is no active session.
            TypeError: The transport does not support this authentication operation.

        """
        provider_name = oauth_provider_name(provider)
        request_method = oauth_api_method(method)
        binding = self._client.capture_session_binding()
        if binding[2] is None:
            raise AuthenticationError(NO_ACTIVE_SESSION)
        transport = self._client.transport()
        if not isinstance(transport, AuthCallOAuthAPITransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        request_body = deepcopy(dict(body)) if body is not None else None
        response = self._requests.request(
            lambda access_token: invoke(
                transport.auth_call_oauth_api,
                authorization=access_token,
                provider=provider_name,
                endpoint=endpoint,
                method=request_method,
                body=request_body,
            ),
            binding=binding,
        )
        result = oauth_api_data_from_payload(response_payload(response, 200))
        _ = self._requests.owned_session(binding)
        return result
