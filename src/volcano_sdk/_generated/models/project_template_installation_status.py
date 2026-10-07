from typing import Literal

ProjectTemplateInstallationStatus = Literal['failed', 'pending', 'ready', 'running']

PROJECT_TEMPLATE_INSTALLATION_STATUS_VALUES: set[ProjectTemplateInstallationStatus] = { 'failed', 'pending', 'ready', 'running',  }

def check_project_template_installation_status(value: str) -> ProjectTemplateInstallationStatus:
    if value in PROJECT_TEMPLATE_INSTALLATION_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_TEMPLATE_INSTALLATION_STATUS_VALUES!r}")
