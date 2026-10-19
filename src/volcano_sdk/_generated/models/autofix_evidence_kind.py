from typing import Literal

AutofixEvidenceKind = Literal['code', 'log', 'other']

AUTOFIX_EVIDENCE_KIND_VALUES: set[AutofixEvidenceKind] = { 'code', 'log', 'other',  }

def check_autofix_evidence_kind(value: str) -> AutofixEvidenceKind:
    if value in AUTOFIX_EVIDENCE_KIND_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTOFIX_EVIDENCE_KIND_VALUES!r}")
