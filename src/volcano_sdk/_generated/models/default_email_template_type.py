from typing import Literal

DefaultEmailTemplateType = Literal['confirmation', 'password_changed', 'password_reset', 'welcome']

DEFAULT_EMAIL_TEMPLATE_TYPE_VALUES: set[DefaultEmailTemplateType] = { 'confirmation', 'password_changed', 'password_reset', 'welcome',  }

def check_default_email_template_type(value: str) -> DefaultEmailTemplateType:
    if value in DEFAULT_EMAIL_TEMPLATE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DEFAULT_EMAIL_TEMPLATE_TYPE_VALUES!r}")
