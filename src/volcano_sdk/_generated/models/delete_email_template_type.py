from typing import Literal

DeleteEmailTemplateType = Literal['confirmation', 'password_changed', 'password_reset', 'welcome']

DELETE_EMAIL_TEMPLATE_TYPE_VALUES: set[DeleteEmailTemplateType] = { 'confirmation', 'password_changed', 'password_reset', 'welcome',  }

def check_delete_email_template_type(value: str) -> DeleteEmailTemplateType:
    if value in DELETE_EMAIL_TEMPLATE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DELETE_EMAIL_TEMPLATE_TYPE_VALUES!r}")
