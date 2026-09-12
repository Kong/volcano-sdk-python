from typing import Literal

ProjectConfigFunctionVariableScope = Literal['all', 'scoped']

PROJECT_CONFIG_FUNCTION_VARIABLE_SCOPE_VALUES: set[ProjectConfigFunctionVariableScope] = { 'all', 'scoped',  }

def check_project_config_function_variable_scope(value: str) -> ProjectConfigFunctionVariableScope:
    if value in PROJECT_CONFIG_FUNCTION_VARIABLE_SCOPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_CONFIG_FUNCTION_VARIABLE_SCOPE_VALUES!r}")
