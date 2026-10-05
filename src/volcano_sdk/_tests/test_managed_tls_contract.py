from attrs import fields_dict

from volcano_sdk._generated.models import (
    BYOCProjectConfigFrontendCustomDomainTLSConfig,
    CreateFrontendCustomDomainRequest,
    FrontendCustomDomainResponse,
    FrontendCustomDomainTLSConfig,
    FrontendDomainRoutingRecord,
    ManagedProjectConfigFrontendCustomDomainTLSConfig,
    ProjectConfigCustomDomain,
)


def test_managed_tls_request_omits_certificate_material() -> None:
    request = CreateFrontendCustomDomainRequest(
        domain="app.example.com",
        tls=FrontendCustomDomainTLSConfig(mode="managed"),
    )

    assert request.to_dict() == {
        "domain": "app.example.com",
        "tls": {"mode": "managed"},
    }


def test_byoc_tls_request_carries_certificate_material() -> None:
    request = CreateFrontendCustomDomainRequest(
        domain="app.example.com",
        tls=FrontendCustomDomainTLSConfig(
            mode="byoc",
            certificate_pem="certificate",
            private_key_pem="private-key",
        ),
    )

    assert request.to_dict() == {
        "domain": "app.example.com",
        "tls": {
            "mode": "byoc",
            "certificate_pem": "certificate",
            "private_key_pem": "private-key",
        },
    }


def test_managed_tls_response_exposes_provider_neutral_lifecycle() -> None:
    assert "managed_tls_certificate" not in fields_dict(FrontendCustomDomainResponse)

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
