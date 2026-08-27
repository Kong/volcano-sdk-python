from typing import Literal

CreateAnonKeyBodyPermissionsItem = Literal['auth.confirm_email', 'auth.logout', 'auth.password_reset', 'auth.refresh', 'auth.resend_confirmation', 'auth.signin', 'auth.signup', 'functions.invoke', 'realtime.connect', 'realtime.publish', 'realtime.subscribe', 'storage.delete', 'storage.download', 'storage.list', 'storage.upload']

CREATE_ANON_KEY_BODY_PERMISSIONS_ITEM_VALUES: set[CreateAnonKeyBodyPermissionsItem] = { 'auth.confirm_email', 'auth.logout', 'auth.password_reset', 'auth.refresh', 'auth.resend_confirmation', 'auth.signin', 'auth.signup', 'functions.invoke', 'realtime.connect', 'realtime.publish', 'realtime.subscribe', 'storage.delete', 'storage.download', 'storage.list', 'storage.upload',  }

def check_create_anon_key_body_permissions_item(value: str) -> CreateAnonKeyBodyPermissionsItem:
    if value in CREATE_ANON_KEY_BODY_PERMISSIONS_ITEM_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_ANON_KEY_BODY_PERMISSIONS_ITEM_VALUES!r}")
