from typing import Literal

UpdateEmailTemplateType = Literal['confirmation', 'password_changed', 'password_reset', 'welcome']

UPDATE_EMAIL_TEMPLATE_TYPE_VALUES: set[UpdateEmailTemplateType] = { 'confirmation', 'password_changed', 'password_reset', 'welcome',  }

def check_update_email_template_type(value: str) -> UpdateEmailTemplateType:
    if value in UPDATE_EMAIL_TEMPLATE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {UPDATE_EMAIL_TEMPLATE_TYPE_VALUES!r}")
