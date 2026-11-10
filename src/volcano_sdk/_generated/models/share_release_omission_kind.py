from typing import Literal

ShareReleaseOmissionKind = Literal['database', 'no_source', 'sandbox', 'secret_file', 'unsupported_entry']

SHARE_RELEASE_OMISSION_KIND_VALUES: set[ShareReleaseOmissionKind] = { 'database', 'no_source', 'sandbox', 'secret_file', 'unsupported_entry',  }

def check_share_release_omission_kind(value: str) -> ShareReleaseOmissionKind:
    if value in SHARE_RELEASE_OMISSION_KIND_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SHARE_RELEASE_OMISSION_KIND_VALUES!r}")
