from typing import Literal

ProjectFrontendCustomDomainTargetType = Literal['frontend']

PROJECT_FRONTEND_CUSTOM_DOMAIN_TARGET_TYPE_VALUES: set[ProjectFrontendCustomDomainTargetType] = { 'frontend',  }

def check_project_frontend_custom_domain_target_type(value: str) -> ProjectFrontendCustomDomainTargetType:
    if value in PROJECT_FRONTEND_CUSTOM_DOMAIN_TARGET_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_FRONTEND_CUSTOM_DOMAIN_TARGET_TYPE_VALUES!r}")
