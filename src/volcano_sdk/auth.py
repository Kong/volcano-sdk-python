"""Authentication facade."""

from __future__ import annotations

import base64
import binascii
import json
from collections.abc import Mapping
from datetime import datetime
from typing import TYPE_CHECKING, Protocol, TypeVar, cast

from ._generated.models.auth_confirm_email_change_response_200 import (
    AuthConfirmEmailChangeResponse200,
)
from ._generated.models.auth_convert_anonymous_response_200 import (
    AuthConvertAnonymousResponse200,
)
from ._generated.models.auth_get_my_sessions_response_200 import (
    AuthGetMySessionsResponse200,
)
from ._generated.models.auth_get_user_response_200 import AuthGetUserResponse200
from ._generated.models.auth_link_o_auth_provider_response_200 import (
    AuthLinkOAuthProviderResponse200,
)
from ._generated.models.auth_list_o_auth_providers_response_200 import (
    AuthListOAuthProvidersResponse200,
)
from ._generated.models.auth_update_user_response_200 import AuthUpdateUserResponse200
from ._generated.types import Unset
from ._transport import (
    AuthCancelEmailChangeTransport,
    AuthConfirmEmailChangeTransport,
    AuthConfirmEmailTransport,
    AuthConvertAnonymousTransport,
    AuthDeleteAllMySessionsTransport,
    AuthDeleteMySessionTransport,
    AuthForgotPasswordTransport,
    AuthGetMySessionsTransport,
    AuthGetUserTransport,
    AuthLinkOAuthProviderTransport,
    AuthListOAuthProvidersTransport,
    AuthLogoutTransport,
    AuthRefreshTransport,
    AuthRequestEmailChangeTransport,
    AuthResendConfirmationTransport,
    AuthResetPasswordTransport,
    AuthSignUpAnonymousTransport,
    AuthSignUpTransport,
    AuthUpdateUserTransport,
    Transport,
    invoke,
    response_payload,
)
from .errors import (
    AuthenticationError,
    SessionChangedError,
    TransportError,
    VolcanoError,
)
from .models import (
    AuthSession,
    EmailChangeResult,
    JSONValue,
    LinkedOAuthProvider,
    OAuthProviderName,
    Session,
    SessionPage,
    SignUpResult,
    User,
)

_INCOMPLETE_SESSION = "Expected a complete Session"
_INVALID_SIGN_UP_RESULT = "Expected a complete sign-up acknowledgement"
_INVALID_EMAIL_CHANGE_RESULT = "Expected a valid email-change acknowledgement"
_INVALID_USER = "Expected a complete user profile"
_INVALID_SESSION_PAGE = "Expected a complete session page"
_INVALID_LINKED_OAUTH_PROVIDERS = "Expected complete linked OAuth providers"
_INVALID_OAUTH_LINK = "Expected an OAuth authorization URL"
_UNSUPPORTED_OAUTH_PROVIDER = "Unsupported OAuth provider"
_JWT_PARTS = 3
_NO_ACTIVE_SESSION = "No active session"
_T = TypeVar("_T")
_OAUTH_PROVIDERS: frozenset[str] = frozenset({"apple", "github", "google", "microsoft"})

if TYPE_CHECKING:
    from ._generated.models import (
        AuthListOAuthProvidersResponse200ProvidersItem,
    )
    from ._generated.models.auth_session import AuthSession as GeneratedAuthSession


def _is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _session_id_from_access_token(access_token: str) -> str | None:
    parts = access_token.split(".")
    if len(parts) != _JWT_PARTS:
        return None
    padding = "=" * (-len(parts[1]) % 4)
    try:
        payload: object = json.loads(
            base64.urlsafe_b64decode(parts[1] + padding).decode()
        )
    except (binascii.Error, json.JSONDecodeError, UnicodeDecodeError):
        return None
    if not isinstance(payload, Mapping):
        return None
    values = cast("Mapping[object, object]", payload)
    session_id = values.get("session_id")
    if not isinstance(session_id, str) or not session_id.strip():
        return None
    return session_id.strip()


def _has_complete_values(session: Session) -> bool:
    return all(
        _is_non_empty_string(value)
        for value in (
            session.access_token,
            session.refresh_token,
            session.user_id,
        )
    )


def _copy_complete_session(session: object) -> Session:
    if not isinstance(session, Session) or not _has_complete_values(session):
        raise ValueError(_INCOMPLETE_SESSION)
    return Session(
        access_token=session.access_token,
        refresh_token=session.refresh_token,
        user_id=session.user_id,
    )


def _session_from_payload(payload: object) -> Session:
    values: Mapping[object, object] = (
        cast("Mapping[object, object]", payload) if isinstance(payload, Mapping) else {}
    )
    raw_user = values.get("user")
    user: Mapping[object, object] = (
        cast("Mapping[object, object]", raw_user)
        if isinstance(raw_user, Mapping)
        else {}
    )
    return _copy_complete_session(
        Session(
            access_token=cast("str", values.get("access_token")),
            refresh_token=cast("str", values.get("refresh_token")),
            user_id=cast("str", user.get("id")),
        )
    )


def _sign_up_result_from_payload(payload: object) -> SignUpResult:
    values: Mapping[object, object] = (
        cast("Mapping[object, object]", payload) if isinstance(payload, Mapping) else {}
    )
    confirmation_required = values.get("confirmation_required")
    message = values.get("message")
    if not isinstance(confirmation_required, bool) or not isinstance(message, str):
        raise TypeError(_INVALID_SIGN_UP_RESULT)
    return SignUpResult(
        confirmation_required=confirmation_required,
        message=message,
    )


def _email_change_result_from_payload(payload: object) -> EmailChangeResult:
    if not isinstance(payload, Mapping):
        raise TypeError(_INVALID_EMAIL_CHANGE_RESULT)
    values = cast("Mapping[object, object]", payload)
    message = values.get("message")
    new_email = values.get("new_email")
    if not all(
        value is None or isinstance(value, str) for value in (message, new_email)
    ):
        raise TypeError(_INVALID_EMAIL_CHANGE_RESULT)
    return EmailChangeResult(
        message=cast("str | None", message),
        new_email=cast("str | None", new_email),
    )


def _user_from_payload(payload: object) -> User:
    if not isinstance(
        payload,
        (
            AuthConvertAnonymousResponse200,
            AuthConfirmEmailChangeResponse200,
            AuthGetUserResponse200,
            AuthUpdateUserResponse200,
        ),
    ) or isinstance(payload.user, Unset):
        raise AuthenticationError(_INVALID_USER)
    user = payload.user
    project_id = _none_if_unset(user.project_id)
    user_metadata = _none_if_unset(user.user_metadata)
    app_metadata = _none_if_unset(user.app_metadata)
    return User(
        id=str(user.id),
        email=user.email,
        status=user.status,
        project_id=None if project_id is None else str(project_id),
        email_confirmed=_none_if_unset(user.email_confirmed),
        user_metadata=(
            None
            if user_metadata is None
            else cast("Mapping[str, JSONValue]", user_metadata.to_dict())
        ),
        app_metadata=(
            None
            if app_metadata is None
            else cast("Mapping[str, JSONValue]", app_metadata.to_dict())
        ),
        avatar_url=_none_if_unset(user.avatar_url),
        banned_until=_none_if_unset(user.banned_until),
        last_sign_in_at=_none_if_unset(user.last_sign_in_at),
        created_at=_none_if_unset(user.created_at),
        updated_at=_none_if_unset(user.updated_at),
    )


def _none_if_unset(value: _T | Unset) -> _T | None:
    return None if isinstance(value, Unset) else value


def _auth_session_from_model(session: GeneratedAuthSession) -> AuthSession:
    return AuthSession(
        id=str(session.id),
        user_id=str(session.user_id),
        provider=session.provider,
        expires_at=session.expires_at,
        is_active=_session_bool(session.is_active),
        is_current=_session_bool(session.is_current),
        user_agent=_optional_session_string(session.user_agent),
        ip_address=_optional_session_string(session.ip_address),
        last_ip_address=_optional_session_string(session.last_ip_address),
        last_activity_at=_none_if_unset(session.last_activity_at),
        session_started_at=_none_if_unset(session.session_started_at),
        created_at=_none_if_unset(session.created_at),
        updated_at=_none_if_unset(session.updated_at),
    )


def _session_bool(value: object) -> bool:
    if not isinstance(value, bool):
        raise VolcanoError(_INVALID_SESSION_PAGE)
    return value


def _optional_session_string(value: object) -> str | None:
    if isinstance(value, Unset) or value is None:
        return None
    if not isinstance(value, str):
        raise VolcanoError(_INVALID_SESSION_PAGE)
    return value


def _session_page_from_payload(payload: object) -> SessionPage:
    if not isinstance(payload, AuthGetMySessionsResponse200):
        raise VolcanoError(_INVALID_SESSION_PAGE)
    pagination = (
        payload.total,
        payload.page,
        payload.limit,
        payload.total_pages,
    )
    if isinstance(payload.sessions, Unset) or any(
        type(value) is not int for value in pagination
    ):
        raise VolcanoError(_INVALID_SESSION_PAGE)
    return SessionPage(
        sessions=tuple(
            _auth_session_from_model(session) for session in payload.sessions
        ),
        total=cast("int", payload.total),
        page=cast("int", payload.page),
        limit=cast("int", payload.limit),
        total_pages=cast("int", payload.total_pages),
    )


def _linked_oauth_provider_from_model(
    item: AuthListOAuthProvidersResponse200ProvidersItem,
) -> LinkedOAuthProvider:
    try:
        provider = _oauth_provider_name(item.provider)
    except ValueError as error:
        raise VolcanoError(_INVALID_LINKED_OAUTH_PROVIDERS) from error
    return LinkedOAuthProvider(
        provider=provider,
        linked_at=_linked_oauth_datetime(item.linked_at),
        updated_at=_linked_oauth_datetime(item.updated_at),
    )


def _linked_oauth_datetime(value: object) -> datetime:
    if not isinstance(value, datetime):
        raise VolcanoError(_INVALID_LINKED_OAUTH_PROVIDERS)
    return value


def _linked_oauth_providers_from_payload(
    payload: object,
) -> tuple[LinkedOAuthProvider, ...]:
    if not isinstance(payload, AuthListOAuthProvidersResponse200) or isinstance(
        payload.providers, Unset
    ):
        raise VolcanoError(_INVALID_LINKED_OAUTH_PROVIDERS)
    return tuple(
        _linked_oauth_provider_from_model(provider) for provider in payload.providers
    )


def _oauth_provider_name(value: object) -> OAuthProviderName:
    if not isinstance(value, str) or value not in _OAUTH_PROVIDERS:
        raise ValueError(_UNSUPPORTED_OAUTH_PROVIDER)
    return cast("OAuthProviderName", value)


def _oauth_link_from_payload(payload: object) -> str:
    if not isinstance(payload, AuthLinkOAuthProviderResponse200):
        raise VolcanoError(_INVALID_OAUTH_LINK)
    authorization_url = payload.authorization_url
    if not isinstance(authorization_url, str) or not authorization_url.strip():
        raise VolcanoError(_INVALID_OAUTH_LINK)
    return authorization_url


class AuthContext(Protocol):
    """Client capabilities required by the authentication facade."""

    _transport: Transport

    @property
    def current_session(self) -> Session | None:
        """Return the locally held session, if one exists."""
        ...

    def _anon_token(self) -> str: ...

    def _set_session(self, session: Session) -> None: ...

    def _capture_session(self) -> tuple[int, Session | None]: ...

    def _set_session_if_current(self, session: Session, generation: int) -> bool: ...

    def _clear_session_if_current(self, generation: int) -> bool: ...


class Auth:
    """Authenticate users and update the client session."""

    def __init__(self, client: AuthContext) -> None:
        """Create an authentication facade backed by a client."""
        self._client = client

    def get_session(self) -> Session | None:
        """Return the immutable locally held session without validating it."""
        return self._client.current_session

    def set_session(self, session: Session) -> Session:
        """Copy a complete session into local client state."""
        owned = _copy_complete_session(session)
        self._client._set_session(owned)
        return owned

    def sign_up(
        self,
        *,
        email: str,
        password: str,
        metadata: Mapping[str, object] | None = None,
    ) -> SignUpResult:
        """Create an account without creating or replacing a local session."""
        transport = cast("AuthSignUpTransport", self._client._transport)
        response = invoke(
            transport.auth_signup,
            authorization=self._client._anon_token(),
            email=email,
            password=password,
            metadata=dict(metadata or {}),
        )
        return _sign_up_result_from_payload(response_payload(response, 201))

    def sign_in_anonymously(
        self,
        *,
        metadata: Mapping[str, object] | None = None,
    ) -> Session:
        """Create an anonymous account and store its session."""
        generation, _ = self._client._capture_session()
        transport = cast("AuthSignUpAnonymousTransport", self._client._transport)
        response = invoke(
            transport.auth_signup_anonymous,
            authorization=self._client._anon_token(),
            metadata=dict(metadata or {}),
        )
        session = _session_from_payload(response_payload(response, 201))
        if not self._client._set_session_if_current(session, generation):
            raise SessionChangedError
        return session

    def convert_anonymous(
        self,
        *,
        email: str,
        password: str,
        metadata: Mapping[str, object] | None = None,
    ) -> User:
        """Attach email credentials to the current anonymous account."""
        generation, current = self._client._capture_session()
        if current is None:
            raise AuthenticationError(_NO_ACTIVE_SESSION)
        transport = cast("AuthConvertAnonymousTransport", self._client._transport)
        response = invoke(
            transport.auth_convert_anonymous,
            authorization=current.access_token,
            email=email,
            password=password,
            metadata=dict(metadata or {}),
        )
        user = _user_from_payload(response_payload(response, 200))
        if self._client._capture_session()[0] != generation:
            raise SessionChangedError
        return user

    def reset_password_for_email(self, *, email: str) -> None:
        """Request a reset email without revealing whether the account exists."""
        transport = cast("AuthForgotPasswordTransport", self._client._transport)
        response = invoke(
            transport.auth_forgot_password,
            authorization=self._client._anon_token(),
            email=email,
        )
        response_payload(response, 200)

    def request_email_change(self, *, new_email: str) -> EmailChangeResult:
        """Request a confirmation email without changing the current session."""
        generation, current = self._client._capture_session()
        if current is None:
            raise AuthenticationError(_NO_ACTIVE_SESSION)
        transport = cast("AuthRequestEmailChangeTransport", self._client._transport)
        response = invoke(
            transport.auth_request_email_change,
            authorization=current.access_token,
            new_email=new_email,
        )
        result = _email_change_result_from_payload(response_payload(response, 200))
        if self._client._capture_session()[0] != generation:
            raise SessionChangedError
        return result

    def cancel_email_change(self) -> None:
        """Cancel a pending email change without changing the current session."""
        generation, current = self._client._capture_session()
        if current is None:
            raise AuthenticationError(_NO_ACTIVE_SESSION)
        transport = cast("AuthCancelEmailChangeTransport", self._client._transport)
        response = invoke(
            transport.auth_cancel_email_change,
            authorization=current.access_token,
        )
        response_payload(response, 200)
        if self._client._capture_session()[0] != generation:
            raise SessionChangedError

    def confirm_email_change(self, *, token: str) -> User:
        """Confirm a pending email change and return the updated user."""
        generation, current = self._client._capture_session()
        if current is None:
            raise AuthenticationError(_NO_ACTIVE_SESSION)
        transport = cast("AuthConfirmEmailChangeTransport", self._client._transport)
        response = invoke(
            transport.auth_confirm_email_change,
            authorization=current.access_token,
            token=token,
        )
        user = _user_from_payload(response_payload(response, 200))
        if self._client._capture_session()[0] != generation:
            raise SessionChangedError
        return user

    def delete_all_other_sessions(self) -> None:
        """Delete every other session while preserving the current session."""
        generation, current = self._client._capture_session()
        if current is None:
            raise AuthenticationError(_NO_ACTIVE_SESSION)
        transport = cast("AuthDeleteAllMySessionsTransport", self._client._transport)
        response = invoke(
            transport.auth_delete_all_my_sessions,
            authorization=current.access_token,
        )
        response_payload(response, 204)
        if self._client._capture_session()[0] != generation:
            raise SessionChangedError

    def list_sessions(self, *, page: int = 1, limit: int = 20) -> SessionPage:
        """List sessions in the stable offset-paginated activity order."""
        generation, current = self._client._capture_session()
        if current is None:
            raise AuthenticationError(_NO_ACTIVE_SESSION)
        transport = cast("AuthGetMySessionsTransport", self._client._transport)
        response = invoke(
            transport.auth_get_my_sessions,
            authorization=current.access_token,
            page=page,
            limit=limit,
        )
        result = _session_page_from_payload(response_payload(response, 200))
        if self._client._capture_session()[0] != generation:
            raise SessionChangedError
        return result

    def list_linked_oauth_providers(self) -> tuple[LinkedOAuthProvider, ...]:
        """List OAuth providers linked to the current account."""
        generation, current = self._client._capture_session()
        if current is None:
            raise AuthenticationError(_NO_ACTIVE_SESSION)
        transport = cast("AuthListOAuthProvidersTransport", self._client._transport)
        response = invoke(
            transport.auth_list_oauth_providers,
            authorization=current.access_token,
        )
        result = _linked_oauth_providers_from_payload(response_payload(response, 200))
        if self._client._capture_session()[0] != generation:
            raise SessionChangedError
        return result

    def link_oauth_provider(self, *, provider: OAuthProviderName) -> str:
        """Return the authorization URL for linking an OAuth provider."""
        provider_name = _oauth_provider_name(provider)
        generation, current = self._client._capture_session()
        if current is None:
            raise AuthenticationError(_NO_ACTIVE_SESSION)
        transport = cast("AuthLinkOAuthProviderTransport", self._client._transport)
        response = invoke(
            transport.auth_link_oauth_provider,
            authorization=current.access_token,
            provider=provider_name,
        )
        result = _oauth_link_from_payload(response_payload(response, 200))
        if self._client._capture_session()[0] != generation:
            raise SessionChangedError
        return result

    def delete_session(self, *, session_id: str) -> None:
        """Delete one session and clear local state when it is current."""
        generation, current = self._client._capture_session()
        if current is None:
            raise AuthenticationError(_NO_ACTIVE_SESSION)
        current_session_id = _session_id_from_access_token(current.access_token)
        deletes_current = (
            current_session_id is not None
            and current_session_id.casefold() == session_id.casefold()
        )
        transport = cast("AuthDeleteMySessionTransport", self._client._transport)
        try:
            response = invoke(
                transport.auth_delete_my_session,
                authorization=current.access_token,
                session_id=session_id,
            )
            response_payload(response, 204)
        except TransportError as error:
            if deletes_current and not self._client._clear_session_if_current(
                generation
            ):
                raise SessionChangedError from error
            raise
        if deletes_current:
            current_unchanged = self._client._clear_session_if_current(generation)
        else:
            current_unchanged = self._client._capture_session()[0] == generation
        if not current_unchanged:
            raise SessionChangedError

    def confirm_email(self, *, token: str) -> None:
        """Confirm an email with its token without changing local state."""
        transport = cast("AuthConfirmEmailTransport", self._client._transport)
        response = invoke(
            transport.auth_confirm_email,
            authorization=self._client._anon_token(),
            token=token,
        )
        response_payload(response, 200)

    def resend_confirmation(self, *, email: str) -> None:
        """Request a generic confirmation resend without changing local state."""
        transport = cast("AuthResendConfirmationTransport", self._client._transport)
        response = invoke(
            transport.auth_resend_confirmation,
            authorization=self._client._anon_token(),
            email=email,
        )
        response_payload(response, 200)

    def reset_password(self, *, token: str, new_password: str) -> None:
        """Set a new password with a recovery token without changing local state."""
        transport = cast("AuthResetPasswordTransport", self._client._transport)
        response = invoke(
            transport.auth_reset_password,
            authorization=self._client._anon_token(),
            token=token,
            new_password=new_password,
        )
        response_payload(response, 200)

    def get_user(self) -> User:
        """Load a server-validated profile for the current session."""
        generation, current = self._client._capture_session()
        if current is None:
            raise AuthenticationError(_NO_ACTIVE_SESSION)
        transport = cast("AuthGetUserTransport", self._client._transport)
        response = invoke(transport.auth_get_user, authorization=current.access_token)
        user = _user_from_payload(response_payload(response, 200))
        if self._client._capture_session()[0] != generation:
            raise SessionChangedError
        return user

    def update_user(
        self,
        *,
        password: str | None = None,
        metadata: Mapping[str, object] | None = None,
    ) -> User:
        """Update and return the current user's server-validated profile."""
        generation, current = self._client._capture_session()
        if current is None:
            raise AuthenticationError(_NO_ACTIVE_SESSION)
        transport = cast("AuthUpdateUserTransport", self._client._transport)
        response = invoke(
            transport.auth_update_user,
            authorization=current.access_token,
            password=password,
            metadata=None if metadata is None else dict(metadata),
        )
        user = _user_from_payload(response_payload(response, 200))
        if self._client._capture_session()[0] != generation:
            raise SessionChangedError
        return user

    def sign_in(self, *, email: str, password: str) -> Session:
        """Sign in a user and store the returned session."""
        response = invoke(
            self._client._transport.auth_signin,
            authorization=self._client._anon_token(),
            email=email,
            password=password,
        )
        payload = response_payload(response, 200)
        session = _session_from_payload(payload)
        self._client._set_session(session)
        return session

    def refresh_session(self) -> Session:
        """Refresh and replace the current session."""
        generation, current = self._client._capture_session()
        if current is None:
            raise AuthenticationError(_NO_ACTIVE_SESSION)

        transport = cast("AuthRefreshTransport", self._client._transport)
        response = invoke(
            transport.auth_refresh,
            authorization=self._client._anon_token(),
            refresh_token=current.refresh_token,
        )
        try:
            payload = response_payload(response, 200)
        except AuthenticationError:
            self._client._clear_session_if_current(generation)
            raise
        refreshed = _session_from_payload(payload)
        if not self._client._set_session_if_current(refreshed, generation):
            raise SessionChangedError
        return refreshed

    def sign_out(self) -> None:
        """Revoke and clear the current session."""
        generation, current = self._client._capture_session()
        if current is None:
            return
        transport = cast("AuthLogoutTransport", self._client._transport)
        error: VolcanoError | None = None
        try:
            response = invoke(
                transport.auth_logout,
                authorization=self._client._anon_token(),
                refresh_token=current.refresh_token,
            )
            response_payload(response, 204)
        except VolcanoError as caught:
            error = caught
        if not self._client._clear_session_if_current(generation):
            raise SessionChangedError from error
        if error is not None:
            raise error
