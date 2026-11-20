from typing import Literal

ProjectConfigCustomDomainRedirectStatus = Literal[301, 302, 307, 308]

PROJECT_CONFIG_CUSTOM_DOMAIN_REDIRECT_STATUS_VALUES: set[ProjectConfigCustomDomainRedirectStatus] = { 301, 302, 307, 308,  }

def check_project_config_custom_domain_redirect_status(value: int) -> ProjectConfigCustomDomainRedirectStatus:
    if value in PROJECT_CONFIG_CUSTOM_DOMAIN_REDIRECT_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_CONFIG_CUSTOM_DOMAIN_REDIRECT_STATUS_VALUES!r}")
