from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_email_template_request import CreateEmailTemplateRequest
from ...models.email_template import EmailTemplate
from ...models.error import Error
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    body: CreateEmailTemplateRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/email-templates".format(id=quote(str(id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> EmailTemplate | Error | None:
    if response.status_code == 201:
        response_201 = EmailTemplate.from_dict(response.json())



        return response_201

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[EmailTemplate | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: CreateEmailTemplateRequest,

) -> Response[EmailTemplate | Error]:
    """ Create email template

     Creates a custom email template for the project. Custom email templates
    are a PRO-plan feature: requests from a FREE-plan project owner are
    rejected with 403, and FREE projects always send the built-in default
    templates regardless of any previously saved custom rows.
    Every project is created with one template per type, so customizing one
    is usually a PUT; creating a type the project already has returns 409.
    Valid template types: welcome, confirmation, password_reset, password_changed

    Args:
        id (UUID):
        body (CreateEmailTemplateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EmailTemplate | Error]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: CreateEmailTemplateRequest,

) -> EmailTemplate | Error | None:
    """ Create email template

     Creates a custom email template for the project. Custom email templates
    are a PRO-plan feature: requests from a FREE-plan project owner are
    rejected with 403, and FREE projects always send the built-in default
    templates regardless of any previously saved custom rows.
    Every project is created with one template per type, so customizing one
    is usually a PUT; creating a type the project already has returns 409.
    Valid template types: welcome, confirmation, password_reset, password_changed

    Args:
        id (UUID):
        body (CreateEmailTemplateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EmailTemplate | Error
     """


    return sync_detailed(
        id=id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: CreateEmailTemplateRequest,

) -> Response[EmailTemplate | Error]:
    """ Create email template

     Creates a custom email template for the project. Custom email templates
    are a PRO-plan feature: requests from a FREE-plan project owner are
    rejected with 403, and FREE projects always send the built-in default
    templates regardless of any previously saved custom rows.
    Every project is created with one template per type, so customizing one
    is usually a PUT; creating a type the project already has returns 409.
    Valid template types: welcome, confirmation, password_reset, password_changed

    Args:
        id (UUID):
        body (CreateEmailTemplateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EmailTemplate | Error]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: CreateEmailTemplateRequest,

) -> EmailTemplate | Error | None:
    """ Create email template

     Creates a custom email template for the project. Custom email templates
    are a PRO-plan feature: requests from a FREE-plan project owner are
    rejected with 403, and FREE projects always send the built-in default
    templates regardless of any previously saved custom rows.
    Every project is created with one template per type, so customizing one
    is usually a PUT; creating a type the project already has returns 409.
    Valid template types: welcome, confirmation, password_reset, password_changed

    Args:
        id (UUID):
        body (CreateEmailTemplateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EmailTemplate | Error
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,

    )).parsed
