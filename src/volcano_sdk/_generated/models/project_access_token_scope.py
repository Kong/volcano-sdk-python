from typing import Literal

ProjectAccessTokenScope = Literal['full', 'read_only']

PROJECT_ACCESS_TOKEN_SCOPE_VALUES: set[ProjectAccessTokenScope] = { 'full', 'read_only',  }

def check_project_access_token_scope(value: str) -> ProjectAccessTokenScope:
    if value in PROJECT_ACCESS_TOKEN_SCOPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_ACCESS_TOKEN_SCOPE_VALUES!r}")
