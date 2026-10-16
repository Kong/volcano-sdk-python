from typing import Literal

AutofixRunTrigger = Literal['manual', 'new_issue', 'regression']

AUTOFIX_RUN_TRIGGER_VALUES: set[AutofixRunTrigger] = { 'manual', 'new_issue', 'regression',  }

def check_autofix_run_trigger(value: str) -> AutofixRunTrigger:
    if value in AUTOFIX_RUN_TRIGGER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTOFIX_RUN_TRIGGER_VALUES!r}")
