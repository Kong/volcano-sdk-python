import json
from collections.abc import Callable
from datetime import UTC, datetime
from uuid import UUID

import httpx
import pytest
from attrs import AttrsInstance, fields_dict

from volcano_sdk._generated.api.frontends import (
    create_frontend_custom_domain,
    get_frontend_custom_domain,
)
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
OWNERSHIP_CHALLENGE = {
    "name": "_volcano.app.example.com",
    "type": "TXT",
    "value": "volcano-domain-verification=0123456789abcdef0123456789abcdef",
}
CERTIFICATE_VALIDATION = {
    "name": "_acme-challenge.app.example.com",
    "type": "CNAME",
    "value": "7d7b8a4e-7418-4a86-8e16-670870f00fa0.acme.frontends.volcano.run",
}
ROUTING_TARGET = "my-frontend.frontends.volcano.run"
CREATED_AT = datetime(2026, 9, 2, 12, tzinfo=UTC)
DOMAIN_PATH = f"/projects/{PROJECT_ID}/frontends/{FRONTEND_ID}/domain"
DomainEntry = FrontendCustomDomainResponse | ProjectFrontendCustomDomain


def domain_payload() -> dict[str, object]:
    return {
        "domain": "app.example.com",
        "tls_mode": "managed",
        "domain_status": "pending_verification",
        "verification_status": "pending",
        "routing_target_hostname": ROUTING_TARGET,
        "effective_urls": [f"https://{ROUTING_TARGET}/"],
        "created_at": "2026-09-02T12:00:00Z",
        "updated_at": "2026-09-02T12:00:00Z",
    }


def mock_client(
    status: int, payload: dict[str, object]
) -> tuple[AuthenticatedClient, list[httpx.Request]]:
    sent: list[httpx.Request] = []

    def respond(request: httpx.Request) -> httpx.Response:
        sent.append(request)
        return httpx.Response(status, json=payload)

    client = AuthenticatedClient(
        base_url="https://api.example.com",
        token="access-token",
        httpx_args={"transport": httpx.MockTransport(respond)},
    )
    return client, sent


def create_managed_domain(
    status: int, payload: dict[str, object]
) -> Error | FrontendCustomDomainConflictError | FrontendCustomDomainResponse | None:
    client, sent = mock_client(status, payload)
    with client:
        result = create_frontend_custom_domain.sync_detailed(
            PROJECT_ID,
            FRONTEND_ID,
            client=client,
            body=CreateFrontendCustomDomainRequest(
                domain="app.example.com",
                tls=FrontendCustomDomainTLSConfig(mode="managed"),
            ),
        )

    assert [
        (request.method, request.url.path, request.headers["Authorization"])
        for request in sent
    ] == [("POST", DOMAIN_PATH, "Bearer access-token")]
    assert json.loads(sent[0].content) == {
        "domain": "app.example.com",
        "tls": {"mode": "managed"},
    }
    assert result.status_code == status
    return result.parsed


def poll_domain(payload: dict[str, object]) -> DomainEntry:
    client, sent = mock_client(200, payload)
    with client:
        result = get_frontend_custom_domain.sync_detailed(
            PROJECT_ID, FRONTEND_ID, client=client
        )

    assert [(request.method, request.url.path) for request in sent] == [
        ("GET", DOMAIN_PATH)
    ]
    assert isinstance(result.parsed, FrontendCustomDomainResponse)
    return result.parsed


def decode_project_feed_entry(payload: dict[str, object]) -> DomainEntry:
    return ProjectFrontendCustomDomain.from_dict(
        {**payload, "frontend": {"id": str(FRONTEND_ID), "name": "my-frontend"}}
    )


DOMAIN_DECODERS = pytest.mark.parametrize(
    "decode",
    [poll_domain, decode_project_feed_entry],
    ids=["domain-status", "project-feed"],
)


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
def test_models_without_tls_material_declare_no_pem_or_private_key_fields(
    model: type[AttrsInstance],
) -> None:
    assert not [
        name
        for name in fields_dict(model)
        if name.endswith("_pem") or "private_key" in name
    ]


@pytest.mark.parametrize("status", [200, 201], ids=["already-configured", "created"])
def test_create_operation_decodes_the_ownership_challenge(status: int) -> None:
    created = create_managed_domain(
        status,
        {**domain_payload(), "verification_records": [OWNERSHIP_CHALLENGE]},
    )

    assert isinstance(created, FrontendCustomDomainResponse)
    assert created.tls_mode == "managed"
    assert created.domain_status == "pending_verification"
    assert created.verification_status == "pending"
    assert isinstance(created.verification_records, list)
    assert [record.to_dict() for record in created.verification_records] == [
        OWNERSHIP_CHALLENGE
    ]
    assert created.routing_target_hostname == ROUTING_TARGET
    assert created.required_routing_record is UNSET
    assert created.failure_reason is UNSET
    assert created.created_at == CREATED_AT


@DOMAIN_DECODERS
def test_pending_domain_decodes_the_certificate_validation_record(
    decode: Callable[[dict[str, object]], DomainEntry],
) -> None:
    pending = decode(
        {**domain_payload(), "verification_records": [CERTIFICATE_VALIDATION]}
    )

    assert isinstance(pending.verification_records, list)
    assert [record.to_dict() for record in pending.verification_records] == [
        CERTIFICATE_VALIDATION
    ]
    assert pending.routing_target_hostname == ROUTING_TARGET


def test_create_conflict_carries_the_callers_ownership_record() -> None:
    payload: dict[str, object] = {
        "error": (
            "custom domain is reserved by another account until its ownership "
            "is verified"
        ),
        "code": "ownership_verification_required",
        "required_record": OWNERSHIP_CHALLENGE,
    }

    conflict = create_managed_domain(409, payload)

    assert isinstance(conflict, FrontendCustomDomainConflictError)
    assert conflict.error == payload["error"]
    assert conflict.code == "ownership_verification_required"
    assert isinstance(conflict.required_record, FrontendDomainVerificationRecord)
    assert conflict.required_record.to_dict() == OWNERSHIP_CHALLENGE
    assert conflict.to_dict() == payload


def test_other_create_conflicts_omit_the_ownership_fields() -> None:
    conflict = create_managed_domain(409, {"error": "custom domain already in use"})

    assert isinstance(conflict, FrontendCustomDomainConflictError)
    assert conflict.error == "custom domain already in use"
    assert conflict.code is UNSET
    assert conflict.required_record is UNSET


@pytest.mark.parametrize("status", [400, 503], ids=["bad-request", "unavailable"])
def test_other_create_errors_keep_the_plain_error_shape(status: int) -> None:
    error = create_managed_domain(status, {"error": "custom domain rejected"})

    assert type(error) is Error
    assert error.error == "custom domain rejected"


@pytest.mark.parametrize(
    ("failure_fields", "failure_reason"),
    [
        (
            {
                "tls_mode": "managed",
                "verification_status": "failed",
                "failure_reason": "ownership",
            },
            "ownership",
        ),
        (
            {
                "tls_mode": "managed",
                "verification_status": "verified",
                "failure_reason": "certificate",
            },
            "certificate",
        ),
        (
            {
                "tls_mode": "managed",
                "verification_status": "failed",
                "failure_reason": "quota",
            },
            "quota",
        ),
        ({"tls_mode": "managed", "verification_status": "failed"}, UNSET),
        ({"tls_mode": "byoc", "verification_status": "failed"}, UNSET),
    ],
    ids=[
        "managed",
        "managed-after-verification",
        "unrecognized-reason",
        "managed-uncategorized",
        "byoc",
    ],
)
@DOMAIN_DECODERS
def test_failed_domain_decodes_its_failure_reason(
    decode: Callable[[dict[str, object]], DomainEntry],
    failure_fields: dict[str, str],
    failure_reason: str | Unset,
) -> None:
    failed = decode({**domain_payload(), **failure_fields, "domain_status": "failed"})

    assert failed.tls_mode == failure_fields["tls_mode"]
    assert failed.domain_status == "failed"
    assert failed.verification_status == failure_fields["verification_status"]
    assert failed.failure_reason == failure_reason


@DOMAIN_DECODERS
def test_deprecated_routing_record_from_older_servers_round_trips(
    decode: Callable[[dict[str, object]], DomainEntry],
) -> None:
    legacy_record = {
        "record_type": "CNAME",
        "name": "app.example.com",
        "value": ROUTING_TARGET,
    }
    legacy = {
        key: value
        for key, value in domain_payload().items()
        if key != "routing_target_hostname"
    }

    response = decode({**legacy, "required_routing_record": legacy_record})

    assert response.routing_target_hostname is UNSET
    assert isinstance(response.required_routing_record, FrontendDomainRoutingRecord)
    assert response.required_routing_record.to_dict() == legacy_record
    assert response.to_dict()["required_routing_record"] == legacy_record


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


def test_project_config_domain_without_tls_keeps_the_stored_certificate() -> None:
    domain = ProjectConfigCustomDomain.from_dict({"domain": "app.example.com"})

    assert domain.tls is UNSET
    assert domain.to_dict() == {"domain": "app.example.com"}
