from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.durable_execution import DurableExecution
from ...models.error import Error
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    function_id: str,
    *,
    body: Any | Unset = UNSET,
    x_volcano_execution_name: str | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_volcano_execution_name, Unset):
        headers["X-Volcano-Execution-Name"] = x_volcano_execution_name



    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/durable-functions/{function_id}/executions".format(function_id=quote(str(function_id), safe=""),),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DurableExecution | Error | None:
    if response.status_code == 202:
        response_202 = DurableExecution.from_dict(response.json())



        return response_202

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

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())



        return response_413

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DurableExecution | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    function_id: str,
    *,
    client: AuthenticatedClient,
    body: Any | Unset = UNSET,
    x_volcano_execution_name: str | Unset = UNSET,

) -> Response[DurableExecution | Error]:
    """ Start a durable execution from an application

     Starts an execution of a durable function using an application
    credential, and returns its handle.

    This is the durable counterpart of `POST /functions/{functionId}/invoke`,
    and it is the endpoint an application calls. Like that one, it is not
    project-scoped: an anon key, a service key and an auth user token each
    carry their own project. The project-scoped collection under
    `/projects/{id}/durable-functions/...` remains the owner's management
    surface.

    **With a service key or an auth user token:** any durable function in
    the project.

    **With an anon key:** requires the `functions.invoke` permission, and
    the function must have `is_public: true`.

    Starting is all this endpoint does. Reading a result or stopping an
    execution requires the project owner's token, because an anon key is
    shared by everyone who loads the page and an execution is addressed by
    id alone.

    Send `X-Volcano-Execution-Name` to make the start idempotent: repeating
    a start with the same name returns the existing execution instead of
    beginning a second one.

    Each execution counts once against the project's durable execution
    allowance, however many times the start is retried under the same
    execution name, and the number in flight at once is capped by the plan.
    The operations the execution performs are counted against the durable
    operations allowance when it finishes.

    Args:
        function_id (str):
        x_volcano_execution_name (str | Unset):
        body (Any | Unset): Input passed to the function, up to 256 KiB.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableExecution | Error]
     """


    kwargs = _get_kwargs(
        function_id=function_id,
body=body,
x_volcano_execution_name=x_volcano_execution_name,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    function_id: str,
    *,
    client: AuthenticatedClient,
    body: Any | Unset = UNSET,
    x_volcano_execution_name: str | Unset = UNSET,

) -> DurableExecution | Error | None:
    """ Start a durable execution from an application

     Starts an execution of a durable function using an application
    credential, and returns its handle.

    This is the durable counterpart of `POST /functions/{functionId}/invoke`,
    and it is the endpoint an application calls. Like that one, it is not
    project-scoped: an anon key, a service key and an auth user token each
    carry their own project. The project-scoped collection under
    `/projects/{id}/durable-functions/...` remains the owner's management
    surface.

    **With a service key or an auth user token:** any durable function in
    the project.

    **With an anon key:** requires the `functions.invoke` permission, and
    the function must have `is_public: true`.

    Starting is all this endpoint does. Reading a result or stopping an
    execution requires the project owner's token, because an anon key is
    shared by everyone who loads the page and an execution is addressed by
    id alone.

    Send `X-Volcano-Execution-Name` to make the start idempotent: repeating
    a start with the same name returns the existing execution instead of
    beginning a second one.

    Each execution counts once against the project's durable execution
    allowance, however many times the start is retried under the same
    execution name, and the number in flight at once is capped by the plan.
    The operations the execution performs are counted against the durable
    operations allowance when it finishes.

    Args:
        function_id (str):
        x_volcano_execution_name (str | Unset):
        body (Any | Unset): Input passed to the function, up to 256 KiB.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableExecution | Error
     """


    return sync_detailed(
        function_id=function_id,
client=client,
body=body,
x_volcano_execution_name=x_volcano_execution_name,

    ).parsed

async def asyncio_detailed(
    function_id: str,
    *,
    client: AuthenticatedClient,
    body: Any | Unset = UNSET,
    x_volcano_execution_name: str | Unset = UNSET,

) -> Response[DurableExecution | Error]:
    """ Start a durable execution from an application

     Starts an execution of a durable function using an application
    credential, and returns its handle.

    This is the durable counterpart of `POST /functions/{functionId}/invoke`,
    and it is the endpoint an application calls. Like that one, it is not
    project-scoped: an anon key, a service key and an auth user token each
    carry their own project. The project-scoped collection under
    `/projects/{id}/durable-functions/...` remains the owner's management
    surface.

    **With a service key or an auth user token:** any durable function in
    the project.

    **With an anon key:** requires the `functions.invoke` permission, and
    the function must have `is_public: true`.

    Starting is all this endpoint does. Reading a result or stopping an
    execution requires the project owner's token, because an anon key is
    shared by everyone who loads the page and an execution is addressed by
    id alone.

    Send `X-Volcano-Execution-Name` to make the start idempotent: repeating
    a start with the same name returns the existing execution instead of
    beginning a second one.

    Each execution counts once against the project's durable execution
    allowance, however many times the start is retried under the same
    execution name, and the number in flight at once is capped by the plan.
    The operations the execution performs are counted against the durable
    operations allowance when it finishes.

    Args:
        function_id (str):
        x_volcano_execution_name (str | Unset):
        body (Any | Unset): Input passed to the function, up to 256 KiB.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableExecution | Error]
     """


    kwargs = _get_kwargs(
        function_id=function_id,
body=body,
x_volcano_execution_name=x_volcano_execution_name,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    function_id: str,
    *,
    client: AuthenticatedClient,
    body: Any | Unset = UNSET,
    x_volcano_execution_name: str | Unset = UNSET,

) -> DurableExecution | Error | None:
    """ Start a durable execution from an application

     Starts an execution of a durable function using an application
    credential, and returns its handle.

    This is the durable counterpart of `POST /functions/{functionId}/invoke`,
    and it is the endpoint an application calls. Like that one, it is not
    project-scoped: an anon key, a service key and an auth user token each
    carry their own project. The project-scoped collection under
    `/projects/{id}/durable-functions/...` remains the owner's management
    surface.

    **With a service key or an auth user token:** any durable function in
    the project.

    **With an anon key:** requires the `functions.invoke` permission, and
    the function must have `is_public: true`.

    Starting is all this endpoint does. Reading a result or stopping an
    execution requires the project owner's token, because an anon key is
    shared by everyone who loads the page and an execution is addressed by
    id alone.

    Send `X-Volcano-Execution-Name` to make the start idempotent: repeating
    a start with the same name returns the existing execution instead of
    beginning a second one.

    Each execution counts once against the project's durable execution
    allowance, however many times the start is retried under the same
    execution name, and the number in flight at once is capped by the plan.
    The operations the execution performs are counted against the durable
    operations allowance when it finishes.

    Args:
        function_id (str):
        x_volcano_execution_name (str | Unset):
        body (Any | Unset): Input passed to the function, up to 256 KiB.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableExecution | Error
     """


    return (await asyncio_detailed(
        function_id=function_id,
client=client,
body=body,
x_volcano_execution_name=x_volcano_execution_name,

    )).parsed
