from typing import Literal

SandboxFileEntrySha256Skipped = Literal['budget', 'changing', 'unreadable']

SANDBOX_FILE_ENTRY_SHA_256_SKIPPED_VALUES: set[SandboxFileEntrySha256Skipped] = { 'budget', 'changing', 'unreadable',  }

def check_sandbox_file_entry_sha_256_skipped(value: str) -> SandboxFileEntrySha256Skipped:
    if value in SANDBOX_FILE_ENTRY_SHA_256_SKIPPED_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SANDBOX_FILE_ENTRY_SHA_256_SKIPPED_VALUES!r}")
