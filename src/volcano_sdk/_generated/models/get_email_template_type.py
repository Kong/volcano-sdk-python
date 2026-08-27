from typing import Literal

GetEmailTemplateType = Literal['confirmation', 'password_changed', 'password_reset', 'welcome']

GET_EMAIL_TEMPLATE_TYPE_VALUES: set[GetEmailTemplateType] = { 'confirmation', 'password_changed', 'password_reset', 'welcome',  }

def check_get_email_template_type(value: str) -> GetEmailTemplateType:
    if value in GET_EMAIL_TEMPLATE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_EMAIL_TEMPLATE_TYPE_VALUES!r}")
