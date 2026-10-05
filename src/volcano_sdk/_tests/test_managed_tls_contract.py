import pytest
from attrs import AttrsInstance, fields_dict

from volcano_sdk._generated.models import (
    BYOCProjectConfigFrontendCustomDomainTLSConfig,
    CreateFrontendCustomDomainRequest,
    FrontendCustomDomainResponse,
    FrontendCustomDomainTLSConfig,
    FrontendDomainRoutingRecord,
    ManagedProjectConfigFrontendCustomDomainTLSConfig,
    ProjectConfigCustomDomain,
    ProjectFrontendCustomDomain,
)
from volcano_sdk._generated.types import UNSET

BYOC_MATERIAL = {
    "certificate_pem": "certificate",
    "private_key_pem": "private-key",
}


@pytest.mark.parametrize(
    "wire_tls",
    [{"mode": "managed"}, {"mode": "byoc", **BYOC_MATERIAL}],
    ids=["managed", "byoc"],
)
def test_create_request_round_trips_the_selected_tls_mode(
    wire_tls: dict[str, str],
) -> None:
    wire_request = {"domain": "app.example.com", "tls": wire_tls}

    request = CreateFrontendCustomDomainRequest.from_dict(wire_request)

    assert isinstance(request.tls, FrontendCustomDomainTLSConfig)
    assert request.tls.mode == wire_tls["mode"]
    assert request.to_dict() == wire_request


@pytest.mark.parametrize(
    "model",
    [
        FrontendCustomDomainResponse,
        ProjectFrontendCustomDomain,
        ManagedProjectConfigFrontendCustomDomainTLSConfig,
    ],
)
def test_material_free_models_do_not_declare_certificate_or_key_fields(
    model: type[AttrsInstance],
) -> None:
    assert not [
        name
        for name in fields_dict(model)
        if any(marker in name for marker in ("certificate", "private_key", "pem"))
    ]


def test_managed_tls_response_decodes_lifecycle_and_dns_records() -> None:
    response = FrontendCustomDomainResponse.from_dict(
        {
            "domain": "app.example.com",
            "tls_mode": "managed",
            "domain_status": "pending_verification",
            "verification_status": "pending",
            "verification_records": [
                {
                    "name": "_token.app.example.com",
                    "type": "CNAME",
                    "value": "_validation.volcano.dev",
                }
            ],
            "required_routing_record": {
                "record_type": "CNAME",
                "zone_apex_record_type": "ALIAS",
                "name": "app.example.com",
                "value": "frontend.frontends.volcano.dev",
            },
            "effective_urls": ["https://frontend.frontends.volcano.dev/"],
            "created_at": "2026-09-02T12:00:00Z",
            "updated_at": "2026-09-02T12:00:00Z",
        }
    )
    assert response.tls_mode == "managed"
    assert response.domain_status == "pending_verification"
    assert response.verification_status == "pending"
    assert response.failure_reason is UNSET
    assert isinstance(response.verification_records, list)
    assert response.verification_records[0].to_dict() == {
        "name": "_token.app.example.com",
        "type": "CNAME",
        "value": "_validation.volcano.dev",
    }
    assert isinstance(response.required_routing_record, FrontendDomainRoutingRecord)
    assert response.required_routing_record.to_dict() == {
        "record_type": "CNAME",
        "zone_apex_record_type": "ALIAS",
        "name": "app.example.com",
        "value": "frontend.frontends.volcano.dev",
    }

    failed = FrontendCustomDomainResponse.from_dict(
        {
            **response.to_dict(),
            "domain_status": "failed",
            "verification_status": "failed",
            "failure_reason": "ownership",
        }
    )
    assert failed.domain_status == "failed"
    assert failed.verification_status == "failed"
    assert failed.failure_reason == "ownership"


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
    ids=["managed", "byoc-export", "byoc-rotation"],
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
