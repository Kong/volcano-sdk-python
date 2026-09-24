from typing import Literal

FrontendVariableScope = Literal['all', 'scoped', 'shared']

FRONTEND_VARIABLE_SCOPE_VALUES: set[FrontendVariableScope] = { 'all', 'scoped', 'shared',  }

def check_frontend_variable_scope(value: str) -> FrontendVariableScope:
    if value in FRONTEND_VARIABLE_SCOPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FRONTEND_VARIABLE_SCOPE_VALUES!r}")
