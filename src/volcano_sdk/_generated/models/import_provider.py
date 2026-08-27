from typing import Literal

ImportProvider = Literal['vercel']

IMPORT_PROVIDER_VALUES: set[ImportProvider] = { 'vercel',  }

def check_import_provider(value: str) -> ImportProvider:
    if value in IMPORT_PROVIDER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {IMPORT_PROVIDER_VALUES!r}")
