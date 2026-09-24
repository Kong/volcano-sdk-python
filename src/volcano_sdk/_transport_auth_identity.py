"""Generated auth identity operation adapters."""

from __future__ import annotations

from ._generated.api.authentication import (
    auth_logout,
    auth_refresh,
    auth_signin,
    auth_signup,
)
from ._generated.api.authentication.auth_cancel_email_change import (
    request_kwargs as cancel_email_change_kwargs,
)
from ._generated.api.authentication.auth_confirm_email import (
    request_kwargs as confirm_email_kwargs,
)
from ._generated.api.authentication.auth_confirm_email_change import (
    build_response as build_auth_confirm_email_change_response,
)
from ._generated.api.authentication.auth_confirm_email_change import (
    request_kwargs as auth_confirm_email_change_kwargs,
)
from ._generated.api.authentication.auth_convert_anonymous import (
    build_response as build_auth_convert_anonymous_response,
)
from ._generated.api.authentication.auth_convert_anonymous import (
    request_kwargs as auth_convert_anonymous_kwargs,
)
from ._generated.api.authentication.auth_forgot_password import (
    request_kwargs as forgot_password_kwargs,
)
from ._generated.api.authentication.auth_get_user import (
    build_response as build_auth_get_user_response,
)
from ._generated.api.authentication.auth_get_user import (
    request_kwargs as auth_get_user_kwargs,
)
from ._generated.api.authentication.auth_request_email_change import (
    request_kwargs as request_email_change_kwargs,
)
from ._generated.api.authentication.auth_resend_confirmation import (
    request_kwargs as resend_confirmation_kwargs,
)
from ._generated.api.authentication.auth_reset_password import (
    request_kwargs as reset_password_kwargs,
)
from ._generated.api.authentication.auth_signup_anonymous import (
    request_kwargs as signup_anonymous_kwargs,
)
from ._generated.api.authentication.auth_update_user import (
    build_response as build_auth_update_user_response,
)
from ._generated.api.authentication.auth_update_user import (
    request_kwargs as auth_update_user_kwargs,
)
from ._generated.models.auth_confirm_email_body import AuthConfirmEmailBody
from ._generated.models.auth_confirm_email_change_body import AuthConfirmEmailChangeBody
from ._generated.models.auth_convert_anonymous_body import AuthConvertAnonymousBody
from ._generated.models.auth_convert_anonymous_body_user_metadata import (
    AuthConvertAnonymousBodyUserMetadata,
)
from ._generated.models.auth_forgot_password_body import AuthForgotPasswordBody
from ._generated.models.auth_logout_body import AuthLogoutBody
from ._generated.models.auth_refresh_body import AuthRefreshBody
from ._generated.models.auth_request_email_change_body import AuthRequestEmailChangeBody
from ._generated.models.auth_resend_confirmation_body import AuthResendConfirmationBody
from ._generated.models.auth_reset_password_body import AuthResetPasswordBody
from ._generated.models.auth_signin_body import AuthSigninBody
from ._generated.models.auth_signup_anonymous_body import AuthSignupAnonymousBody
from ._generated.models.auth_signup_anonymous_body_user_metadata import (
    AuthSignupAnonymousBodyUserMetadata,
)
from ._generated.models.auth_signup_body import AuthSignupBody
from ._generated.models.auth_signup_body_user_metadata import (
    AuthSignupBodyUserMetadata,
)
from ._generated.models.auth_update_user_body import AuthUpdateUserBody
from ._generated.models.auth_update_user_body_user_metadata import (
    AuthUpdateUserBodyUserMetadata,
)
from ._generated.types import UNSET
from ._transport_base import TransportBase
from ._transport_response import (
    generated_request,
    parsed_response,
    unparsed_response,
)
from ._transport_types import (
    HTTP_OK,
    HTTP_UNAUTHORIZED,
    MALFORMED_USER_PROFILE,
    GeneratedTransportResponse,
    TransportResponse,
)
from .errors import (
    AuthenticationError,
)


class AuthIdentityTransport(TransportBase):
    """Adapt generated auth identity operations to the SDK transport."""

    def auth_signin(
        self,
        *,
        authorization: str,
        email: str,
        password: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = auth_signin.sync_detailed(
                client=client,
                body=AuthSigninBody(email=email, password=password),
            )
        return parsed_response(response)

    def auth_signup(
        self,
        *,
        authorization: str,
        email: str,
        password: str,
        metadata: dict[str, object],
    ) -> TransportResponse:
        body = AuthSignupBody(
            email=email,
            password=password,
            user_metadata=AuthSignupBodyUserMetadata.from_dict(metadata),
        )
        with self._client(authorization) as client:
            response = auth_signup.sync_detailed(client=client, body=body)
        return parsed_response(response)

    def auth_signup_anonymous(
        self,
        *,
        authorization: str,
        metadata: dict[str, object],
    ) -> TransportResponse:
        body = AuthSignupAnonymousBody(
            user_metadata=AuthSignupAnonymousBodyUserMetadata.from_dict(metadata)
        )
        with self._client(authorization) as client:
            response = generated_request(client, signup_anonymous_kwargs(body=body))
        return unparsed_response(response)

    def auth_convert_anonymous(
        self,
        *,
        authorization: str,
        email: str,
        password: str,
        metadata: dict[str, object],
    ) -> TransportResponse:
        body = AuthConvertAnonymousBody(
            email=email,
            password=password,
            user_metadata=AuthConvertAnonymousBodyUserMetadata.from_dict(metadata),
        )
        try:
            with self._client(authorization) as client:
                raw_response = generated_request(
                    client, auth_convert_anonymous_kwargs(body=body)
                )
                if raw_response.status_code == HTTP_UNAUTHORIZED:
                    return unparsed_response(raw_response)
                response = build_auth_convert_anonymous_response(
                    client=client, response=raw_response
                )
        except (
            AttributeError,
            KeyError,
            TypeError,
            UnicodeDecodeError,
            ValueError,
        ) as error:
            raise AuthenticationError(MALFORMED_USER_PROFILE) from error
        if int(response.status_code) != HTTP_OK:
            return parsed_response(response)
        return GeneratedTransportResponse(
            status_code=int(response.status_code),
            payload=response.parsed,
            content=response.content,
            headers=dict(response.headers),
        )

    def auth_forgot_password(
        self,
        *,
        authorization: str,
        email: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = generated_request(
                client, forgot_password_kwargs(body=AuthForgotPasswordBody(email=email))
            )
        return unparsed_response(response)

    def auth_confirm_email(
        self,
        *,
        authorization: str,
        token: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = generated_request(
                client, confirm_email_kwargs(body=AuthConfirmEmailBody(token=token))
            )
        return unparsed_response(response)

    def auth_reset_password(
        self,
        *,
        authorization: str,
        token: str,
        new_password: str,
    ) -> TransportResponse:
        body = AuthResetPasswordBody(token=token, new_password=new_password)
        with self._client(authorization) as client:
            response = generated_request(client, reset_password_kwargs(body=body))
        return unparsed_response(response)

    def auth_resend_confirmation(
        self,
        *,
        authorization: str,
        email: str,
    ) -> TransportResponse:
        body = AuthResendConfirmationBody(email=email)
        with self._client(authorization) as client:
            response = generated_request(client, resend_confirmation_kwargs(body=body))
        return unparsed_response(response)

    def auth_request_email_change(
        self,
        *,
        authorization: str,
        new_email: str,
    ) -> TransportResponse:
        body = AuthRequestEmailChangeBody(new_email=new_email)
        with self._client(authorization) as client:
            response = generated_request(client, request_email_change_kwargs(body=body))
        return unparsed_response(response)

    def auth_cancel_email_change(self, *, authorization: str) -> TransportResponse:
        with self._client(authorization) as client:
            response = generated_request(client, cancel_email_change_kwargs())
        return unparsed_response(response)

    def auth_confirm_email_change(
        self,
        *,
        authorization: str,
        token: str,
    ) -> TransportResponse:
        body = AuthConfirmEmailChangeBody(email_change_token=token)
        try:
            with self._client(authorization) as client:
                raw_response = generated_request(
                    client, auth_confirm_email_change_kwargs(body=body)
                )
                if raw_response.status_code == HTTP_UNAUTHORIZED:
                    return unparsed_response(raw_response)
                response = build_auth_confirm_email_change_response(
                    client=client, response=raw_response
                )
        except (
            AttributeError,
            KeyError,
            TypeError,
            UnicodeDecodeError,
            ValueError,
        ) as error:
            raise AuthenticationError(MALFORMED_USER_PROFILE) from error
        if int(response.status_code) != HTTP_OK:
            return parsed_response(response)
        return GeneratedTransportResponse(
            status_code=int(response.status_code),
            payload=response.parsed,
            content=response.content,
            headers=dict(response.headers),
        )

    def auth_get_user(self, *, authorization: str) -> TransportResponse:
        try:
            with self._client(authorization) as client:
                raw_response = generated_request(client, auth_get_user_kwargs())
                if raw_response.status_code == HTTP_UNAUTHORIZED:
                    return unparsed_response(raw_response)
                response = build_auth_get_user_response(
                    client=client, response=raw_response
                )
        except (
            AttributeError,
            KeyError,
            TypeError,
            UnicodeDecodeError,
            ValueError,
        ) as error:
            raise AuthenticationError(MALFORMED_USER_PROFILE) from error
        if int(response.status_code) != HTTP_OK:
            return parsed_response(response)
        return GeneratedTransportResponse(
            status_code=int(response.status_code),
            payload=response.parsed,
            content=response.content,
            headers=dict(response.headers),
        )

    def auth_update_user(
        self,
        *,
        authorization: str,
        password: str | None,
        metadata: dict[str, object] | None,
    ) -> TransportResponse:
        body = AuthUpdateUserBody(
            password=UNSET if password is None else password,
            user_metadata=(
                UNSET
                if metadata is None
                else AuthUpdateUserBodyUserMetadata.from_dict(metadata)
            ),
        )
        try:
            with self._client(authorization) as client:
                raw_response = generated_request(
                    client, auth_update_user_kwargs(body=body)
                )
                if raw_response.status_code == HTTP_UNAUTHORIZED:
                    return unparsed_response(raw_response)
                response = build_auth_update_user_response(
                    client=client, response=raw_response
                )
        except (
            AttributeError,
            KeyError,
            TypeError,
            UnicodeDecodeError,
            ValueError,
        ) as error:
            raise AuthenticationError(MALFORMED_USER_PROFILE) from error
        if int(response.status_code) != HTTP_OK:
            return parsed_response(response)
        return GeneratedTransportResponse(
            status_code=int(response.status_code),
            payload=response.parsed,
            content=response.content,
            headers=dict(response.headers),
        )

    def auth_refresh(
        self,
        *,
        authorization: str,
        refresh_token: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = auth_refresh.sync_detailed(
                client=client,
                body=AuthRefreshBody(refresh_token=refresh_token),
            )
        return parsed_response(response)

    def auth_logout(
        self,
        *,
        authorization: str,
        refresh_token: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = auth_logout.sync_detailed(
                client=client,
                body=AuthLogoutBody(refresh_token=refresh_token),
            )
        return parsed_response(response)
