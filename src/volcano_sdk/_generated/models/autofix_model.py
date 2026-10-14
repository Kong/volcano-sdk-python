from typing import Literal

AutofixModel = Literal['claude-fable-5-1', 'claude-haiku-4-5', 'claude-haiku-5-5', 'claude-opus-5', 'claude-opus-5-5', 'claude-sonnet-5', 'claude-sonnet-5-5']

AUTOFIX_MODEL_VALUES: set[AutofixModel] = { 'claude-fable-5-1', 'claude-haiku-4-5', 'claude-haiku-5-5', 'claude-opus-5', 'claude-opus-5-5', 'claude-sonnet-5', 'claude-sonnet-5-5',  }

def check_autofix_model(value: str) -> AutofixModel:
    if value in AUTOFIX_MODEL_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTOFIX_MODEL_VALUES!r}")
