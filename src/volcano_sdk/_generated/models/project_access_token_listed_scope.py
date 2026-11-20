from typing import Literal

ProjectAccessTokenListedScope = Literal['delegated', 'full', 'read_only']

PROJECT_ACCESS_TOKEN_LISTED_SCOPE_VALUES: set[ProjectAccessTokenListedScope] = { 'delegated', 'full', 'read_only',  }

def check_project_access_token_listed_scope(value: str) -> ProjectAccessTokenListedScope:
    if value in PROJECT_ACCESS_TOKEN_LISTED_SCOPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_ACCESS_TOKEN_LISTED_SCOPE_VALUES!r}")
