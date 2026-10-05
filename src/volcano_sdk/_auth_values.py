"""Validate authentication response values at the transport boundary."""

from __future__ import annotations

import secrets
from collections.abc import Mapping
from datetime import datetime
from typing import TYPE_CHECKING, Literal, Protocol, TypeGuard, TypeVar, cast

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
from ._generated.models.call_o_auth_provider_api_response_200 import (
    CallOAuthProviderAPIResponse200,
)
from ._generated.models.get_o_auth_provider_token_response_200 import (
    GetOAuthProviderTokenResponse200,
)
from ._generated.models.refresh_o_auth_provider_token_response_200 import (
    RefreshOAuthProviderTokenResponse200,
)
from ._generated.types import Unset
from ._json_values import freeze_json
from .errors import (
    AuthenticationError,
    VolcanoError,
)
from .models import (
    AuthSession,
    EmailChangeResult,
    JSONValue,
    LinkedOAuthProvider,
    OAuthProviderName,
    OAuthProviderTokenStatus,
    Session,
    SessionPage,
    SignUpResult,
    User,
)

if TYPE_CHECKING:
    from ._generated.models import (
        AuthListOAuthProvidersResponse200ProvidersItem,
    )
    from ._generated.models.auth_session import AuthSession as GeneratedAuthSession


INCOMPLETE_SESSION = "Expected a complete Session"


INVALID_SIGN_UP_RESULT = "Expected a complete sign-up acknowledgement"


INVALID_EMAIL_CHANGE_RESULT = "Expected a valid email-change acknowledgement"


INVALID_USER = "Expected a complete user profile"


INVALID_SESSION_PAGE = "Expected a complete session page"


INVALID_LINKED_OAUTH_PROVIDERS = "Expected complete linked OAuth providers"


INVALID_OAUTH_LINK = "Expected an OAuth authorization URL"


INVALID_OAUTH_STATUS = "Expected complete OAuth provider token status"


INVALID_OAUTH_API_RESPONSE = "Expected OAuth provider API response data"


INVALID_AUTH_TRANSPORT = "Transport does not support the requested auth operation"


INVALID_AUTH_CALLBACK = "callback must be callable"


INVALID_HOSTED_AUTH_PARAMETER = "Hosted auth parameters must be non-empty strings"


HOSTED_AUTH_STATE_MISMATCH = "Hosted auth state mismatch"


UNSUPPORTED_HOSTED_AUTH_ACTION = "Unsupported hosted auth action"


UNSUPPORTED_OAUTH_PROVIDER = "Unsupported OAuth provider"


UNSUPPORTED_OAUTH_API_METHOD = "Unsupported OAuth provider API method"


INVALID_OAUTH_PARAMETER = "OAuth parameters must be non-empty strings"


INVALID_OAUTH_STATE = "OAuth state must not exceed 255 characters"


OAUTH_STATE_MISMATCH = "OAuth state mismatch"


MAX_OAUTH_STATE_LENGTH = 255


NO_ACTIVE_SESSION = "No active session"


REFRESH_UNAVAILABLE = "No refresh token"


T = TypeVar("T")


OAUTH_PROVIDERS: frozenset[str] = frozenset({"apple", "github", "google", "microsoft"})


OAUTH_API_METHODS: frozenset[str] = frozenset({"GET", "POST"})


HOSTED_AUTH_ACTIONS: frozenset[str] = frozenset({"login", "signup", "forgot-password"})


PATH_SEGMENT_SAFE = ""


def is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def is_object_mapping(value: object) -> TypeGuard[Mapping[object, object]]:
    return isinstance(value, Mapping)


def is_object_sequence(
    value: object,
) -> TypeGuard[list[object] | tuple[object, ...]]:
    return isinstance(value, (list, tuple))


def is_json_value(value: object) -> TypeGuard[JSONValue]:
    if value is None or isinstance(value, (str, int, float, bool)):
        return True
    if is_object_mapping(value):
        return is_json_mapping(value)
    if is_object_sequence(value):
        return all(is_json_value(item) for item in value)
    return False


def is_json_mapping(value: object) -> TypeGuard[Mapping[str, JSONValue]]:
    return is_object_mapping(value) and all(
        isinstance(key, str) and is_json_value(item) for key, item in value.items()
    )


def oauth_parameter(value: str) -> str:
    if not is_non_empty_string(value):
        raise ValueError(INVALID_OAUTH_PARAMETER)
    return value


def hosted_auth_parameter(value: str) -> str:
    if not is_non_empty_string(value):
        raise ValueError(INVALID_HOSTED_AUTH_PARAMETER)
    return value


def validate_hosted_auth_callback_state(state: str, expected_state: str) -> None:
    actual = hosted_auth_parameter(state).encode()
    expected = hosted_auth_parameter(expected_state).encode()
    if not secrets.compare_digest(actual, expected):
        raise ValueError(HOSTED_AUTH_STATE_MISMATCH)


def oauth_state(value: str) -> str:
    state = oauth_parameter(value)
    if len(state) > MAX_OAUTH_STATE_LENGTH:
        raise ValueError(INVALID_OAUTH_STATE)
    return state


def validate_oauth_callback_state(state: str, expected_state: str) -> None:
    actual = oauth_state(state).encode()
    expected = oauth_state(expected_state).encode()
    if not secrets.compare_digest(actual, expected):
        raise ValueError(OAUTH_STATE_MISMATCH)


def has_complete_values(session: Session) -> bool:
    return all(
        is_non_empty_string(value)
        for value in (
            session.access_token,
            session.refresh_token,
            session.user_id,
        )
    )


def copy_complete_session(session: object) -> Session:
    if not isinstance(session, Session) or not has_complete_values(session):
        raise ValueError(INCOMPLETE_SESSION)
    if session.user is not None and session.user.get("id") != session.user_id:
        raise ValueError(INCOMPLETE_SESSION)
    return Session(
        access_token=session.access_token,
        refresh_token=session.refresh_token,
        user_id=session.user_id,
        user=session.user,
    )


def session_from_payload(payload: object) -> Session:
    values: Mapping[object, object] = (
        cast("Mapping[object, object]", payload) if isinstance(payload, Mapping) else {}
    )
    raw_user = values.get("user")
    user: Mapping[object, object] = (
        cast("Mapping[object, object]", raw_user)
        if isinstance(raw_user, Mapping)
        else {}
    )
    if not is_json_mapping(user):
        raise TypeError(INCOMPLETE_SESSION)
    match (values.get("access_token"), values.get("refresh_token"), user.get("id")):
        case (str() as access, str() as refresh, str() as user_id):
            return copy_complete_session(
                Session(
                    access_token=access,
                    refresh_token=refresh,
                    user_id=user_id,
                    user=user,
                )
            )
        case _:
            raise ValueError(INCOMPLETE_SESSION)


def sign_up_result_from_payload(payload: object) -> SignUpResult:
    values: Mapping[object, object] = (
        cast("Mapping[object, object]", payload) if isinstance(payload, Mapping) else {}
    )
    confirmation_required = values.get("confirmation_required")
    message = values.get("message")
    if not isinstance(confirmation_required, bool) or not isinstance(message, str):
        raise TypeError(INVALID_SIGN_UP_RESULT)
    return SignUpResult(
        confirmation_required=confirmation_required,
        message=message,
    )


def email_change_result_from_payload(payload: object) -> EmailChangeResult:
    if not isinstance(payload, Mapping):
        raise TypeError(INVALID_EMAIL_CHANGE_RESULT)
    values = cast("Mapping[object, object]", payload)
    message = values.get("message")
    new_email = values.get("new_email")
    if message is not None and not isinstance(message, str):
        raise TypeError(INVALID_EMAIL_CHANGE_RESULT)
    if new_email is not None and not isinstance(new_email, str):
        raise TypeError(INVALID_EMAIL_CHANGE_RESULT)
    return EmailChangeResult(
        message=message,
        new_email=new_email,
    )


def user_from_payload(payload: object) -> tuple[User, Mapping[str, JSONValue]]:
    if not isinstance(
        payload,
        (
            AuthConvertAnonymousResponse200,
            AuthConfirmEmailChangeResponse200,
            AuthGetUserResponse200,
            AuthUpdateUserResponse200,
        ),
    ) or isinstance(payload.user, Unset):
        raise AuthenticationError(INVALID_USER)
    user = payload.user
    project_id = none_if_unset(user.project_id)
    user_metadata = none_if_unset(user.user_metadata)
    app_metadata = none_if_unset(user.app_metadata)
    user_metadata_value = None if user_metadata is None else user_metadata.to_dict()
    app_metadata_value = None if app_metadata is None else app_metadata.to_dict()
    if user_metadata_value is not None and not is_json_mapping(user_metadata_value):
        raise AuthenticationError(INVALID_USER)
    if app_metadata_value is not None and not is_json_mapping(app_metadata_value):
        raise AuthenticationError(INVALID_USER)
    profile = User(
        id=str(user.id),
        email=user.email,
        status=user.status,
        project_id=None if project_id is None else str(project_id),
        email_confirmed=none_if_unset(user.email_confirmed),
        user_metadata=user_metadata_value,
        app_metadata=app_metadata_value,
        avatar_url=none_if_unset(user.avatar_url),
        banned_until=none_if_unset(user.banned_until),
        last_sign_in_at=none_if_unset(user.last_sign_in_at),
        created_at=none_if_unset(user.created_at),
        updated_at=none_if_unset(user.updated_at),
    )
    snapshot = user.to_dict()
    if not is_json_mapping(snapshot):
        raise AuthenticationError(INVALID_USER)
    return profile, snapshot


def none_if_unset(value: T | Unset) -> T | None:
    return None if isinstance(value, Unset) else value


def auth_session_from_model(session: GeneratedAuthSession) -> AuthSession:
    return AuthSession(
        id=str(session.id),
        user_id=str(session.user_id),
        provider=session.provider,
        expires_at=session.expires_at,
        is_active=session_bool(session.is_active),
        is_current=session_bool(session.is_current),
        user_agent=optional_session_string(session.user_agent),
        ip_address=optional_session_string(session.ip_address),
        last_ip_address=optional_session_string(session.last_ip_address),
        last_activity_at=none_if_unset(session.last_activity_at),
        session_started_at=none_if_unset(session.session_started_at),
        created_at=none_if_unset(session.created_at),
        updated_at=none_if_unset(session.updated_at),
    )


def session_bool(value: object) -> bool:
    if not isinstance(value, bool):
        raise VolcanoError(INVALID_SESSION_PAGE)
    return value


def optional_session_string(value: object) -> str | None:
    if isinstance(value, Unset) or value is None:
        return None
    if not isinstance(value, str):
        raise VolcanoError(INVALID_SESSION_PAGE)
    return value


def session_page_from_payload(payload: object) -> SessionPage:
    if not isinstance(payload, AuthGetMySessionsResponse200):
        raise VolcanoError(INVALID_SESSION_PAGE)
    pagination = (
        payload.total,
        payload.page,
        payload.limit,
        payload.total_pages,
    )
    if isinstance(payload.sessions, Unset) or any(
        type(value) is not int for value in pagination
    ):
        raise VolcanoError(INVALID_SESSION_PAGE)
    return SessionPage(
        sessions=tuple(
            auth_session_from_model(session) for session in payload.sessions
        ),
        total=cast("int", payload.total),
        page=cast("int", payload.page),
        limit=cast("int", payload.limit),
        total_pages=cast("int", payload.total_pages),
    )


def linked_oauth_provider_from_model(
    item: AuthListOAuthProvidersResponse200ProvidersItem,
) -> LinkedOAuthProvider:
    provider = item.provider
    if not isinstance(provider, str) or not provider.strip():
        raise VolcanoError(INVALID_LINKED_OAUTH_PROVIDERS)
    return LinkedOAuthProvider(
        provider=provider,
        linked_at=linked_oauth_datetime(item.linked_at),
        updated_at=linked_oauth_datetime(item.updated_at),
    )


def linked_oauth_datetime(value: object) -> datetime:
    if not isinstance(value, datetime):
        raise VolcanoError(INVALID_LINKED_OAUTH_PROVIDERS)
    return value


def linked_oauth_providers_from_payload(
    payload: object,
) -> tuple[LinkedOAuthProvider, ...]:
    if not isinstance(payload, AuthListOAuthProvidersResponse200) or isinstance(
        payload.providers, Unset
    ):
        raise VolcanoError(INVALID_LINKED_OAUTH_PROVIDERS)
    return tuple(
        linked_oauth_provider_from_model(provider) for provider in payload.providers
    )


def oauth_provider_name(value: object) -> OAuthProviderName:
    if not isinstance(value, str) or value not in OAUTH_PROVIDERS:
        raise ValueError(UNSUPPORTED_OAUTH_PROVIDER)
    return cast("OAuthProviderName", value)


def oauth_api_method(value: object) -> Literal["GET", "POST"]:
    if not isinstance(value, str) or value not in OAUTH_API_METHODS:
        raise ValueError(UNSUPPORTED_OAUTH_API_METHOD)
    return cast('Literal["GET", "POST"]', value)


def oauth_link_from_payload(payload: object) -> str:
    if not isinstance(payload, AuthLinkOAuthProviderResponse200):
        raise VolcanoError(INVALID_OAUTH_LINK)
    authorization_url = payload.authorization_url
    if not isinstance(authorization_url, str) or not authorization_url.strip():
        raise VolcanoError(INVALID_OAUTH_LINK)
    return authorization_url


def oauth_provider_token_status_from_payload(
    payload: object,
) -> OAuthProviderTokenStatus:
    if not isinstance(
        payload,
        (GetOAuthProviderTokenResponse200, RefreshOAuthProviderTokenResponse200),
    ):
        raise VolcanoError(INVALID_OAUTH_STATUS)
    message = payload.message
    provider = payload.provider
    expires_in = payload.expires_in
    if (
        not is_non_empty_string(message)
        or not is_non_empty_string(provider)
        or type(expires_in) is not int
    ):
        raise VolcanoError(INVALID_OAUTH_STATUS)
    return OAuthProviderTokenStatus(
        message=cast("str", message),
        provider=cast("str", provider),
        expires_in=expires_in,
    )


class OAuthAPIData(Protocol):
    @property
    def data(self) -> object: ...


def oauth_api_data(payload: OAuthAPIData) -> object:
    return payload.data


def oauth_api_data_from_payload(payload: object) -> JSONValue:
    if not isinstance(payload, CallOAuthProviderAPIResponse200):
        raise VolcanoError(INVALID_OAUTH_API_RESPONSE)
    data = oauth_api_data(payload)
    if not is_json_value(data):
        raise VolcanoError(INVALID_OAUTH_API_RESPONSE)
    return freeze_json(data)
