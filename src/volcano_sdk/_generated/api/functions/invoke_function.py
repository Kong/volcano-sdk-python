from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.function_invocation_request import FunctionInvocationRequest
from ...models.function_invocation_response import FunctionInvocationResponse
from typing import cast
from uuid import UUID



def _get_kwargs(
    function_id: UUID,
    *,
    body: FunctionInvocationRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/functions/{function_id}/invoke".format(function_id=quote(str(function_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | FunctionInvocationResponse:
    if response.status_code == 200:
        response_200 = FunctionInvocationResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    response_default = FunctionInvocationResponse.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | FunctionInvocationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    function_id: UUID,
    *,
    client: AuthenticatedClient,
    body: FunctionInvocationRequest,

) -> Response[Error | FunctionInvocationResponse]:
    r""" Invoke a function

     Invoke a serverless function.

    **With Service Key** (admin/background operations):
    - Use for background jobs, webhooks, cron, admin operations
    - Function receives payload only (no user context)
    - Database queries bypass RLS (admin access)

    **With Auth User Token** (user-facing):
    - Use for user-initiated actions
    - Function receives payload + `__volcano_auth` context:
      ```javascript
      {
        user_id: \"uuid\",
        email: \"user@example.com\",
        project_id: \"uuid\",
        role: \"authenticated\" or \"anonymous\"
      }
      ```
    - Database queries enforce RLS (user-scoped data)

    **With Anon Key** (public function only):
    - Requires anon key permission: `functions.invoke`
    - Function must have `is_public: true`
    - Function receives payload only (no `__volcano_auth`)

    **Transport and CORS:**
    - Direct invocation endpoint is intended for `http://api.<domain>/functions/{functionId}/invoke`
    - DNS invocation endpoint is `https://{functionId}.functions.<domain>/`
    - CORS preflight for invocation allows only `POST, OPTIONS`

    Args:
        function_id (UUID):
        body (FunctionInvocationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FunctionInvocationResponse]
     """


    kwargs = _get_kwargs(
        function_id=function_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    function_id: UUID,
    *,
    client: AuthenticatedClient,
    body: FunctionInvocationRequest,

) -> Error | FunctionInvocationResponse | None:
    r""" Invoke a function

     Invoke a serverless function.

    **With Service Key** (admin/background operations):
    - Use for background jobs, webhooks, cron, admin operations
    - Function receives payload only (no user context)
    - Database queries bypass RLS (admin access)

    **With Auth User Token** (user-facing):
    - Use for user-initiated actions
    - Function receives payload + `__volcano_auth` context:
      ```javascript
      {
        user_id: \"uuid\",
        email: \"user@example.com\",
        project_id: \"uuid\",
        role: \"authenticated\" or \"anonymous\"
      }
      ```
    - Database queries enforce RLS (user-scoped data)

    **With Anon Key** (public function only):
    - Requires anon key permission: `functions.invoke`
    - Function must have `is_public: true`
    - Function receives payload only (no `__volcano_auth`)

    **Transport and CORS:**
    - Direct invocation endpoint is intended for `http://api.<domain>/functions/{functionId}/invoke`
    - DNS invocation endpoint is `https://{functionId}.functions.<domain>/`
    - CORS preflight for invocation allows only `POST, OPTIONS`

    Args:
        function_id (UUID):
        body (FunctionInvocationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FunctionInvocationResponse
     """


    return sync_detailed(
        function_id=function_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    function_id: UUID,
    *,
    client: AuthenticatedClient,
    body: FunctionInvocationRequest,

) -> Response[Error | FunctionInvocationResponse]:
    r""" Invoke a function

     Invoke a serverless function.

    **With Service Key** (admin/background operations):
    - Use for background jobs, webhooks, cron, admin operations
    - Function receives payload only (no user context)
    - Database queries bypass RLS (admin access)

    **With Auth User Token** (user-facing):
    - Use for user-initiated actions
    - Function receives payload + `__volcano_auth` context:
      ```javascript
      {
        user_id: \"uuid\",
        email: \"user@example.com\",
        project_id: \"uuid\",
        role: \"authenticated\" or \"anonymous\"
      }
      ```
    - Database queries enforce RLS (user-scoped data)

    **With Anon Key** (public function only):
    - Requires anon key permission: `functions.invoke`
    - Function must have `is_public: true`
    - Function receives payload only (no `__volcano_auth`)

    **Transport and CORS:**
    - Direct invocation endpoint is intended for `http://api.<domain>/functions/{functionId}/invoke`
    - DNS invocation endpoint is `https://{functionId}.functions.<domain>/`
    - CORS preflight for invocation allows only `POST, OPTIONS`

    Args:
        function_id (UUID):
        body (FunctionInvocationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FunctionInvocationResponse]
     """


    kwargs = _get_kwargs(
        function_id=function_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    function_id: UUID,
    *,
    client: AuthenticatedClient,
    body: FunctionInvocationRequest,

) -> Error | FunctionInvocationResponse | None:
    r""" Invoke a function

     Invoke a serverless function.

    **With Service Key** (admin/background operations):
    - Use for background jobs, webhooks, cron, admin operations
    - Function receives payload only (no user context)
    - Database queries bypass RLS (admin access)

    **With Auth User Token** (user-facing):
    - Use for user-initiated actions
    - Function receives payload + `__volcano_auth` context:
      ```javascript
      {
        user_id: \"uuid\",
        email: \"user@example.com\",
        project_id: \"uuid\",
        role: \"authenticated\" or \"anonymous\"
      }
      ```
    - Database queries enforce RLS (user-scoped data)

    **With Anon Key** (public function only):
    - Requires anon key permission: `functions.invoke`
    - Function must have `is_public: true`
    - Function receives payload only (no `__volcano_auth`)

    **Transport and CORS:**
    - Direct invocation endpoint is intended for `http://api.<domain>/functions/{functionId}/invoke`
    - DNS invocation endpoint is `https://{functionId}.functions.<domain>/`
    - CORS preflight for invocation allows only `POST, OPTIONS`

    Args:
        function_id (UUID):
        body (FunctionInvocationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FunctionInvocationResponse
     """


    return (await asyncio_detailed(
        function_id=function_id,
client=client,
body=body,

    )).parsed
