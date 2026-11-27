from typing import Literal

NotificationTestDeliveryChannel = Literal['email', 'webhook']

NOTIFICATION_TEST_DELIVERY_CHANNEL_VALUES: set[NotificationTestDeliveryChannel] = { 'email', 'webhook',  }

def check_notification_test_delivery_channel(value: str) -> NotificationTestDeliveryChannel:
    if value in NOTIFICATION_TEST_DELIVERY_CHANNEL_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {NOTIFICATION_TEST_DELIVERY_CHANNEL_VALUES!r}")
