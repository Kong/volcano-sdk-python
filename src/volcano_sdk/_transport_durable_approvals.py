"""Generated durable approval operation adapters."""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from ._generated.api.durable_functions import (
    approve_durable_approval,
    deny_durable_approval,
    get_durable_approval,
    get_durable_approval_stats,
    list_durable_approvals,
)
from ._generated.models.durable_approval_decision_request import (
    DurableApprovalDecisionRequest,
)
from ._generated.types import UNSET
from ._transport_base import TransportBase
from ._transport_response import parsed_response

if TYPE_CHECKING:
    from ._transport_types import (
        DurableApprovalListRequest,
        DurableApprovalStatsRequest,
        TransportResponse,
    )


def _decision_body(comment: str | None) -> DurableApprovalDecisionRequest:
    return DurableApprovalDecisionRequest(comment=UNSET if comment is None else comment)


class DurableApprovalTransport(TransportBase):
    """Adapt generated durable approval operations to the SDK transport."""

    def list_durable_approvals(
        self,
        *,
        authorization: str,
        project_id: str,
        request: DurableApprovalListRequest,
    ) -> TransportResponse:
        execution_id = request.execution_id
        with self._client(authorization) as client:
            response = list_durable_approvals.sync_detailed(
                UUID(project_id),
                client=client,
                page=UNSET if request.page is None else request.page,
                limit=UNSET if request.limit is None else request.limit,
                status=UNSET if request.status is None else request.status,
                function=UNSET if request.function is None else request.function,
                execution_id=UNSET if execution_id is None else UUID(execution_id),
                from_=UNSET if request.from_ is None else request.from_,
                to=UNSET if request.to is None else request.to,
            )
        return parsed_response(response)

    def get_durable_approval(
        self,
        *,
        authorization: str,
        project_id: str,
        approval_id: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = get_durable_approval.sync_detailed(
                UUID(project_id), UUID(approval_id), client=client
            )
        return parsed_response(response)

    def get_durable_approval_stats(
        self,
        *,
        authorization: str,
        project_id: str,
        request: DurableApprovalStatsRequest,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = get_durable_approval_stats.sync_detailed(
                UUID(project_id),
                client=client,
                function=UNSET if request.function is None else request.function,
                from_=UNSET if request.from_ is None else request.from_,
                to=UNSET if request.to is None else request.to,
            )
        return parsed_response(response)

    def approve_durable_approval(
        self,
        *,
        authorization: str,
        project_id: str,
        approval_id: str,
        comment: str | None,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = approve_durable_approval.sync_detailed(
                UUID(project_id),
                UUID(approval_id),
                client=client,
                body=_decision_body(comment),
            )
        return parsed_response(response)

    def deny_durable_approval(
        self,
        *,
        authorization: str,
        project_id: str,
        approval_id: str,
        comment: str | None,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = deny_durable_approval.sync_detailed(
                UUID(project_id),
                UUID(approval_id),
                client=client,
                body=_decision_body(comment),
            )
        return parsed_response(response)
