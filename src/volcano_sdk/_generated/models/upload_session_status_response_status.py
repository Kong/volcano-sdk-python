from typing import Literal

UploadSessionStatusResponseStatus = Literal['aborted', 'completed', 'completing', 'pending', 'uploading']

UPLOAD_SESSION_STATUS_RESPONSE_STATUS_VALUES: set[UploadSessionStatusResponseStatus] = { 'aborted', 'completed', 'completing', 'pending', 'uploading',  }

def check_upload_session_status_response_status(value: str) -> UploadSessionStatusResponseStatus:
    if value in UPLOAD_SESSION_STATUS_RESPONSE_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {UPLOAD_SESSION_STATUS_RESPONSE_STATUS_VALUES!r}")
