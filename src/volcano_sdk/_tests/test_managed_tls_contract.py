import json
from uuid import UUID

import httpx
import pytest
from attrs import AttrsInstance, fields_dict

from volcano_sdk._generated.api.frontends import create_frontend_custom_domain
from volcano_sdk._generated.client import AuthenticatedClient
from volcano_sdk._generated.models import (
    BYOCProjectConfigFrontendCustomDomainTLSConfig,
    CreateFrontendCustomDomainRequest,
    Error,
    FrontendCustomDomainConflictError,
    FrontendCustomDomainResponse,
    FrontendCustomDomainTLSConfig,
    FrontendDomainRoutingRecord,
    FrontendDomainVerificationRecord,
    ManagedProjectConfigFrontendCustomDomainTLSConfig,
    ProjectConfigCustomDomain,
    ProjectFrontendCustomDomain,
)
from volcano_sdk._generated.types import UNSET, Unset

PROJECT_ID = UUID("00000000-0000-4000-8000-000000000001")
FRONTEND_ID = UUID("00000000-0000-4000-8000-000000000002")
BYOC_MATERIAL = {
    "certificate_pem": "certificate",
    "private_key_pem": "private-key",
    "certificate_chain_pem": "chain",
}
PROJECT_FEED_FIELDS = {"frontend": {"id": str(FRONTEND_ID), "name": "web"}}
OWNERSHIP_RECORD = {
    "name": "_volcano-ownership.app.example.com",
    "type": "TXT",
    "value": "volcano-ownership=token",
}
VALIDATION_RECORD = {
    "name": "_token.app.example.com",
    "type": "CNAME",
    "value": "_validation.volcano.dev",
}
ROUTING_TARGET = "frontend.frontends.volcano.dev"


def managed_pending() -> dict[str, object]:
    return {
        "domain": "app.example.com",
        "tls_mode": "managed",
        "domain_status": "pending_verification",
        "verification_status": "pending",
        "verification_records": [dict(VALIDATION_RECORD)],
        "routing_target_hostname": ROUTING_TARGET,
        "effective_urls": [f"https://{ROUTING_TARGET}/"],
        "created_at": "2026-09-02T12:00:00+00:00",
        "updated_at": "2026-09-02T12:00:00+00:00",
    }


def create_managed_domain(
    status: int, payload: dict[str, object]
) -> Error | FrontendCustomDomainConflictError | FrontendCustomDomainResponse | None:
    sent: list[httpx.Request] = []

    def respond(request: httpx.Request) -> httpx.Response:
        sent.append(request)
        return httpx.Response(status, json=payload)

    with AuthenticatedClient(
        base_url="https://api.example.com",
        token="access-token",
        httpx_args={"transport": httpx.MockTransport(respond)},
    ) as client:
        result = create_frontend_custom_domain.sync_detailed(
            PROJECT_ID,
            FRONTEND_ID,
            client=client,
            body=CreateFrontendCustomDomainRequest(
                domain="app.example.com",
                tls=FrontendCustomDomainTLSConfig(mode="managed"),
            ),
        )

    assert [json.loads(request.content) for request in sent] == [
        {"domain": "app.example.com", "tls": {"mode": "managed"}}
    ]
    return result.parsed


@pytest.mark.parametrize(
    ("tls", "wire_tls"),
    [
        (FrontendCustomDomainTLSConfig(mode="managed"), {"mode": "managed"}),
        (
            FrontendCustomDomainTLSConfig(
                mode="byoc",
                certificate_pem=BYOC_MATERIAL["certificate_pem"],
                private_key_pem=BYOC_MATERIAL["private_key_pem"],
                certificate_chain_pem=BYOC_MATERIAL["certificate_chain_pem"],
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
        FrontendCustomDomainConflictError,
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


@pytest.mark.parametrize("status", [200, 201], ids=["already-configured", "created"])
def test_create_operation_decodes_a_pending_managed_domain(status: int) -> None:
    created = create_managed_domain(status, managed_pending())

    assert isinstance(created, FrontendCustomDomainResponse)
    assert created.tls_mode == "managed"
    assert created.domain_status == "pending_verification"
    assert created.verification_status == "pending"
    assert created.failure_reason is UNSET
    assert created.required_routing_record is UNSET
    assert created.routing_target_hostname == ROUTING_TARGET
    assert created.to_dict() == managed_pending()


def test_create_conflict_carries_the_callers_ownership_record() -> None:
    conflict = create_managed_domain(
        409,
        {
            "error": "hostname is reserved by another account",
            "code": "ownership_verification_required",
            "required_record": dict(OWNERSHIP_RECORD),
        },
    )

    assert isinstance(conflict, FrontendCustomDomainConflictError)
    assert conflict.code == "ownership_verification_required"
    assert isinstance(conflict.required_record, FrontendDomainVerificationRecord)
    assert conflict.required_record.to_dict() == OWNERSHIP_RECORD


def test_other_create_conflicts_omit_the_ownership_fields() -> None:
    conflict = create_managed_domain(409, {"error": "custom domain already in use"})

    assert isinstance(conflict, FrontendCustomDomainConflictError)
    assert conflict.error == "custom domain already in use"
    assert conflict.code is UNSET
    assert conflict.required_record is UNSET


@pytest.mark.parametrize(
    ("tls_mode", "failure_fields", "failure_reason"),
    [
        ("managed", {"failure_reason": "ownership"}, "ownership"),
        ("byoc", {}, UNSET),
    ],
    ids=["managed", "byoc"],
)
@pytest.mark.parametrize(
    ("model", "feed_fields"),
    [
        (FrontendCustomDomainResponse, {}),
        (ProjectFrontendCustomDomain, PROJECT_FEED_FIELDS),
    ],
    ids=["frontend-domain", "project-feed"],
)
def test_failed_domain_decodes_with_and_without_failure_reason(
    model: type[FrontendCustomDomainResponse | ProjectFrontendCustomDomain],
    feed_fields: dict[str, dict[str, str]],
    tls_mode: str,
    failure_fields: dict[str, str],
    failure_reason: str | Unset,
) -> None:
    failed = model.from_dict(
        {
            **managed_pending(),
            **feed_fields,
            **failure_fields,
            "tls_mode": tls_mode,
            "domain_status": "failed",
            "verification_status": "failed",
        }
    )

    assert failed.tls_mode == tls_mode
    assert failed.domain_status == "failed"
    assert failed.verification_status == "failed"
    assert failed.failure_reason == failure_reason
    assert failed.routing_target_hostname == ROUTING_TARGET


@pytest.mark.parametrize(
    ("model", "feed_fields"),
    [
        (FrontendCustomDomainResponse, {}),
        (ProjectFrontendCustomDomain, PROJECT_FEED_FIELDS),
    ],
    ids=["frontend-domain", "project-feed"],
)
def test_deprecated_routing_record_from_older_servers_still_decodes(
    model: type[FrontendCustomDomainResponse | ProjectFrontendCustomDomain],
    feed_fields: dict[str, dict[str, str]],
) -> None:
    legacy_record = {
        "record_type": "CNAME",
        "name": "app.example.com",
        "value": ROUTING_TARGET,
    }
    legacy = {
        key: value
        for key, value in managed_pending().items()
        if key != "routing_target_hostname"
    }

    response = model.from_dict(
        {**legacy, **feed_fields, "required_routing_record": legacy_record}
    )

    assert response.routing_target_hostname is UNSET
    assert isinstance(response.required_routing_record, FrontendDomainRoutingRecord)
    assert response.required_routing_record.to_dict() == legacy_record


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
