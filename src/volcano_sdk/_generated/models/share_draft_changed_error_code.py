from typing import Literal

ShareDraftChangedErrorCode = Literal['draft_changed']

SHARE_DRAFT_CHANGED_ERROR_CODE_VALUES: set[ShareDraftChangedErrorCode] = { 'draft_changed',  }

def check_share_draft_changed_error_code(value: str) -> ShareDraftChangedErrorCode:
    if value in SHARE_DRAFT_CHANGED_ERROR_CODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SHARE_DRAFT_CHANGED_ERROR_CODE_VALUES!r}")
