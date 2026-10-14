from typing import Literal

AutofixProvider = Literal['anthropic', 'volcano']

AUTOFIX_PROVIDER_VALUES: set[AutofixProvider] = { 'anthropic', 'volcano',  }

def check_autofix_provider(value: str) -> AutofixProvider:
    if value in AUTOFIX_PROVIDER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTOFIX_PROVIDER_VALUES!r}")
