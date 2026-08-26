from typing import Literal

FrontendFramework = Literal['nextjs']

FRONTEND_FRAMEWORK_VALUES: set[FrontendFramework] = { 'nextjs',  }

def check_frontend_framework(value: str) -> FrontendFramework:
    if value in FRONTEND_FRAMEWORK_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FRONTEND_FRAMEWORK_VALUES!r}")
