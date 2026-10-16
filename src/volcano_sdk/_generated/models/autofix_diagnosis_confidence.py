from typing import Literal

AutofixDiagnosisConfidence = Literal['high', 'low', 'medium']

AUTOFIX_DIAGNOSIS_CONFIDENCE_VALUES: set[AutofixDiagnosisConfidence] = { 'high', 'low', 'medium',  }

def check_autofix_diagnosis_confidence(value: str) -> AutofixDiagnosisConfidence:
    if value in AUTOFIX_DIAGNOSIS_CONFIDENCE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AUTOFIX_DIAGNOSIS_CONFIDENCE_VALUES!r}")
