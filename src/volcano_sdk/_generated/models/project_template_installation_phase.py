from typing import Literal

ProjectTemplateInstallationPhase = Literal['configure', 'database', 'deploy', 'ready', 'restore', 'verify']

PROJECT_TEMPLATE_INSTALLATION_PHASE_VALUES: set[ProjectTemplateInstallationPhase] = { 'configure', 'database', 'deploy', 'ready', 'restore', 'verify',  }

def check_project_template_installation_phase(value: str) -> ProjectTemplateInstallationPhase:
    if value in PROJECT_TEMPLATE_INSTALLATION_PHASE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_TEMPLATE_INSTALLATION_PHASE_VALUES!r}")
