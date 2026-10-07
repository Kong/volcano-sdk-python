"""Custom Sandbox image deployment operations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Unpack, cast

from ._sandbox import SandboxRequests, identifier, integer, record, request_id, text
from ._transport_sandbox import SandboxRequest
from .errors import ValidationError
from .sandbox_deployment_models import (
    SandboxBuildLog,
    SandboxBuildLogPage,
    SandboxDeployment,
    SandboxDeploymentPage,
)

if TYPE_CHECKING:
    from .models import JSONValue
    from .sandbox_deployment_models import SandboxBuildLogOptions, SandboxDeployOptions

_MAX_SOURCE = 32 * 1024 * 1024
_MAX_PORT = 65535


class SandboxDeployments:
    """Manage immutable custom-image deployments through the public facade."""

    def __init__(self, requests: SandboxRequests) -> None:
        """Bind the credential-aware request scope."""
        self._requests: SandboxRequests = requests

    def deploy(
        self,
        project_id: str,
        sandbox_id: str,
        source: bytes,
        **options: Unpack[SandboxDeployOptions],
    ) -> SandboxDeployment:
        """Upload a source archive; retain both IDs and source for retries.

        Returns:
            The accepted deployment and its build status.

        """
        _validate_source(source, options.get("ports", []))
        body: dict[str, JSONValue] = {
            "name": options["name"],
            "memory_mb": options.get("memory_mb", 1024),
            "ports": tuple(options.get("ports", [])),
        }
        request = SandboxRequest(
            "deploy_sandbox",
            identifier(project_id),
            identifier(sandbox_id),
            body=body,
            request_id=request_id(options),
            archive=source,
        )
        return _deployment(self._requests.management().send(request, 202))

    def deployments(
        self, project_id: str, sandbox_id: str, *, cursor: str | None = None
    ) -> SandboxDeploymentPage:
        """Read one deployment history page.

        Returns:
            Deployments and continuation information.

        Raises:
            TypeError: If the response pagination is malformed.

        """
        request = SandboxRequest(
            "list_sandbox_deployments",
            identifier(project_id),
            identifier(sandbox_id),
            cursor=cursor,
        )
        data = record(self._requests.management().send(request))
        pagination = record(data.get("pagination"))
        more = pagination.get("has_more")
        if not isinstance(more, bool):
            message = "Invalid Sandbox pagination"
            raise TypeError(message)
        return SandboxDeploymentPage(
            tuple(_deployment(row) for row in _rows(data.get("data"))),
            integer(pagination.get("limit")),
            more,
            _optional_text(pagination.get("next_cursor")),
        )

    def deployment(
        self, project_id: str, sandbox_id: str, deployment_id: str
    ) -> SandboxDeployment:
        """Read the current build and validation status.

        Returns:
            The deployment snapshot.

        """
        return _deployment(
            self._requests.management().send(
                _request(
                    "get_sandbox_deployment", project_id, sandbox_id, deployment_id
                )
            )
        )

    def source(self, project_id: str, sandbox_id: str, deployment_id: str) -> bytes:
        """Download the exact original source archive.

        Returns:
            The compressed tar archive bytes.

        Raises:
            TypeError: If the response is not a binary archive.

        """
        data = self._requests.management().send(
            _request(
                "get_sandbox_deployment_source", project_id, sandbox_id, deployment_id
            )
        )
        if not isinstance(data, bytes):
            message = "Invalid Sandbox source archive"
            raise TypeError(message)
        return data

    def logs(
        self,
        project_id: str,
        sandbox_id: str,
        deployment_id: str,
        **options: Unpack[SandboxBuildLogOptions],
    ) -> SandboxBuildLogPage:
        """Read regional build output.

        Returns:
            Build messages and an optional continuation cursor.

        """
        request = SandboxRequest(
            "get_sandbox_deployment_logs",
            identifier(project_id),
            identifier(sandbox_id),
            deployment_id=identifier(deployment_id),
            region=options["region"],
            cursor=options.get("cursor"),
            limit=options.get("limit", 100),
        )
        data = record(self._requests.management().send(request))
        return SandboxBuildLogPage(
            tuple(_log(row) for row in _rows(data.get("data"))),
            _optional_text(data.get("next_cursor")),
        )

    def delete_template(self, project_id: str, sandbox_id: str) -> None:
        """Delete a template and terminate its sessions."""
        _ = self._requests.management().send(
            SandboxRequest(
                "delete_sandbox", identifier(project_id), identifier(sandbox_id)
            ),
            202,
        )


def _request(
    operation: str, project: str, template: str, deployment: str
) -> SandboxRequest:
    return SandboxRequest(
        operation,
        identifier(project),
        identifier(template),
        deployment_id=identifier(deployment),
    )


def _deployment(value: object) -> SandboxDeployment:
    data = record(value)
    return SandboxDeployment(
        text(data.get("id")),
        text(data.get("status")),
        text(data.get("created_at")),
        text(data.get("updated_at")),
    )


def _log(value: object) -> SandboxBuildLog:
    data = record(value)
    return SandboxBuildLog(text(data.get("timestamp")), text(data.get("message")))


def _optional_text(value: object) -> str | None:
    return None if value is None else text(value)


def _rows(value: object) -> list[object]:
    if not isinstance(value, list):
        message = "Invalid Sandbox list"
        raise TypeError(message)
    return cast("list[object]", value)


def _validate_source(source: bytes, ports: list[int]) -> None:
    if len(source) > _MAX_SOURCE:
        message = "Sandbox source archives are limited to 32 MiB"
        raise ValidationError(message)
    for port in ports:
        if isinstance(port, bool) or not 1 <= port <= _MAX_PORT:
            message = "Sandbox ports must be between 1 and 65535"
            raise ValidationError(message)
