from typing import Literal

CreateDurableFunctionBodyVariableScope = Literal['all', 'scoped']

CREATE_DURABLE_FUNCTION_BODY_VARIABLE_SCOPE_VALUES: set[CreateDurableFunctionBodyVariableScope] = { 'all', 'scoped',  }

def check_create_durable_function_body_variable_scope(value: str) -> CreateDurableFunctionBodyVariableScope:
    if value in CREATE_DURABLE_FUNCTION_BODY_VARIABLE_SCOPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_DURABLE_FUNCTION_BODY_VARIABLE_SCOPE_VALUES!r}")
