from typing import Literal

VariableDeploySource = Literal['api', 'cli', 'git', 'system', 'unknown', 'web']

VARIABLE_DEPLOY_SOURCE_VALUES: set[VariableDeploySource] = { 'api', 'cli', 'git', 'system', 'unknown', 'web',  }

def check_variable_deploy_source(value: str) -> VariableDeploySource:
    if value in VARIABLE_DEPLOY_SOURCE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {VARIABLE_DEPLOY_SOURCE_VALUES!r}")
