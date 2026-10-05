import pytest
from attrs import fields_dict

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


@pytest.mark.parametrize(
    ("tls", "wire_tls"),
    [
        (FrontendCustomDomainTLSConfig(mode="managed"), {"mode": "managed"}),
        (
            FrontendCustomDomainTLSConfig(
                mode="byoc",
                certificate_pem="certificate",
                private_key_pem="private-key",
            ),
            {
                "mode": "byoc",
                "certificate_pem": "certificate",
                "private_key_pem": "private-key",
            },
        ),
    ],
    ids=["managed", "byoc"],
)
def test_create_request_encodes_the_selected_tls_mode(
    tls: FrontendCustomDomainTLSConfig,
    wire_tls: dict[str, str],
) -> None:
    request = CreateFrontendCustomDomainRequest(domain="app.example.com", tls=tls)

    assert request.to_dict() == {"domain": "app.example.com", "tls": wire_tls}


@pytest.mark.parametrize(
    "model", [FrontendCustomDomainResponse, ProjectFrontendCustomDomain]
)
def test_domain_responses_do_not_declare_certificate_or_key_fields(
    model: type[FrontendCustomDomainResponse | ProjectFrontendCustomDomain],
) -> None:
    assert not [
        name
        for name in fields_dict(model)
        if any(marker in name for marker in ("certificate", "private_key", "pem"))
    ]


def test_managed_tls_response_exposes_provider_neutral_lifecycle() -> None:
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


def test_project_config_tls_decodes_each_mode_without_certificate_material() -> None:
    assert {
        "certificate_pem",
        "private_key_pem",
        "certificate_chain_pem",
    }.isdisjoint(fields_dict(ManagedProjectConfigFrontendCustomDomainTLSConfig))

    managed = ProjectConfigCustomDomain.from_dict(
        {"domain": "app.example.com", "tls": {"mode": "managed"}}
    )
    exported_byoc = ProjectConfigCustomDomain.from_dict(
        {"domain": "app.example.com", "tls": {"mode": "byoc"}}
    )

    assert isinstance(managed.tls, ManagedProjectConfigFrontendCustomDomainTLSConfig)
    assert managed.to_dict() == {
        "domain": "app.example.com",
        "tls": {"mode": "managed"},
    }
    assert isinstance(exported_byoc.tls, BYOCProjectConfigFrontendCustomDomainTLSConfig)
    assert exported_byoc.to_dict() == {
        "domain": "app.example.com",
        "tls": {"mode": "byoc"},
    }
