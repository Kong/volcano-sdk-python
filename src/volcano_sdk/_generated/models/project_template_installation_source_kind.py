from typing import Literal

ProjectTemplateInstallationSourceKind = Literal['share_release']

PROJECT_TEMPLATE_INSTALLATION_SOURCE_KIND_VALUES: set[ProjectTemplateInstallationSourceKind] = { 'share_release',  }

def check_project_template_installation_source_kind(value: str) -> ProjectTemplateInstallationSourceKind:
    if value in PROJECT_TEMPLATE_INSTALLATION_SOURCE_KIND_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_TEMPLATE_INSTALLATION_SOURCE_KIND_VALUES!r}")
