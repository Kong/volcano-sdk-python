"""Generated database operation adapters."""

from __future__ import annotations

from ._generated.api.database_queries import (
    query_database_select,
)
from ._generated.api.database_queries.query_database_delete import (
    build_response as build_database_delete_response,
)
from ._generated.api.database_queries.query_database_delete import (
    request_kwargs as database_delete_kwargs,
)
from ._generated.api.database_queries.query_database_insert import (
    build_response as build_database_insert_response,
)
from ._generated.api.database_queries.query_database_insert import (
    request_kwargs as database_insert_kwargs,
)
from ._generated.api.database_queries.query_database_select import (
    build_response as build_database_select_response,
)
from ._generated.api.database_queries.query_database_select import (
    request_kwargs as database_select_kwargs,
)
from ._generated.api.database_queries.query_database_update import (
    build_response as build_database_update_response,
)
from ._generated.api.database_queries.query_database_update import (
    request_kwargs as database_update_kwargs,
)
from ._generated.models.database_delete_request import DatabaseDeleteRequest
from ._generated.models.database_insert_request import DatabaseInsertRequest
from ._generated.models.database_select_request import DatabaseSelectRequest
from ._generated.models.database_update_request import DatabaseUpdateRequest
from ._transport_base import TransportBase
from ._transport_response import (
    generated_request,
    parsed_response,
    unparsed_response,
)
from ._transport_types import (
    HTTP_UNAUTHORIZED,
    TransportResponse,
)


class DatabaseTransport(TransportBase):
    """Adapt generated database operations to the SDK transport."""

    def query_database_select(
        self,
        *,
        authorization: str,
        database_name: str,
        body: dict[str, object],
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = generated_request(
                client,
                database_select_kwargs(
                    database_name,
                    body=DatabaseSelectRequest.from_dict(body),
                ),
            )
            if response.status_code == HTTP_UNAUTHORIZED:
                return unparsed_response(response)
            parsed = build_database_select_response(client=client, response=response)
        return parsed_response(parsed)

    async def query_database_select_async(
        self,
        *,
        authorization: str,
        database_name: str,
        body: dict[str, object],
    ) -> TransportResponse:
        async with self._client(authorization) as client:
            response = await query_database_select.asyncio_detailed(
                database_name,
                client=client,
                body=DatabaseSelectRequest.from_dict(body),
            )
        return parsed_response(response)

    def query_database_insert(
        self,
        *,
        authorization: str,
        database_name: str,
        body: dict[str, object],
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = generated_request(
                client,
                database_insert_kwargs(
                    database_name, body=DatabaseInsertRequest.from_dict(body)
                ),
            )
            if response.status_code == HTTP_UNAUTHORIZED:
                return unparsed_response(response)
            parsed = build_database_insert_response(client=client, response=response)
        return parsed_response(parsed)

    def query_database_update(
        self,
        *,
        authorization: str,
        database_name: str,
        body: dict[str, object],
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = generated_request(
                client,
                database_update_kwargs(
                    database_name, body=DatabaseUpdateRequest.from_dict(body)
                ),
            )
            if response.status_code == HTTP_UNAUTHORIZED:
                return unparsed_response(response)
            parsed = build_database_update_response(client=client, response=response)
        return parsed_response(parsed)

    def query_database_delete(
        self,
        *,
        authorization: str,
        database_name: str,
        body: dict[str, object],
    ) -> TransportResponse:
        with self._client(authorization) as client:
            response = generated_request(
                client,
                database_delete_kwargs(
                    database_name, body=DatabaseDeleteRequest.from_dict(body)
                ),
            )
            if response.status_code == HTTP_UNAUTHORIZED:
                return unparsed_response(response)
            parsed = build_database_delete_response(client=client, response=response)
        return parsed_response(parsed)
