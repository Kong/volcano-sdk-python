from typing import Literal

ProjectCustomDomainTargetType = Literal['frontend', 'function']

PROJECT_CUSTOM_DOMAIN_TARGET_TYPE_VALUES: set[ProjectCustomDomainTargetType] = { 'frontend', 'function',  }

def check_project_custom_domain_target_type(value: str) -> ProjectCustomDomainTargetType:
    if value in PROJECT_CUSTOM_DOMAIN_TARGET_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_CUSTOM_DOMAIN_TARGET_TYPE_VALUES!r}")
