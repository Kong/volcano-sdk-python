from typing import Literal

CreateFrontendBodyFramework = Literal['nextjs']

CREATE_FRONTEND_BODY_FRAMEWORK_VALUES: set[CreateFrontendBodyFramework] = { 'nextjs',  }

def check_create_frontend_body_framework(value: str) -> CreateFrontendBodyFramework:
    if value in CREATE_FRONTEND_BODY_FRAMEWORK_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_FRONTEND_BODY_FRAMEWORK_VALUES!r}")
