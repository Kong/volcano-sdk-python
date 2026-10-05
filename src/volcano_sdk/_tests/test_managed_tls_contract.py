from attrs import fields_dict

from volcano_sdk._generated.models import (
    CreateFrontendCustomDomainRequest,
    FrontendCustomDomainResponse,
    FrontendCustomDomainTLSConfig,
    FrontendDomainRoutingRecord,
    ManagedFrontendCustomDomainTLSConfig,
    ManagedProjectConfigFrontendCustomDomainTLSConfig,
)


def test_managed_tls_models_keep_the_public_contract_provider_neutral() -> None:
    request = CreateFrontendCustomDomainRequest(
        domain="app.example.com",
        tls=ManagedFrontendCustomDomainTLSConfig(mode="managed"),
    )

    assert request.to_dict() == {
        "domain": "app.example.com",
        "tls": {"mode": "managed"},
    }
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
        {**response.to_dict(), "verification_status": "failed"}
    )
    assert failed.verification_status == "failed"


def test_managed_project_config_model_cannot_serialize_certificate_material() -> None:
    assert {
        "certificate_pem",
        "private_key_pem",
        "certificate_chain_pem",
    }.isdisjoint(fields_dict(ManagedProjectConfigFrontendCustomDomainTLSConfig))
    assert ManagedProjectConfigFrontendCustomDomainTLSConfig.from_dict(
        {"mode": "managed"}
    ).to_dict() == {"mode": "managed"}


def test_legacy_byoc_model_keeps_its_default_mode() -> None:
    legacy = FrontendCustomDomainTLSConfig(
        certificate_pem="certificate",
        private_key_pem="private-key",
    )

    assert legacy.to_dict() == {
        "mode": "byoc",
        "certificate_pem": "certificate",
        "private_key_pem": "private-key",
    }
