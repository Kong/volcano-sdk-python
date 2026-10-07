"""Typed generated Sandbox operation adapters."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from http import HTTPStatus
from io import BytesIO
from typing import TYPE_CHECKING, cast
from uuid import UUID

import httpx

from ._generated.api.sandboxes import (
    delete_sandbox,
    deploy_sandbox,
    get_sandbox_deployment,
    get_sandbox_deployment_logs,
    get_sandbox_deployment_source,
    list_sandbox_deployments,
)
from ._generated.api.sandboxes.create_sandbox_session import (
    request_kwargs as create_sandbox_session_kwargs,
)
from ._generated.api.sandboxes.create_sandbox_session_access import (
    request_kwargs as create_sandbox_session_access_kwargs,
)
from ._generated.api.sandboxes.execute_sandbox import (
    request_kwargs as execute_sandbox_kwargs,
)
from ._generated.api.sandboxes.execute_sandbox_session import (
    request_kwargs as execute_sandbox_session_kwargs,
)
from ._generated.api.sandboxes.get_sandbox_session import (
    request_kwargs as get_sandbox_session_kwargs,
)
from ._generated.api.sandboxes.grant_sandbox_session import (
    request_kwargs as grant_sandbox_session_kwargs,
)
from ._generated.api.sandboxes.list_sandbox_presets import (
    request_kwargs as list_sandbox_presets_kwargs,
)
from ._generated.api.sandboxes.read_sandbox_session_file import (
    request_kwargs as read_sandbox_session_file_kwargs,
)
from ._generated.api.sandboxes.resume_sandbox_session import (
    request_kwargs as resume_sandbox_session_kwargs,
)
from ._generated.api.sandboxes.revoke_sandbox_session import (
    request_kwargs as revoke_sandbox_session_kwargs,
)
from ._generated.api.sandboxes.suspend_sandbox_session import (
    request_kwargs as suspend_sandbox_session_kwargs,
)
from ._generated.api.sandboxes.terminate_sandbox_session import (
    request_kwargs as terminate_sandbox_session_kwargs,
)
from ._generated.api.sandboxes.write_sandbox_session_file import (
    request_kwargs as write_sandbox_session_file_kwargs,
)
from ._generated.models.deploy_sandbox_body import DeploySandboxBody
from ._generated.models.deploy_sandbox_body_memory_mb import (
    check_deploy_sandbox_body_memory_mb,
)
from ._generated.models.sandbox_access_request import SandboxAccessRequest
from ._generated.models.sandbox_command_request import SandboxCommandRequest
from ._generated.models.sandbox_file_read_request import SandboxFileReadRequest
from ._generated.models.sandbox_file_write_request import SandboxFileWriteRequest
from ._generated.models.sandbox_subject_grant_request import SandboxSubjectGrantRequest
from ._generated.types import UNSET, File
from ._transport_base import TransportBase
from ._transport_response import generated_request, unparsed_response
from ._transport_types import GeneratedTransportResponse
from .models import JSONValue

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from ._generated.client import AuthenticatedClient, Client
    from ._transport_types import TransportResponse


@dataclass(frozen=True)
class SandboxRequest:
    """One generated operation with immutable addressing."""

    operation: str
    resource_id: str = ""
    subject_id: str = ""
    body: Mapping[str, JSONValue] = field(default_factory=dict[str, JSONValue])
    request_id: str = ""
    timeout: float | None = None
    service_only: bool = False
    deployment_id: str = ""
    archive: bytes = field(default=b"", repr=False)
    cursor: str | None = None
    region: str = ""
    limit: int = 100


_OPERATIONS: dict[str, Callable[[SandboxRequest], dict[str, object]]] = {
    "delete_sandbox": lambda request: delete_sandbox.request_kwargs(
        UUID(request.resource_id), UUID(request.subject_id)
    ),
    "list_sandbox_deployments": lambda request: list_sandbox_deployments.request_kwargs(
        UUID(request.resource_id),
        UUID(request.subject_id),
        cursor=request.cursor if request.cursor is not None else UNSET,
    ),
    "get_sandbox_deployment": lambda request: get_sandbox_deployment.request_kwargs(
        UUID(request.resource_id), UUID(request.subject_id), UUID(request.deployment_id)
    ),
    "get_sandbox_deployment_source": lambda request: (
        get_sandbox_deployment_source.request_kwargs(
            UUID(request.resource_id),
            UUID(request.subject_id),
            UUID(request.deployment_id),
        )
    ),
    "get_sandbox_deployment_logs": lambda request: (
        get_sandbox_deployment_logs.request_kwargs(
            UUID(request.resource_id),
            UUID(request.subject_id),
            UUID(request.deployment_id),
            region=request.region,
            cursor=request.cursor if request.cursor is not None else UNSET,
            limit=request.limit,
        )
    ),
    "list_sandbox_presets": lambda _request: list_sandbox_presets_kwargs(),
    "create_sandbox_session": lambda request: create_sandbox_session_kwargs(
        UUID(request.resource_id),
        body=dict(request.body),
        idempotency_key=request.request_id,
    ),
    "execute_sandbox": lambda request: execute_sandbox_kwargs(
        UUID(request.resource_id),
        body=dict(request.body),
        idempotency_key=request.request_id,
    ),
    "get_sandbox_session": lambda request: get_sandbox_session_kwargs(
        UUID(request.resource_id)
    ),
    "execute_sandbox_session": lambda request: execute_sandbox_session_kwargs(
        UUID(request.resource_id),
        body=SandboxCommandRequest.from_dict(dict(request.body)),
        idempotency_key=request.request_id,
    ),
    "suspend_sandbox_session": lambda request: suspend_sandbox_session_kwargs(
        UUID(request.resource_id)
    ),
    "resume_sandbox_session": lambda request: resume_sandbox_session_kwargs(
        UUID(request.resource_id)
    ),
    "terminate_sandbox_session": lambda request: terminate_sandbox_session_kwargs(
        UUID(request.resource_id)
    ),
    "create_sandbox_session_access": lambda request: (
        create_sandbox_session_access_kwargs(
            UUID(request.resource_id),
            body=SandboxAccessRequest.from_dict(dict(request.body)),
        )
    ),
    "read_sandbox_session_file": lambda request: read_sandbox_session_file_kwargs(
        UUID(request.resource_id),
        body=SandboxFileReadRequest.from_dict(dict(request.body)),
    ),
    "write_sandbox_session_file": lambda request: write_sandbox_session_file_kwargs(
        UUID(request.resource_id),
        body=SandboxFileWriteRequest.from_dict(dict(request.body)),
    ),
    "grant_sandbox_session": lambda request: grant_sandbox_session_kwargs(
        UUID(request.resource_id),
        UUID(request.subject_id),
        body=SandboxSubjectGrantRequest.from_dict(dict(request.body)),
    ),
    "revoke_sandbox_session": lambda request: revoke_sandbox_session_kwargs(
        UUID(request.resource_id), UUID(request.subject_id)
    ),
}


class SandboxHTTPTransport(TransportBase):
    """Dispatch generated Sandbox operations without automatic replay."""

    def sandbox_request(
        self, *, authorization: str | None, request: SandboxRequest
    ) -> TransportResponse:
        """Return the raw HTTP result for facade validation.

        Returns:
            The status, headers, and decoded response body.

        """
        base_client = (
            self._public_client()
            if authorization is None
            else self._client(authorization)
        )
        timeout = self._timeout
        if request.timeout is not None:
            timeout = max(timeout, request.timeout)
        with base_client.with_timeout(httpx.Timeout(timeout)) as client:
            if request.operation == "deploy_sandbox":
                return _deploy(client, request)
            response = generated_request(
                client, _OPERATIONS[request.operation](request)
            )
        if (
            request.operation == "get_sandbox_deployment_source"
            and response.status_code == HTTPStatus.OK
        ):
            return GeneratedTransportResponse(
                status_code=response.status_code,
                payload=response.content,
                content=response.content,
                headers=dict(response.headers),
            )
        return unparsed_response(response)


def _deploy(
    client: AuthenticatedClient | Client, request: SandboxRequest
) -> TransportResponse:
    body = DeploySandboxBody(
        name=cast("str", request.body["name"]),
        code=File(
            payload=BytesIO(request.archive),
            file_name="source.tar.gz",
            mime_type="application/gzip",
        ),
        memory_mb=check_deploy_sandbox_body_memory_mb(
            cast("int", request.body["memory_mb"])
        ),
        ports=json.dumps(request.body.get("ports", [])),
    )
    return unparsed_response(
        deploy_sandbox.sync_detailed(
            UUID(request.resource_id),
            UUID(request.subject_id),
            client=cast("AuthenticatedClient", client),
            body=body,
            idempotency_key=request.request_id,
        )
    )
