from typing import Literal

GetDefaultEmailTemplateType = Literal['confirmation', 'password_changed', 'password_reset', 'welcome']

GET_DEFAULT_EMAIL_TEMPLATE_TYPE_VALUES: set[GetDefaultEmailTemplateType] = { 'confirmation', 'password_changed', 'password_reset', 'welcome',  }

def check_get_default_email_template_type(value: str) -> GetDefaultEmailTemplateType:
    if value in GET_DEFAULT_EMAIL_TEMPLATE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_DEFAULT_EMAIL_TEMPLATE_TYPE_VALUES!r}")
