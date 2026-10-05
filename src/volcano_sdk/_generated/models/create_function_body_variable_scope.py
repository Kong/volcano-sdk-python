from typing import Literal

CreateFunctionBodyVariableScope = Literal['all', 'scoped']

CREATE_FUNCTION_BODY_VARIABLE_SCOPE_VALUES: set[CreateFunctionBodyVariableScope] = { 'all', 'scoped',  }

def check_create_function_body_variable_scope(value: str) -> CreateFunctionBodyVariableScope:
    if value in CREATE_FUNCTION_BODY_VARIABLE_SCOPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_FUNCTION_BODY_VARIABLE_SCOPE_VALUES!r}")
