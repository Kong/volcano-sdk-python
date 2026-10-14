from typing import Literal

AutofixStage = Literal['diagnose', 'pull_request']

AUTOFIX_STAGE_VALUES: set[AutofixStage] = { 'diagnose', 'pull_request',  }

def check_autofix_stage(value: str) -> AutofixStage:
    if value in AUTOFIX_STAGE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTOFIX_STAGE_VALUES!r}")
