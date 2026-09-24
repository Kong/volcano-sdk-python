"""Generated execution operation adapters."""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
)
from uuid import UUID

from ._generated.api.durable_functions import (
    get_durable_execution,
    list_durable_executions,
    start_durable_execution_from_application,
    stop_durable_execution,
)
from ._generated.api.functions.invoke_function import (
    request_kwargs as invoke_function_kwargs,
)
from ._generated.api.functions.resolve_function_for_invocation import (
    request_kwargs as resolve_function_kwargs,
)
from ._generated.api.logs.get_project_log_activity import (
    build_response as build_log_activity_response,
)
from ._generated.api.logs.get_project_log_activity import (
    request_kwargs as log_activity_kwargs,
)
from ._generated.api.logs.search_project_logs import (
    build_response as build_log_search_response,
)
from ._generated.api.logs.search_project_logs import (
    request_kwargs as log_search_kwargs,
)
from ._generated.models.function_invocation_request import FunctionInvocationRequest
from ._generated.models.function_invocation_request_payload import (
    FunctionInvocationRequestPayload,
)
from ._generated.models.log_activity_request import LogActivityRequest
from ._generated.models.log_search_request import LogSearchRequest
from ._generated.types import UNSET
from ._log_response import (
    activity_total,
    response_data,
    response_values,
    search_metadata,
)
from ._transport_base import TransportBase
from ._transport_response import (
    generated_request,
    parsed_response,
    plain_json,
    unparsed_response,
)
from ._transport_types import (
    HTTP_OK,
    HTTP_UNAUTHORIZED,
    DurableExecutionListRequest,
    RawHTTPResponse,
    TransportResponse,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from .models import JSONValue


class ExecutionTransport(TransportBase):
    """Adapt generated execution operations to the SDK transport."""

    def resolve_function_for_invocation(
        self,
        *,
        authorization: str,
        name: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = generated_request(client, resolve_function_kwargs(name=name))
        return unparsed_response(response)

    def invoke_function(
        self,
        *,
        authorization: str,
        function_id: str,
        payload: Mapping[str, JSONValue],
    ) -> TransportResponse:
        plain_payload = plain_json(payload)
        body = FunctionInvocationRequest(
            payload=FunctionInvocationRequestPayload.from_dict(plain_payload)
        )
        with self._client(authorization) as client:
            response = generated_request(
                client,
                invoke_function_kwargs(
                    UUID(function_id),
                    body=body,
                ),
            )
        return unparsed_response(response)

    def invoke_function_url(
        self,
        *,
        authorization: str,
        invoke_url: str,
        payload: Mapping[str, JSONValue],
    ) -> TransportResponse:
        # The resolved endpoint is absolute and off the API host, so it cannot
        # go through the generated client's base URL. The body still uses the
        # invoke contract's { payload } envelope.
        plain_payload = plain_json(payload)
        with self._client(authorization) as client:
            response = client.get_httpx_client().post(
                invoke_url, json={"payload": plain_payload}
            )
        return unparsed_response(response)

    @staticmethod
    def _validate_log_response(
        response: RawHTTPResponse,
        metadata: Callable[[Mapping[str, object]], object],
    ) -> None:
        if response.status_code == HTTP_OK:
            payload = unparsed_response(response).payload
            values = response_values(payload)
            _ = response_data(values)
            _ = metadata(values)

    def search_project_logs(
        self,
        *,
        authorization: str,
        project_id: str,
        request: Mapping[str, JSONValue],
    ) -> TransportResponse:
        plain_request = plain_json(request)
        with self._client(authorization) as client:
            request_kwargs = log_search_kwargs(
                UUID(project_id), body=LogSearchRequest.from_dict(plain_request)
            )
            request_kwargs["json"] = plain_request
            raw_response = generated_request(client, request_kwargs)
            if raw_response.status_code == HTTP_UNAUTHORIZED:
                return unparsed_response(raw_response)
            self._validate_log_response(raw_response, search_metadata)
            response = build_log_search_response(
                client=client,
                response=raw_response,
            )
        return parsed_response(response)

    def get_project_log_activity(
        self,
        *,
        authorization: str,
        project_id: str,
        request: Mapping[str, JSONValue],
    ) -> TransportResponse:
        plain_request = plain_json(request)
        with self._client(authorization) as client:
            request_kwargs = log_activity_kwargs(
                UUID(project_id), body=LogActivityRequest.from_dict(plain_request)
            )
            request_kwargs["json"] = plain_request
            raw_response = generated_request(client, request_kwargs)
            if raw_response.status_code == HTTP_UNAUTHORIZED:
                return unparsed_response(raw_response)
            self._validate_log_response(raw_response, activity_total)
            response = build_log_activity_response(
                client=client,
                response=raw_response,
            )
        return parsed_response(response)

    def start_durable_execution_from_application(
        self,
        *,
        authorization: str,
        function_id: str,
        payload: JSONValue,
        execution_name: str | None = None,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = start_durable_execution_from_application.sync_detailed(
                function_id,
                client=client,
                body=plain_json(payload),
                x_volcano_execution_name=(
                    UNSET if execution_name is None else execution_name
                ),
            )
        return parsed_response(response)

    def get_durable_execution(
        self,
        *,
        authorization: str,
        project_id: str,
        function_id: str,
        execution_id: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = get_durable_execution.sync_detailed(
                UUID(project_id),
                function_id,
                UUID(execution_id),
                client=client,
            )
        return parsed_response(response)

    def list_durable_executions(
        self,
        *,
        authorization: str,
        project_id: str,
        function_id: str,
        request: DurableExecutionListRequest,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = list_durable_executions.sync_detailed(
                UUID(project_id),
                function_id,
                client=client,
                status=UNSET if request.status is None else request.status,
                page=UNSET if request.page is None else request.page,
                limit=UNSET if request.limit is None else request.limit,
            )
        return parsed_response(response)

    def stop_durable_execution(
        self,
        *,
        authorization: str,
        project_id: str,
        function_id: str,
        execution_id: str,
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = stop_durable_execution.sync_detailed(
                UUID(project_id),
                function_id,
                UUID(execution_id),
                client=client,
            )
        return parsed_response(response)
