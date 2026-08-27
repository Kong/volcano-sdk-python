from typing import Literal

GetProjectConfigFormat = Literal['json', 'yaml']

GET_PROJECT_CONFIG_FORMAT_VALUES: set[GetProjectConfigFormat] = { 'json', 'yaml',  }

def check_get_project_config_format(value: str) -> GetProjectConfigFormat:
    if value in GET_PROJECT_CONFIG_FORMAT_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_PROJECT_CONFIG_FORMAT_VALUES!r}")
