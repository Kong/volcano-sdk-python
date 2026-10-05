"""Credential-scoped authentication request coordination."""

from __future__ import annotations

from contextlib import suppress
from http import HTTPStatus
from typing import TYPE_CHECKING

from ._auth_values import (
    INCOMPLETE_SESSION,
    INVALID_AUTH_TRANSPORT,
    NO_ACTIVE_SESSION,
    REFRESH_UNAVAILABLE,
    session_from_payload,
)
from ._session import (
    session_id_from_access_token,
    validate_refresh_identity,
    validate_refresh_source,
)
from ._transport import (
    AuthDeleteMySessionTransport,
    AuthLogoutTransport,
    AuthRefreshTransport,
    invoke,
    response_payload,
)
from .errors import (
    AuthenticationError,
    RateLimitedError,
    SessionChangedError,
    TransportError,
    VolcanoError,
)

if TYPE_CHECKING:
    from collections.abc import Callable
    from concurrent.futures import Future

    from ._auth_context import AuthContext
    from ._session_operations import SessionOperations
    from ._transport import TransportResponse
    from .models import (
        Session,
    )


class AuthRequests:
    """Coordinate requests, refreshes, and sign-out for one client."""

    def __init__(self, client: AuthContext) -> None:
        self._client: AuthContext = client
        self._rejected_refresh: tuple[int, SessionOperations] | None = None

    def request(
        self,
        operation: Callable[[str], TransportResponse],
        *,
        binding: tuple[int, SessionOperations, Session | None] | None = None,
    ) -> TransportResponse:
        if binding is None:
            binding = self._client.capture_session_binding()
        if binding[2] is None:
            raise RuntimeError(NO_ACTIVE_SESSION)
        owned = self.owned_session(binding)
        current = owned[2]
        response = operation(current.access_token)
        if response.status_code != HTTPStatus.UNAUTHORIZED:
            return response
        return self._replay_session_request(operation, owned, response)

    def _replay_session_request(
        self,
        operation: Callable[[str], TransportResponse],
        binding: tuple[int, SessionOperations, Session | None],
        rejected_response: TransportResponse,
    ) -> TransportResponse:
        try:
            _ = self.refresh(binding)
        except SessionChangedError:
            raise
        except VolcanoError:
            self.validate_failure(binding)
            return rejected_response
        session = self.owned_session(binding)[2]
        response = operation(session.access_token)
        _ = self.owned_session(binding)
        return response

    def validate_failure(
        self, binding: tuple[int, SessionOperations, Session | None]
    ) -> None:
        with suppress(AuthenticationError):
            _ = self.owned_session(binding)

    def refresh(
        self, binding: tuple[int, SessionOperations, Session | None]
    ) -> Session:
        generation, owner, current = binding
        if current is None:
            raise AuthenticationError(NO_ACTIVE_SESSION)
        notifications: list[Callable[[], None]] = []
        try:
            active_generation, _, _ = self.owned_session(binding)
            if active_generation == generation:
                _ = owner.refresh(
                    lambda: self._perform_refresh(binding, current, notifications)
                )
            if owner.signing_out is not None:
                raise SessionChangedError
        except VolcanoError:
            self.validate_failure(binding)
            raise
        finally:
            _dispatch_notifications(notifications)
        return self.owned_session(binding)[2]

    def owned_session(
        self, binding: tuple[int, SessionOperations, Session | None]
    ) -> tuple[int, SessionOperations, Session]:
        generation, lineage, _ = binding
        active = self._client.capture_session_binding()
        if (
            self._rejected_refresh == (generation, lineage)
            and active[0] == generation + 1
            and active[2] is None
        ):
            raise AuthenticationError(NO_ACTIVE_SESSION)
        if active[1] != lineage or active[2] is None:
            raise SessionChangedError
        return active[0], active[1], active[2]

    def _perform_refresh(
        self,
        binding: tuple[int, SessionOperations, Session | None],
        current: Session,
        notifications: list[Callable[[], None]],
    ) -> Session:
        generation, owner, _ = binding
        active_generation, _, active = self.owned_session(binding)
        if active_generation != generation:
            return active
        refresh_token = current.refresh_token
        if refresh_token is None:
            raise AuthenticationError(REFRESH_UNAVAILABLE)
        verified = owner.has_verified_pair(current)
        validate_refresh_source(current, verified=verified)
        owner.verify_pair(None)
        refreshed = self._refresh_with_recovery(
            (current, refresh_token), binding, notifications, verified=verified
        )
        validate_refresh_identity(current, refreshed)
        owner.verify_pair(refreshed)
        if owner.signing_out is None:
            _ = self._client.set_session_if_current(
                refreshed,
                generation,
                event="TOKEN_REFRESHED",
                notifications=notifications,
            )
        return refreshed

    def _refresh_with_recovery(
        self,
        credentials: tuple[Session, str],
        binding: tuple[int, SessionOperations, Session | None],
        notifications: list[Callable[[], None]],
        *,
        verified: bool,
    ) -> Session:
        generation, owner, _ = binding
        current, refresh_token = credentials
        try:
            return self._request_refreshed_session(refresh_token)
        except RateLimitedError:
            if verified:
                owner.verify_pair(current)
            raise
        except AuthenticationError:
            if owner.signing_out is None and self._client.clear_session_if_current(
                generation, event="SIGNED_OUT", notifications=notifications
            ):
                self._rejected_refresh = (generation, owner)
            raise

    def _request_refreshed_session(self, refresh_token: str) -> Session:
        transport = self._client.transport()
        if not isinstance(transport, AuthRefreshTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        try:
            response = invoke(
                transport.auth_refresh,
                authorization=self._client.anon_token(),
                refresh_token=refresh_token,
            )
            return session_from_payload(response_payload(response, 200))
        except (KeyError, TypeError, ValueError) as error:
            raise TransportError(INCOMPLETE_SESSION) from error

    def sign_out(self) -> None:
        """Revoke and clear the current session."""
        binding = self._client.capture_session_binding()
        if binding[2] is None:
            binding[1].wait_for_sign_out()
            return
        notifications: list[Callable[[], None]] = []
        try:
            binding[1].sign_out(
                lambda preceding, pending: self._sign_out_captured(
                    binding, preceding, notifications, pending=pending
                )
            )
        finally:
            _dispatch_notifications(notifications)

    def _sign_out_captured(
        self,
        binding: tuple[int, SessionOperations, Session | None],
        preceding: Future[Session] | None,
        notifications: list[Callable[[], None]],
        *,
        pending: bool,
    ) -> None:
        generation, owner, current = binding
        current, refresh_error = _preceding_session(current, preceding)
        if current is None:
            return
        error: VolcanoError | None = None
        try:
            self._revoke_session(
                current, owner, refresh_error if pending else None, joined=pending
            )
        except VolcanoError as caught:
            error = caught
        if not self._client.clear_session_if_current(
            generation, lineage=owner, event="SIGNED_OUT", notifications=notifications
        ):
            raise SessionChangedError from error
        if error is not None:
            raise error

    def _revoke_session(
        self,
        session: Session,
        owner: SessionOperations,
        refresh_error: VolcanoError | None,
        *,
        joined: bool,
    ) -> None:
        session_id = session_id_from_access_token(session.access_token)
        verified = owner.has_verified_pair(session)
        if session_id is not None and not verified:
            self._revoke_access_session(
                session, session_id, refresh_error, joined=joined
            )
            return
        if refresh_error is not None and not verified:
            raise refresh_error
        if session.refresh_token is not None:
            transport = self._client.transport()
            if not isinstance(transport, AuthLogoutTransport):
                raise TypeError(INVALID_AUTH_TRANSPORT)
            response = invoke(
                transport.auth_logout,
                authorization=self._client.anon_token(),
                refresh_token=session.refresh_token,
            )
        else:
            return
        _ = response_payload(response, 204)

    def _revoke_access_session(
        self,
        session: Session,
        session_id: str,
        refresh_error: VolcanoError | None,
        *,
        joined: bool,
    ) -> None:
        transport = self._client.transport()
        if not isinstance(transport, AuthDeleteMySessionTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        response = invoke(
            transport.auth_delete_my_session,
            authorization=session.access_token,
            session_id=session_id,
        )
        if (
            response.status_code == HTTPStatus.UNAUTHORIZED
            and session.refresh_token is not None
        ):
            if refresh_error is not None:
                raise refresh_error
            if not joined:
                refreshed = self._request_refreshed_session(session.refresh_token)
                validate_refresh_identity(session, refreshed)
                response = invoke(
                    transport.auth_delete_my_session,
                    authorization=refreshed.access_token,
                    session_id=session_id,
                )
        _ = response_payload(response, 204)


def _dispatch_notifications(notifications: list[Callable[[], None]]) -> None:
    for dispatch in notifications:
        dispatch()


def _preceding_session(
    current: Session | None, preceding: Future[Session] | None
) -> tuple[Session | None, VolcanoError | None]:
    if preceding is None:
        return current, None
    try:
        return preceding.result(), None
    except VolcanoError as caught:
        return current, caught
