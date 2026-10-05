"""Email identity, confirmation, and password recovery operations."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._auth_base import AuthBase
from ._auth_values import (
    INVALID_AUTH_TRANSPORT,
    NO_ACTIVE_SESSION,
    email_change_result_from_payload,
)
from ._transport import (
    AuthCancelEmailChangeTransport,
    AuthConfirmEmailChangeTransport,
    AuthConfirmEmailTransport,
    AuthForgotPasswordTransport,
    AuthRequestEmailChangeTransport,
    AuthResendConfirmationTransport,
    AuthResetPasswordTransport,
    invoke,
    response_payload,
)
from .errors import (
    AuthenticationError,
)

if TYPE_CHECKING:
    from .models import (
        EmailChangeResult,
        User,
    )


class EmailAuth(AuthBase):
    """Email identity, confirmation, and password recovery operations."""

    def reset_password_for_email(self, *, email: str) -> None:
        """Request a reset email without revealing whether the account exists.

        Raises:
            TypeError: The transport does not support this authentication operation.

        """
        transport = self._client.transport()
        if not isinstance(transport, AuthForgotPasswordTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        response = invoke(
            transport.auth_forgot_password,
            authorization=self._client.anon_token(),
            email=email,
        )
        _ = response_payload(response, 200)

    def request_email_change(self, *, new_email: str) -> EmailChangeResult:
        """Request a confirmation email without changing the current session.

        Returns:
            The server acknowledgement of the requested email change.

        Raises:
            AuthenticationError: There is no active session.
            TypeError: The transport does not support this authentication operation.

        """
        binding = self._client.capture_session_binding()
        if binding[2] is None:
            raise AuthenticationError(NO_ACTIVE_SESSION)
        transport = self._client.transport()
        if not isinstance(transport, AuthRequestEmailChangeTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        response = self._requests.request(
            lambda access_token: invoke(
                transport.auth_request_email_change,
                authorization=access_token,
                new_email=new_email,
            ),
            binding=binding,
        )
        result = email_change_result_from_payload(response_payload(response, 200))
        _ = self._requests.owned_session(binding)
        return result

    def cancel_email_change(self) -> None:
        """Cancel a pending email change without changing the current session.

        Raises:
            AuthenticationError: There is no active session.
            TypeError: The transport does not support this authentication operation.

        """
        binding = self._client.capture_session_binding()
        if binding[2] is None:
            raise AuthenticationError(NO_ACTIVE_SESSION)
        transport = self._client.transport()
        if not isinstance(transport, AuthCancelEmailChangeTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        response = self._requests.request(
            lambda access_token: invoke(
                transport.auth_cancel_email_change,
                authorization=access_token,
            ),
            binding=binding,
        )
        _ = response_payload(response, 200)
        _ = self._requests.owned_session(binding)

    def confirm_email_change(self, *, token: str) -> User:
        """Confirm a pending email change and return the updated user.

        Returns:
            The updated profile after confirming the new email.

        Raises:
            AuthenticationError: There is no active session.
            TypeError: The transport does not support this authentication operation.

        """
        binding = self._client.capture_session_binding()
        if binding[2] is None:
            raise AuthenticationError(NO_ACTIVE_SESSION)
        transport = self._client.transport()
        if not isinstance(transport, AuthConfirmEmailChangeTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        response = self._requests.request(
            lambda access_token: invoke(
                transport.auth_confirm_email_change,
                authorization=access_token,
                token=token,
            ),
            binding=binding,
        )
        return self._update_current_user(response_payload(response, 200), binding)

    def confirm_email(self, *, token: str) -> None:
        """Confirm an email with its token without changing local state.

        Raises:
            TypeError: The transport does not support this authentication operation.

        """
        transport = self._client.transport()
        if not isinstance(transport, AuthConfirmEmailTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        response = invoke(
            transport.auth_confirm_email,
            authorization=self._client.anon_token(),
            token=token,
        )
        _ = response_payload(response, 200)

    def resend_confirmation(self, *, email: str) -> None:
        """Request a generic confirmation resend without changing local state.

        Raises:
            TypeError: The transport does not support this authentication operation.

        """
        transport = self._client.transport()
        if not isinstance(transport, AuthResendConfirmationTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        response = invoke(
            transport.auth_resend_confirmation,
            authorization=self._client.anon_token(),
            email=email,
        )
        _ = response_payload(response, 200)

    def reset_password(self, *, token: str, new_password: str) -> None:
        """Set a new password with a recovery token without changing local state.

        Raises:
            TypeError: The transport does not support this authentication operation.

        """
        transport = self._client.transport()
        if not isinstance(transport, AuthResetPasswordTransport):
            raise TypeError(INVALID_AUTH_TRANSPORT)
        response = invoke(
            transport.auth_reset_password,
            authorization=self._client.anon_token(),
            token=token,
            new_password=new_password,
        )
        _ = response_payload(response, 200)
