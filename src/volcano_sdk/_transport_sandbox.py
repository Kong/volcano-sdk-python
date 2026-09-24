"""Typed generated Sandbox operation adapters."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from uuid import UUID

import httpx

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
from ._generated.models.sandbox_access_request import SandboxAccessRequest
from ._generated.models.sandbox_command_request import SandboxCommandRequest
from ._generated.models.sandbox_file_read_request import SandboxFileReadRequest
from ._generated.models.sandbox_file_write_request import SandboxFileWriteRequest
from ._generated.models.sandbox_subject_grant_request import SandboxSubjectGrantRequest
from ._transport_base import TransportBase
from ._transport_response import generated_request, unparsed_response
from .models import JSONValue

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from ._transport_types import TransportResponse


@dataclass(frozen=True)
class SandboxRequest:
    """One generated operation with immutable addressing."""

    operation: str
    resource_id: str = ""
    subject_id: str = ""
    body: Mapping[str, JSONValue] = field(default_factory=dict[str, JSONValue])
    request_id: str = ""
    timeout: float = 180.0


_OPERATIONS: dict[str, Callable[[SandboxRequest], dict[str, object]]] = {
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
        self, *, authorization: str, request: SandboxRequest
    ) -> TransportResponse:
        """Return the raw HTTP result for facade validation.

        Returns:
            The status, headers, and decoded response body.

        """
        with self._client(authorization).with_timeout(
            httpx.Timeout(max(self._timeout, request.timeout))
        ) as client:
            response = generated_request(
                client, _OPERATIONS[request.operation](request)
            )
        return unparsed_response(response)
