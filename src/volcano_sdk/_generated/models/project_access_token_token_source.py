from typing import Literal

ProjectAccessTokenTokenSource = Literal['api', 'cli', 'dashboard']

PROJECT_ACCESS_TOKEN_TOKEN_SOURCE_VALUES: set[ProjectAccessTokenTokenSource] = { 'api', 'cli', 'dashboard',  }

def check_project_access_token_token_source(value: str) -> ProjectAccessTokenTokenSource:
    if value in PROJECT_ACCESS_TOKEN_TOKEN_SOURCE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_ACCESS_TOKEN_TOKEN_SOURCE_VALUES!r}")
