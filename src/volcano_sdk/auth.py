"""Authentication facade."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from typing import TYPE_CHECKING

from ._auth_context import AuthContext
from ._auth_email import EmailAuth
from ._auth_oauth import OAuthAuth
from ._auth_values import (
    INVALID_AUTH_CALLBACK,
    INVALID_AUTH_TRANSPORT,
    NO_ACTIVE_SESSION,
    copy_complete_session,
    session_from_payload,
    session_page_from_payload,
    sign_up_result_from_payload,
)
from ._callbacks import require_callable
from ._session import (
    session_id_from_access_token,
)
from ._transport import (
    AuthConvertAnonymousTransport,
    AuthDeleteAllMySessionsTransport,
    AuthDeleteMySessionTransport,
    AuthGetMySessionsTransport,
    AuthGetUserTransport,
    AuthSignUpAnonymousTransport,
    AuthSignUpTransport,
    AuthUpdateUserTransport,
    invoke,
    response_payload,
)
from .errors import (
    AuthenticationError,
    SessionChangedError,
    TransportError,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

    from ._session_operations import SessionOperations
    from .models import (
        AuthStateCallback,
        AuthSubscription,
        Session,
        SessionPage,
        SignUpResult,
        User,
    )


__all__ = ["Auth", "AuthContext"]


class Auth(EmailAuth, OAuthAuth):
    """Authenticate users and update the client session."""

    def get_session(self) -> Session | None:
        """Return the immutable locally held session without validating it.

        Returns:
            The immutable local session, or None when signed out.

        """
        return self._client.current_session()

    def on_auth_state_change(
        self,
        callback: AuthStateCallback,
    ) -> AuthSubscription:
        """Queue initial state, then observe changes until cancellation.

        Returns:
            A subscription whose unsubscribe method stops notifications.

        """
        require_callable(callback, INVALID_AUTH_CALLBACK)
        return self._client.subscribe_auth_state_change(callback)

    def set_session(self, session: Session) -> Session:
        """Copy a complete session locally without notifying auth subscribers.

        Returns:
            The copied session stored by the client.

        """
        owned = copy_complete_session(session)
        self._client.set_session(owned, event=None)
        return owned

    def sign_up(
        self,
        *,
        email: str,
        password: str,
        metadata: Mapping[str, object] | None = None,
        sign_in_when_allowed: bool = False,
    ) -> SignUpResult:
        """Sign up, optionally signing in when confirmation is not required.

        Returns:
            The sign-up acknowledgement, including a session if signed in.

        Raises:
            TypeError: The transport does not support this authentication operation.

        """
        generation, _ = self._client.capture_session()
        transport = self._client.transport()
        if not isinstance(transport, AuthSignUpTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        response = invoke(
            transport.auth_signup,
            authorization=self._client.anon_token(),
            email=email,
            password=password,
            metadata=dict(metadata or {}),
        )
        result = sign_up_result_from_payload(response_payload(response, 201))
        if sign_in_when_allowed and not result.confirmation_required:
            session = self._sign_in_for_generation(email, password, generation)
            return replace(result, session=session)
        return result

    def sign_in_anonymously(
        self,
        *,
        metadata: Mapping[str, object] | None = None,
    ) -> Session:
        """Create an anonymous account and store its session.

        Returns:
            The new anonymous session stored by the client.

        Raises:
            SessionChangedError: The local session changed during sign-up.
            TypeError: The transport does not support this authentication operation.

        """
        generation, _ = self._client.capture_session()
        transport = self._client.transport()
        if not isinstance(transport, AuthSignUpAnonymousTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        response = invoke(
            transport.auth_signup_anonymous,
            authorization=self._client.anon_token(),
            metadata=dict(metadata or {}),
        )
        session = session_from_payload(response_payload(response, 201))
        if not self._client.set_session_if_current(
            session, generation, event="SIGNED_IN"
        ):
            raise SessionChangedError
        return session

    def convert_anonymous(
        self,
        *,
        email: str,
        password: str,
        metadata: Mapping[str, object] | None = None,
    ) -> User:
        """Attach email credentials to the current anonymous account.

        Returns:
            The updated profile for the converted account.

        Raises:
            AuthenticationError: There is no active session.
            TypeError: The transport does not support this authentication operation.

        """
        binding = self._client.capture_session_binding()
        if binding[2] is None:
            raise AuthenticationError(NO_ACTIVE_SESSION)
        transport = self._client.transport()
        if not isinstance(transport, AuthConvertAnonymousTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        request_metadata = deepcopy(dict(metadata or {}))
        response = self._requests.request(
            lambda access_token: invoke(
                transport.auth_convert_anonymous,
                authorization=access_token,
                email=email,
                password=password,
                metadata=request_metadata,
            ),
            binding=binding,
        )
        return self._update_current_user(response_payload(response, 200), binding)

    def delete_all_other_sessions(self) -> None:
        """Delete every other session while preserving the current session.

        Raises:
            AuthenticationError: There is no active session.
            TypeError: The transport does not support this authentication operation.

        """
        binding = self._client.capture_session_binding()
        if binding[2] is None:
            raise AuthenticationError(NO_ACTIVE_SESSION)
        transport = self._client.transport()
        if not isinstance(transport, AuthDeleteAllMySessionsTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        response = self._requests.request(
            lambda access_token: invoke(
                transport.auth_delete_all_my_sessions,
                authorization=access_token,
            ),
            binding=binding,
        )
        _ = response_payload(response, 204)
        _ = self._requests.owned_session(binding)

    def list_sessions(self, *, page: int = 1, limit: int = 20) -> SessionPage:
        """List sessions in the stable offset-paginated activity order.

        Returns:
            A page of session records and pagination metadata.

        Raises:
            AuthenticationError: There is no active session.
            TypeError: The transport does not support this authentication operation.

        """
        binding = self._client.capture_session_binding()
        if binding[2] is None:
            raise AuthenticationError(NO_ACTIVE_SESSION)
        transport = self._client.transport()
        if not isinstance(transport, AuthGetMySessionsTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        response = self._requests.request(
            lambda access_token: invoke(
                transport.auth_get_my_sessions,
                authorization=access_token,
                page=page,
                limit=limit,
            ),
            binding=binding,
        )
        result = session_page_from_payload(response_payload(response, 200))
        _ = self._requests.owned_session(binding)
        return result

    def delete_session(self, *, session_id: str) -> None:
        """Delete one session and clear local state when it is current.

        Raises:
            AuthenticationError: There is no active session.
            SessionChangedError: The local session changed during deletion.
            TransportError: The deletion request failed before a usable response.
            TypeError: The transport does not support this authentication operation.

        """
        binding = self._client.capture_session_binding()
        generation, lineage, current = binding
        if current is None:
            raise AuthenticationError(NO_ACTIVE_SESSION)
        current_session_id = session_id_from_access_token(current.access_token)
        deletes_current = (
            current_session_id is not None
            and current_session_id.casefold() == session_id.casefold()
        )
        transport = self._client.transport()
        if not isinstance(transport, AuthDeleteMySessionTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        try:
            response = self._requests.request(
                lambda access_token: invoke(
                    transport.auth_delete_my_session,
                    authorization=access_token,
                    session_id=session_id,
                ),
                binding=binding,
            )
            _ = response_payload(response, 204)
        except TransportError as error:
            if deletes_current and not self._client.clear_session_if_current(
                generation, lineage=lineage, event="SIGNED_OUT"
            ):
                raise SessionChangedError from error
            raise
        self._finish_session_deletion(binding, deletes_current=deletes_current)

    def _finish_session_deletion(
        self,
        binding: tuple[int, SessionOperations, Session | None],
        *,
        deletes_current: bool,
    ) -> None:
        generation, lineage, _ = binding
        if deletes_current:
            if not self._client.clear_session_if_current(
                generation, lineage=lineage, event="SIGNED_OUT"
            ):
                raise SessionChangedError
            return
        _, active_lineage, active_session = self._client.capture_session_binding()
        if active_lineage is not lineage or active_session is None:
            raise SessionChangedError

    def get_user(self) -> User:
        """Load a server-validated profile for the current session.

        Returns:
            The server profile also saved in the current session.

        Raises:
            AuthenticationError: There is no active session.
            TypeError: The transport does not support this authentication operation.

        """
        binding = self._client.capture_session_binding()
        if binding[2] is None:
            raise AuthenticationError(NO_ACTIVE_SESSION)
        transport = self._client.transport()
        if not isinstance(transport, AuthGetUserTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        response = self._requests.request(
            lambda access_token: invoke(
                transport.auth_get_user, authorization=access_token
            ),
            binding=binding,
        )
        return self._update_current_user(response_payload(response, 200), binding)

    def update_user(
        self,
        *,
        password: str | None = None,
        metadata: Mapping[str, object] | None = None,
    ) -> User:
        """Update and return the current user's server-validated profile.

        Returns:
            The updated profile also saved in the current session.

        Raises:
            AuthenticationError: There is no active session.
            TypeError: The transport does not support this authentication operation.

        """
        binding = self._client.capture_session_binding()
        if binding[2] is None:
            raise AuthenticationError(NO_ACTIVE_SESSION)
        transport = self._client.transport()
        if not isinstance(transport, AuthUpdateUserTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        request_metadata = None if metadata is None else deepcopy(dict(metadata))
        response = self._requests.request(
            lambda access_token: invoke(
                transport.auth_update_user,
                authorization=access_token,
                password=password,
                metadata=request_metadata,
            ),
            binding=binding,
        )
        return self._update_current_user(response_payload(response, 200), binding)

    def sign_in(self, *, email: str, password: str) -> Session:
        """Sign in a user and store the returned session.

        Returns:
            The authenticated session stored by the client.

        """
        generation, _ = self._client.capture_session()
        return self._sign_in_for_generation(email, password, generation)

    def _sign_in_for_generation(
        self, email: str, password: str, generation: int
    ) -> Session:
        if self._client.capture_session()[0] != generation:
            raise SessionChangedError
        response = invoke(
            self._client.transport().auth_signin,
            authorization=self._client.anon_token(),
            email=email,
            password=password,
        )
        payload = response_payload(response, 200)
        session = session_from_payload(payload)
        if not self._client.set_session_if_current(
            session, generation, event="SIGNED_IN"
        ):
            raise SessionChangedError
        return session

    def refresh_session(self) -> Session:
        """Refresh and replace the current session.

        Returns:
            The current session after completing or joining its refresh.

        """
        return self._requests.refresh(self._client.capture_session_binding())

    def sign_out(self) -> None:
        """Revoke and clear the current session."""
        self._requests.sign_out()
