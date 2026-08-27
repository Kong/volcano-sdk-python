from typing import Literal

CreateEmailTemplateRequestTemplateType = Literal['confirmation', 'password_changed', 'password_reset', 'welcome']

CREATE_EMAIL_TEMPLATE_REQUEST_TEMPLATE_TYPE_VALUES: set[CreateEmailTemplateRequestTemplateType] = { 'confirmation', 'password_changed', 'password_reset', 'welcome',  }

def check_create_email_template_request_template_type(value: str) -> CreateEmailTemplateRequestTemplateType:
    if value in CREATE_EMAIL_TEMPLATE_REQUEST_TEMPLATE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_EMAIL_TEMPLATE_REQUEST_TEMPLATE_TYPE_VALUES!r}")
