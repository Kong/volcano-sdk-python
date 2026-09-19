from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.call_mcp_body import CallMCPBody
from ...models.call_mcp_response_200 import CallMCPResponse200
from ...models.error import Error
from typing import cast



def _get_kwargs(
    *,
    body: CallMCPBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/mcp",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | CallMCPResponse200 | Error | None:
    if response.status_code == 200:
        response_200 = CallMCPResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 202:
        response_202 = cast(Any, None)
        return response_202

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 413:
        response_413 = cast(Any, None)
        return response_413

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | CallMCPResponse200 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CallMCPBody,

) -> Response[Any | CallMCPResponse200 | Error]:
    """ Model Context Protocol endpoint

     Streamable-HTTP MCP endpoint: one JSON-RPC 2.0 object per request, one
    response per request. There is no server-to-client stream, so a `GET`
    returns `405`, and a batched array is rejected.

    Authenticated with a **project access token**. The endpoint takes its
    project from the credential, so a platform token is refused with `403` —
    it names no project, and letting a tool argument choose one would hand an
    agent its own blast radius.

    Scope carries over from the REST API. A `read_only` token is not offered
    mutating tools or credential-returning reads, and is refused if it calls
    one anyway. Revoking the token ends MCP access on the same path it ends
    API access.

    Methods: `initialize`, `notifications/initialized`, `ping`,
    `tools/list`, `tools/call`. See the
    [MCP guide](https://docs.volcano.dev/platform/interfaces/mcp) for the
    tool surface and client configuration.

    Args:
        body (CallMCPBody): A JSON-RPC 2.0 request object.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CallMCPResponse200 | Error]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    body: CallMCPBody,

) -> Any | CallMCPResponse200 | Error | None:
    """ Model Context Protocol endpoint

     Streamable-HTTP MCP endpoint: one JSON-RPC 2.0 object per request, one
    response per request. There is no server-to-client stream, so a `GET`
    returns `405`, and a batched array is rejected.

    Authenticated with a **project access token**. The endpoint takes its
    project from the credential, so a platform token is refused with `403` —
    it names no project, and letting a tool argument choose one would hand an
    agent its own blast radius.

    Scope carries over from the REST API. A `read_only` token is not offered
    mutating tools or credential-returning reads, and is refused if it calls
    one anyway. Revoking the token ends MCP access on the same path it ends
    API access.

    Methods: `initialize`, `notifications/initialized`, `ping`,
    `tools/list`, `tools/call`. See the
    [MCP guide](https://docs.volcano.dev/platform/interfaces/mcp) for the
    tool surface and client configuration.

    Args:
        body (CallMCPBody): A JSON-RPC 2.0 request object.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CallMCPResponse200 | Error
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CallMCPBody,

) -> Response[Any | CallMCPResponse200 | Error]:
    """ Model Context Protocol endpoint

     Streamable-HTTP MCP endpoint: one JSON-RPC 2.0 object per request, one
    response per request. There is no server-to-client stream, so a `GET`
    returns `405`, and a batched array is rejected.

    Authenticated with a **project access token**. The endpoint takes its
    project from the credential, so a platform token is refused with `403` —
    it names no project, and letting a tool argument choose one would hand an
    agent its own blast radius.

    Scope carries over from the REST API. A `read_only` token is not offered
    mutating tools or credential-returning reads, and is refused if it calls
    one anyway. Revoking the token ends MCP access on the same path it ends
    API access.

    Methods: `initialize`, `notifications/initialized`, `ping`,
    `tools/list`, `tools/call`. See the
    [MCP guide](https://docs.volcano.dev/platform/interfaces/mcp) for the
    tool surface and client configuration.

    Args:
        body (CallMCPBody): A JSON-RPC 2.0 request object.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CallMCPResponse200 | Error]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CallMCPBody,

) -> Any | CallMCPResponse200 | Error | None:
    """ Model Context Protocol endpoint

     Streamable-HTTP MCP endpoint: one JSON-RPC 2.0 object per request, one
    response per request. There is no server-to-client stream, so a `GET`
    returns `405`, and a batched array is rejected.

    Authenticated with a **project access token**. The endpoint takes its
    project from the credential, so a platform token is refused with `403` —
    it names no project, and letting a tool argument choose one would hand an
    agent its own blast radius.

    Scope carries over from the REST API. A `read_only` token is not offered
    mutating tools or credential-returning reads, and is refused if it calls
    one anyway. Revoking the token ends MCP access on the same path it ends
    API access.

    Methods: `initialize`, `notifications/initialized`, `ping`,
    `tools/list`, `tools/call`. See the
    [MCP guide](https://docs.volcano.dev/platform/interfaces/mcp) for the
    tool surface and client configuration.

    Args:
        body (CallMCPBody): A JSON-RPC 2.0 request object.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CallMCPResponse200 | Error
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
