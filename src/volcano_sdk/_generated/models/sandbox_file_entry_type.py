from typing import Literal

SandboxFileEntryType = Literal['directory', 'file', 'other', 'symlink']

SANDBOX_FILE_ENTRY_TYPE_VALUES: set[SandboxFileEntryType] = { 'directory', 'file', 'other', 'symlink',  }

def check_sandbox_file_entry_type(value: str) -> SandboxFileEntryType:
    if value in SANDBOX_FILE_ENTRY_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SANDBOX_FILE_ENTRY_TYPE_VALUES!r}")
