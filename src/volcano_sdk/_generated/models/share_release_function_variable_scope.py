from typing import Literal

ShareReleaseFunctionVariableScope = Literal['scoped']

SHARE_RELEASE_FUNCTION_VARIABLE_SCOPE_VALUES: set[ShareReleaseFunctionVariableScope] = { 'scoped',  }

def check_share_release_function_variable_scope(value: str) -> ShareReleaseFunctionVariableScope:
    if value in SHARE_RELEASE_FUNCTION_VARIABLE_SCOPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SHARE_RELEASE_FUNCTION_VARIABLE_SCOPE_VALUES!r}")
