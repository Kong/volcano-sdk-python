from typing import Literal

ProjectFunctionCustomDomainTargetType = Literal['function']

PROJECT_FUNCTION_CUSTOM_DOMAIN_TARGET_TYPE_VALUES: set[ProjectFunctionCustomDomainTargetType] = { 'function',  }

def check_project_function_custom_domain_target_type(value: str) -> ProjectFunctionCustomDomainTargetType:
    if value in PROJECT_FUNCTION_CUSTOM_DOMAIN_TARGET_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_FUNCTION_CUSTOM_DOMAIN_TARGET_TYPE_VALUES!r}")
