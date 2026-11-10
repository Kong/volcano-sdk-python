from typing import Literal

AccountSessionKind = Literal['browser', 'cli']

ACCOUNT_SESSION_KIND_VALUES: set[AccountSessionKind] = { 'browser', 'cli',  }

def check_account_session_kind(value: str) -> AccountSessionKind:
    if value in ACCOUNT_SESSION_KIND_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {ACCOUNT_SESSION_KIND_VALUES!r}")
