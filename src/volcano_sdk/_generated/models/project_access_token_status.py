from typing import Literal

ProjectAccessTokenStatus = Literal['active', 'expired', 'revoked']

PROJECT_ACCESS_TOKEN_STATUS_VALUES: set[ProjectAccessTokenStatus] = { 'active', 'expired', 'revoked',  }

def check_project_access_token_status(value: str) -> ProjectAccessTokenStatus:
    if value in PROJECT_ACCESS_TOKEN_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_ACCESS_TOKEN_STATUS_VALUES!r}")
