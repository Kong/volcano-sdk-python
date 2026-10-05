import pytest
from attrs import AttrsInstance, fields_dict

from volcano_sdk._generated.models import (
    BYOCProjectConfigFrontendCustomDomainTLSConfig,
    CreateFrontendCustomDomainRequest,
    FrontendCustomDomainResponse,
    FrontendCustomDomainTLSConfig,
    FrontendDomainRoutingRecord,
    FrontendDomainVerificationRecord,
    ManagedProjectConfigFrontendCustomDomainTLSConfig,
    ProjectConfigCustomDomain,
    ProjectFrontendCustomDomain,
)
from volcano_sdk._generated.types import UNSET

BYOC_MATERIAL = {
    "certificate_pem": "certificate",
    "private_key_pem": "private-key",
}
ROUTING_RECORD = {
    "record_type": "CNAME",
    "zone_apex_record_type": "ALIAS",
    "name": "app.example.com",
    "value": "frontend.frontends.volcano.dev",
}
VALIDATION_RECORD = {
    "name": "_token.app.example.com",
    "type": "CNAME",
    "value": "_validation.volcano.dev",
}
MANAGED_PENDING = {
    "domain": "app.example.com",
    "tls_mode": "managed",
    "domain_status": "pending_verification",
    "verification_status": "pending",
    "verification_records": [VALIDATION_RECORD],
    "required_routing_record": ROUTING_RECORD,
    "effective_urls": ["https://frontend.frontends.volcano.dev/"],
    "created_at": "2026-09-02T12:00:00Z",
    "updated_at": "2026-09-02T12:00:00Z",
}


@pytest.mark.parametrize(
    ("tls", "wire_tls"),
    [
        (FrontendCustomDomainTLSConfig(mode="managed"), {"mode": "managed"}),
        (
            FrontendCustomDomainTLSConfig(
                mode="byoc",
                certificate_pem=BYOC_MATERIAL["certificate_pem"],
                private_key_pem=BYOC_MATERIAL["private_key_pem"],
            ),
            {"mode": "byoc", **BYOC_MATERIAL},
        ),
    ],
    ids=["managed", "byoc"],
)
def test_create_request_encodes_the_selected_tls_mode(
    tls: FrontendCustomDomainTLSConfig,
    wire_tls: dict[str, str],
) -> None:
    wire_request = {"domain": "app.example.com", "tls": wire_tls}

    request = CreateFrontendCustomDomainRequest(domain="app.example.com", tls=tls)

    assert request.to_dict() == wire_request
    assert CreateFrontendCustomDomainRequest.from_dict(wire_request) == request


@pytest.mark.parametrize(
    "model",
    [
        FrontendCustomDomainResponse,
        ProjectFrontendCustomDomain,
        FrontendDomainVerificationRecord,
        FrontendDomainRoutingRecord,
        ManagedProjectConfigFrontendCustomDomainTLSConfig,
    ],
)
def test_material_free_models_do_not_declare_certificate_or_key_fields(
    model: type[AttrsInstance],
) -> None:
    assert not [
        name
        for name in fields_dict(model)
        if any(marker in name for marker in ("cert", "key", "pem"))
    ]


def test_managed_tls_response_decodes_lifecycle_and_dns_records() -> None:
    response = FrontendCustomDomainResponse.from_dict(MANAGED_PENDING)

    assert response.tls_mode == "managed"
    assert response.domain_status == "pending_verification"
    assert response.verification_status == "pending"
    assert response.failure_reason is UNSET
    assert isinstance(response.verification_records, list)
    assert [record.to_dict() for record in response.verification_records] == [
        VALIDATION_RECORD
    ]
    assert isinstance(response.required_routing_record, FrontendDomainRoutingRecord)
    assert response.required_routing_record.to_dict() == ROUTING_RECORD


@pytest.mark.parametrize(
    ("model", "feed_fields"),
    [
        (FrontendCustomDomainResponse, {}),
        (
            ProjectFrontendCustomDomain,
            {
                "frontend": {
                    "id": "00000000-0000-4000-8000-000000000001",
                    "name": "web",
                }
            },
        ),
    ],
    ids=["frontend-domain", "project-feed"],
)
def test_failed_managed_domain_reports_its_failure_reason(
    model: type[FrontendCustomDomainResponse | ProjectFrontendCustomDomain],
    feed_fields: dict[str, dict[str, str]],
) -> None:
    failed = model.from_dict(
        {
            **MANAGED_PENDING,
            **feed_fields,
            "domain_status": "failed",
            "verification_status": "failed",
            "failure_reason": "ownership",
        }
    )

    assert failed.domain_status == "failed"
    assert failed.verification_status == "failed"
    assert failed.failure_reason == "ownership"
    assert isinstance(failed.required_routing_record, FrontendDomainRoutingRecord)
    assert failed.required_routing_record.to_dict() == ROUTING_RECORD


@pytest.mark.parametrize(
    ("wire_tls", "variant"),
    [
        ({"mode": "managed"}, ManagedProjectConfigFrontendCustomDomainTLSConfig),
        ({"mode": "byoc"}, BYOCProjectConfigFrontendCustomDomainTLSConfig),
        (
            {"mode": "byoc", **BYOC_MATERIAL},
            BYOCProjectConfigFrontendCustomDomainTLSConfig,
        ),
    ],
    ids=["managed", "byoc-export", "byoc-apply"],
)
def test_project_config_tls_decodes_each_mode(
    wire_tls: dict[str, str],
    variant: type[
        ManagedProjectConfigFrontendCustomDomainTLSConfig
        | BYOCProjectConfigFrontendCustomDomainTLSConfig
    ],
) -> None:
    wire_domain = {"domain": "app.example.com", "tls": wire_tls}

    domain = ProjectConfigCustomDomain.from_dict(wire_domain)

    assert isinstance(domain.tls, variant)
    assert domain.to_dict() == wire_domain
