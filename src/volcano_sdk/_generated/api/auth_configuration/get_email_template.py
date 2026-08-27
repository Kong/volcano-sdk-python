from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.email_template import EmailTemplate
from ...models.get_email_template_type import check_get_email_template_type
from ...models.get_email_template_type import GetEmailTemplateType
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    type_: GetEmailTemplateType,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/email-templates/{type_}".format(id=quote(str(id), safe=""),type_=quote(str(type_), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | EmailTemplate | None:
    if response.status_code == 200:
        response_200 = EmailTemplate.from_dict(response.json())



        return response_200

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | EmailTemplate]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    type_: GetEmailTemplateType,
    *,
    client: AuthenticatedClient,

) -> Response[Any | EmailTemplate]:
    """ Get email template

    Args:
        id (UUID):
        type_ (GetEmailTemplateType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | EmailTemplate]
     """


    kwargs = _get_kwargs(
        id=id,
type_=type_,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    type_: GetEmailTemplateType,
    *,
    client: AuthenticatedClient,

) -> Any | EmailTemplate | None:
    """ Get email template

    Args:
        id (UUID):
        type_ (GetEmailTemplateType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | EmailTemplate
     """


    return sync_detailed(
        id=id,
type_=type_,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    type_: GetEmailTemplateType,
    *,
    client: AuthenticatedClient,

) -> Response[Any | EmailTemplate]:
    """ Get email template

    Args:
        id (UUID):
        type_ (GetEmailTemplateType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | EmailTemplate]
     """


    kwargs = _get_kwargs(
        id=id,
type_=type_,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    type_: GetEmailTemplateType,
    *,
    client: AuthenticatedClient,

) -> Any | EmailTemplate | None:
    """ Get email template

    Args:
        id (UUID):
        type_ (GetEmailTemplateType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | EmailTemplate
     """


    return (await asyncio_detailed(
        id=id,
type_=type_,
client=client,

    )).parsed
