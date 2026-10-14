from typing import Literal

FrontendCustomDomainResponseServingCertificate = Literal['managed', 'uploaded']

FRONTEND_CUSTOM_DOMAIN_RESPONSE_SERVING_CERTIFICATE_VALUES: set[FrontendCustomDomainResponseServingCertificate] = { 'managed', 'uploaded',  }

def check_frontend_custom_domain_response_serving_certificate(value: str) -> FrontendCustomDomainResponseServingCertificate:
    if value in FRONTEND_CUSTOM_DOMAIN_RESPONSE_SERVING_CERTIFICATE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FRONTEND_CUSTOM_DOMAIN_RESPONSE_SERVING_CERTIFICATE_VALUES!r}")
