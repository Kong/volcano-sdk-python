from typing import Literal

EmailTemplateTemplateType = Literal['confirmation', 'password_changed', 'password_reset', 'welcome']

EMAIL_TEMPLATE_TEMPLATE_TYPE_VALUES: set[EmailTemplateTemplateType] = { 'confirmation', 'password_changed', 'password_reset', 'welcome',  }

def check_email_template_template_type(value: str) -> EmailTemplateTemplateType:
    if value in EMAIL_TEMPLATE_TEMPLATE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {EMAIL_TEMPLATE_TEMPLATE_TYPE_VALUES!r}")
