"""Generated locks operation adapters."""

from __future__ import annotations

from uuid import uuid4

from ._generated.api.locks import (
    force_release_project_lock,
    get_project_lock,
    release_project_lock,
    renew_project_lock,
)
from ._generated.api.locks.acquire_project_lock import (
    build_response as build_lock_acquire_response,
)
from ._generated.api.locks.acquire_project_lock import (
    request_kwargs as lock_acquire_kwargs,
)
from ._generated.models.project_lock_lease_request import ProjectLockLeaseRequest
from ._transport_base import TransportBase
from ._transport_response import (
    generated_request,
    parsed_response,
    unparsed_response,
)
from ._transport_types import (
    HTTP_CREATED,
    TransportResponse,
)


class LocksTransport(TransportBase):
    """Adapt generated locks operations to the SDK transport."""

    def acquire_project_lock(
        self,
        *,
        authorization: str,
        key: str,
        ttl: int,
        token: str,
        request_id: str | None = None,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            request_kwargs = lock_acquire_kwargs(
                key,
                body=ProjectLockLeaseRequest(ttl_seconds=ttl),
                x_volcano_lock_token=token,
                x_volcano_request_id=request_id or str(uuid4()),
            )
            raw_response = generated_request(client, request_kwargs)
            if raw_response.status_code != HTTP_CREATED:
                return unparsed_response(raw_response)
            response = build_lock_acquire_response(client=client, response=raw_response)
        return parsed_response(response)

    def get_project_lock(
        self,
        *,
        authorization: str,
        key: str,
        request_id: str | None = None,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = get_project_lock.sync_detailed(
                key,
                client=client,
                x_volcano_request_id=request_id or str(uuid4()),
            )
        return parsed_response(response)

    def force_release_project_lock(
        self,
        *,
        authorization: str,
        key: str,
        request_id: str | None = None,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = force_release_project_lock.sync_detailed(
                key,
                client=client,
                x_volcano_request_id=request_id or str(uuid4()),
            )
        return parsed_response(response)

    def renew_project_lock(
        self,
        *,
        authorization: str,
        key: str,
        ttl: int,
        token: str,
        request_id: str | None = None,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = renew_project_lock.sync_detailed(
                key,
                client=client,
                body=ProjectLockLeaseRequest(ttl_seconds=ttl),
                x_volcano_lock_token=token,
                x_volcano_request_id=request_id or str(uuid4()),
            )
        return parsed_response(response)

    def release_project_lock(
        self,
        *,
        authorization: str,
        key: str,
        token: str,
        request_id: str | None = None,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = release_project_lock.sync_detailed(
                key,
                client=client,
                x_volcano_lock_token=token,
                x_volcano_request_id=request_id or str(uuid4()),
            )
        return parsed_response(response)
