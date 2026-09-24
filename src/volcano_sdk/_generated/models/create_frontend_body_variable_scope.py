from typing import Literal

CreateFrontendBodyVariableScope = Literal['all', 'scoped']

CREATE_FRONTEND_BODY_VARIABLE_SCOPE_VALUES: set[CreateFrontendBodyVariableScope] = { 'all', 'scoped',  }

def check_create_frontend_body_variable_scope(value: str) -> CreateFrontendBodyVariableScope:
    if value in CREATE_FRONTEND_BODY_VARIABLE_SCOPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_FRONTEND_BODY_VARIABLE_SCOPE_VALUES!r}")
