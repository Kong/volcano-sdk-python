from typing import Literal

ProjectConfigFrontendVariableScope = Literal['all', 'scoped', 'shared']

PROJECT_CONFIG_FRONTEND_VARIABLE_SCOPE_VALUES: set[ProjectConfigFrontendVariableScope] = { 'all', 'scoped', 'shared',  }

def check_project_config_frontend_variable_scope(value: str) -> ProjectConfigFrontendVariableScope:
    if value in PROJECT_CONFIG_FRONTEND_VARIABLE_SCOPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_CONFIG_FRONTEND_VARIABLE_SCOPE_VALUES!r}")
