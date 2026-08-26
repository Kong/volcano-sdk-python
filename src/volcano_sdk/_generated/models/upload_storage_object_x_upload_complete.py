from typing import Literal

UploadStorageObjectXUploadComplete = Literal['true']

UPLOAD_STORAGE_OBJECT_X_UPLOAD_COMPLETE_VALUES: set[UploadStorageObjectXUploadComplete] = { 'true',  }

def check_upload_storage_object_x_upload_complete(value: str) -> UploadStorageObjectXUploadComplete:
    if value in UPLOAD_STORAGE_OBJECT_X_UPLOAD_COMPLETE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {UPLOAD_STORAGE_OBJECT_X_UPLOAD_COMPLETE_VALUES!r}")
