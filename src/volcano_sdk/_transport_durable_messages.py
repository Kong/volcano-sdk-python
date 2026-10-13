"""Generated durable message operation adapters."""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from ._generated.api.durable_functions import (
    list_durable_messages,
    list_durable_messages_from_application,
    send_durable_message,
    send_durable_message_from_application,
)
from ._generated.models.send_durable_message_request import SendDurableMessageRequest
from ._generated.types import UNSET, Unset
from ._transport_base import TransportBase
from ._transport_response import parsed_response

if TYPE_CHECKING:
    from ._generated.client import AuthenticatedClient
    from ._generated.models.durable_message_list import DurableMessageList
    from ._generated.models.error import Error
    from ._generated.types import Response
    from ._transport_types import (
        DurableMessageListRequest,
        DurableMessageSendRequest,
        DurableMessageTarget,
        TransportResponse,
    )
    from .models import DurableMessageDirection


def _unset(value: str | None) -> str | Unset:
    return UNSET if value is None else value


def _direction(
    value: DurableMessageDirection | None,
) -> DurableMessageDirection | Unset:
    return UNSET if value is None else value


def _count(value: int | None) -> int | Unset:
    return UNSET if value is None else value


class DurableMessageTransport(TransportBase):
    """Adapt generated durable message operations to the SDK transport.

    A target with a project id goes to the project route, with the owner's
    credential; one without goes to the application route.
    """

    def send_durable_message(
        self,
        *,
        authorization: str,
        target: DurableMessageTarget,
        request: DurableMessageSendRequest,
    ) -> TransportResponse:
        body = SendDurableMessageRequest(name=request.name, data=request.data)
        key = _unset(request.idempotency_key)
        execution_id = UUID(target.execution_id)
        with self._client(authorization) as client:
            if target.project_id is None:
                response = send_durable_message_from_application.sync_detailed(
                    target.function_id,
                    execution_id,
                    client=client,
                    body=body,
                    idempotency_key=key,
                    x_volcano_client_token=_unset(target.client_token),
                )
            else:
                response = send_durable_message.sync_detailed(
                    UUID(target.project_id),
                    target.function_id,
                    execution_id,
                    client=client,
                    body=body,
                    idempotency_key=key,
                )
        return parsed_response(response)

    def list_durable_messages(
        self,
        *,
        authorization: str,
        target: DurableMessageTarget,
        request: DurableMessageListRequest,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            if target.project_id is None:
                response = list_durable_messages_from_application.sync_detailed(
                    target.function_id,
                    UUID(target.execution_id),
                    client=client,
                    direction=_direction(request.direction),
                    name=_unset(request.name),
                    after=_count(request.after),
                    limit=_count(request.limit),
                    x_volcano_client_token=_unset(target.client_token),
                )
            else:
                response = list_durable_messages.sync_detailed(
                    UUID(target.project_id),
                    target.function_id,
                    UUID(target.execution_id),
                    client=client,
                    direction=_direction(request.direction),
                    name=_unset(request.name),
                    after=_count(request.after),
                    limit=_count(request.limit),
                )
        return parsed_response(response)

    async def list_durable_messages_async(
        self,
        *,
        authorization: str,
        target: DurableMessageTarget,
        request: DurableMessageListRequest,
    ) -> TransportResponse:
        async with self._client(authorization) as client:
            response = await _list_async(client, target, request)
        return parsed_response(response)


async def _list_async(
    client: AuthenticatedClient,
    target: DurableMessageTarget,
    request: DurableMessageListRequest,
) -> Response[DurableMessageList | Error]:
    if target.project_id is None:
        return await list_durable_messages_from_application.asyncio_detailed(
            target.function_id,
            UUID(target.execution_id),
            client=client,
            direction=_direction(request.direction),
            name=_unset(request.name),
            after=_count(request.after),
            limit=_count(request.limit),
            x_volcano_client_token=_unset(target.client_token),
        )
    return await list_durable_messages.asyncio_detailed(
        UUID(target.project_id),
        target.function_id,
        UUID(target.execution_id),
        client=client,
        direction=_direction(request.direction),
        name=_unset(request.name),
        after=_count(request.after),
        limit=_count(request.limit),
    )
