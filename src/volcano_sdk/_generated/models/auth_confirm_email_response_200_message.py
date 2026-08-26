from typing import Literal

AuthConfirmEmailResponse200Message = Literal['Email already confirmed', 'Email confirmed successfully']

AUTH_CONFIRM_EMAIL_RESPONSE_200_MESSAGE_VALUES: set[AuthConfirmEmailResponse200Message] = { 'Email already confirmed', 'Email confirmed successfully',  }

def check_auth_confirm_email_response_200_message(value: str) -> AuthConfirmEmailResponse200Message:
    if value in AUTH_CONFIRM_EMAIL_RESPONSE_200_MESSAGE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTH_CONFIRM_EMAIL_RESPONSE_200_MESSAGE_VALUES!r}")
