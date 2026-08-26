from typing import Literal

ProjectConfigVersion = Literal[1]

PROJECT_CONFIG_VERSION_VALUES: set[ProjectConfigVersion] = { 1,  }

def check_project_config_version(value: int) -> ProjectConfigVersion:
    if value in PROJECT_CONFIG_VERSION_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_CONFIG_VERSION_VALUES!r}")
