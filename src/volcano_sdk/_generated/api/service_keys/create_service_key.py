from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_service_key_body import CreateServiceKeyBody
from ...models.error import Error
from ...models.service_key import ServiceKey
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    *,
    body: CreateServiceKeyBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/service-keys".format(id=quote(str(id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ServiceKey | None:
    if response.status_code == 201:
        response_201 = ServiceKey.from_dict(response.json())



        return response_201

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ServiceKey]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateServiceKeyBody,

) -> Response[Error | ServiceKey]:
    """ Create service key

     Create a new service role key for admin operations.

    **WARNING:** Service keys bypass all RLS policies!
    Store securely and NEVER expose in frontend code.

    A key that holds `ai.invoke` is an AI key for the Volcano AI gateway,
    which calls models on the project's behalf. Volcano pays the model
    provider for those calls; the project is not billed for them. It holds `ai.invoke` and nothing else,
    and is marked as created
    by a person, so the gateway can tell it from every other key: a key
    that holds `"*"`, and a key created before AI keys existed, never
    count. Only a person creates one: signed in to the dashboard, or with
    a `volcano login` token whose sign-in is live. A project access token,
    a request made through MCP, a platform token created through the token
    API, and a sign-in that ended get `403` with code `person_required`.
    On a local server, the local platform token counts as the person.
    Reading or regenerating an AI key takes the same person as creating
    it, and lists leave its value out. An AI key only mints run tokens:
    the database API and realtime refuse it, whether or not service key
    scopes apply to them yet. While the `ai_gateway` capability
    is unavailable, asking for `ai.invoke` answers `404` with code
    `feature_unavailable`; existing keys keep working with the other
    service key routes.

    A key that holds `grants.mint` lets a first-party app, such as the
    Builder, mint delegated grants. It too holds that permission alone
    and takes a person, as an AI key does. Only a registered first-party
    app's project may hold one, and only its owner creates it: another
    project gets `403` with code
    `first_party_app_required`. The `ai_gateway` capability doesn't apply
    to it, and it carries no AI marker.

    Args:
        id (UUID):
        body (CreateServiceKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ServiceKey]
     """


    kwargs = request_kwargs(
        id=id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateServiceKeyBody,

) -> Error | ServiceKey | None:
    """ Create service key

     Create a new service role key for admin operations.

    **WARNING:** Service keys bypass all RLS policies!
    Store securely and NEVER expose in frontend code.

    A key that holds `ai.invoke` is an AI key for the Volcano AI gateway,
    which calls models on the project's behalf. Volcano pays the model
    provider for those calls; the project is not billed for them. It holds `ai.invoke` and nothing else,
    and is marked as created
    by a person, so the gateway can tell it from every other key: a key
    that holds `"*"`, and a key created before AI keys existed, never
    count. Only a person creates one: signed in to the dashboard, or with
    a `volcano login` token whose sign-in is live. A project access token,
    a request made through MCP, a platform token created through the token
    API, and a sign-in that ended get `403` with code `person_required`.
    On a local server, the local platform token counts as the person.
    Reading or regenerating an AI key takes the same person as creating
    it, and lists leave its value out. An AI key only mints run tokens:
    the database API and realtime refuse it, whether or not service key
    scopes apply to them yet. While the `ai_gateway` capability
    is unavailable, asking for `ai.invoke` answers `404` with code
    `feature_unavailable`; existing keys keep working with the other
    service key routes.

    A key that holds `grants.mint` lets a first-party app, such as the
    Builder, mint delegated grants. It too holds that permission alone
    and takes a person, as an AI key does. Only a registered first-party
    app's project may hold one, and only its owner creates it: another
    project gets `403` with code
    `first_party_app_required`. The `ai_gateway` capability doesn't apply
    to it, and it carries no AI marker.

    Args:
        id (UUID):
        body (CreateServiceKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ServiceKey
     """


    return sync_detailed(
        id=id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateServiceKeyBody,

) -> Response[Error | ServiceKey]:
    """ Create service key

     Create a new service role key for admin operations.

    **WARNING:** Service keys bypass all RLS policies!
    Store securely and NEVER expose in frontend code.

    A key that holds `ai.invoke` is an AI key for the Volcano AI gateway,
    which calls models on the project's behalf. Volcano pays the model
    provider for those calls; the project is not billed for them. It holds `ai.invoke` and nothing else,
    and is marked as created
    by a person, so the gateway can tell it from every other key: a key
    that holds `"*"`, and a key created before AI keys existed, never
    count. Only a person creates one: signed in to the dashboard, or with
    a `volcano login` token whose sign-in is live. A project access token,
    a request made through MCP, a platform token created through the token
    API, and a sign-in that ended get `403` with code `person_required`.
    On a local server, the local platform token counts as the person.
    Reading or regenerating an AI key takes the same person as creating
    it, and lists leave its value out. An AI key only mints run tokens:
    the database API and realtime refuse it, whether or not service key
    scopes apply to them yet. While the `ai_gateway` capability
    is unavailable, asking for `ai.invoke` answers `404` with code
    `feature_unavailable`; existing keys keep working with the other
    service key routes.

    A key that holds `grants.mint` lets a first-party app, such as the
    Builder, mint delegated grants. It too holds that permission alone
    and takes a person, as an AI key does. Only a registered first-party
    app's project may hold one, and only its owner creates it: another
    project gets `403` with code
    `first_party_app_required`. The `ai_gateway` capability doesn't apply
    to it, and it carries no AI marker.

    Args:
        id (UUID):
        body (CreateServiceKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ServiceKey]
     """


    kwargs = request_kwargs(
        id=id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateServiceKeyBody,

) -> Error | ServiceKey | None:
    """ Create service key

     Create a new service role key for admin operations.

    **WARNING:** Service keys bypass all RLS policies!
    Store securely and NEVER expose in frontend code.

    A key that holds `ai.invoke` is an AI key for the Volcano AI gateway,
    which calls models on the project's behalf. Volcano pays the model
    provider for those calls; the project is not billed for them. It holds `ai.invoke` and nothing else,
    and is marked as created
    by a person, so the gateway can tell it from every other key: a key
    that holds `"*"`, and a key created before AI keys existed, never
    count. Only a person creates one: signed in to the dashboard, or with
    a `volcano login` token whose sign-in is live. A project access token,
    a request made through MCP, a platform token created through the token
    API, and a sign-in that ended get `403` with code `person_required`.
    On a local server, the local platform token counts as the person.
    Reading or regenerating an AI key takes the same person as creating
    it, and lists leave its value out. An AI key only mints run tokens:
    the database API and realtime refuse it, whether or not service key
    scopes apply to them yet. While the `ai_gateway` capability
    is unavailable, asking for `ai.invoke` answers `404` with code
    `feature_unavailable`; existing keys keep working with the other
    service key routes.

    A key that holds `grants.mint` lets a first-party app, such as the
    Builder, mint delegated grants. It too holds that permission alone
    and takes a person, as an AI key does. Only a registered first-party
    app's project may hold one, and only its owner creates it: another
    project gets `403` with code
    `first_party_app_required`. The `ai_gateway` capability doesn't apply
    to it, and it carries no AI marker.

    Args:
        id (UUID):
        body (CreateServiceKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ServiceKey
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,

    )).parsed
