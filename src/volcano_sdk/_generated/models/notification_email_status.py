from typing import Literal

NotificationEmailStatus = Literal['delivering', 'disabled', 'owner_email_unverified']

NOTIFICATION_EMAIL_STATUS_VALUES: set[NotificationEmailStatus] = { 'delivering', 'disabled', 'owner_email_unverified',  }

def check_notification_email_status(value: str) -> NotificationEmailStatus:
    if value in NOTIFICATION_EMAIL_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {NOTIFICATION_EMAIL_STATUS_VALUES!r}")
