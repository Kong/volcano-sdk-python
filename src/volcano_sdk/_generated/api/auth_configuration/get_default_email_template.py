from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.email_template import EmailTemplate
from ...models.get_default_email_template_type import check_get_default_email_template_type
from ...models.get_default_email_template_type import GetDefaultEmailTemplateType
from typing import cast



def _get_kwargs(
    type_: GetDefaultEmailTemplateType,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/email-templates/defaults/{type_}".format(type_=quote(str(type_), safe=""),),
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
    type_: GetDefaultEmailTemplateType,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Any | EmailTemplate]:
    """ Get default email template by type

    Args:
        type_ (GetDefaultEmailTemplateType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | EmailTemplate]
     """


    kwargs = _get_kwargs(
        type_=type_,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    type_: GetDefaultEmailTemplateType,
    *,
    client: AuthenticatedClient | Client,

) -> Any | EmailTemplate | None:
    """ Get default email template by type

    Args:
        type_ (GetDefaultEmailTemplateType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | EmailTemplate
     """


    return sync_detailed(
        type_=type_,
client=client,

    ).parsed

async def asyncio_detailed(
    type_: GetDefaultEmailTemplateType,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Any | EmailTemplate]:
    """ Get default email template by type

    Args:
        type_ (GetDefaultEmailTemplateType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | EmailTemplate]
     """


    kwargs = _get_kwargs(
        type_=type_,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    type_: GetDefaultEmailTemplateType,
    *,
    client: AuthenticatedClient | Client,

) -> Any | EmailTemplate | None:
    """ Get default email template by type

    Args:
        type_ (GetDefaultEmailTemplateType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | EmailTemplate
     """


    return (await asyncio_detailed(
        type_=type_,
client=client,

    )).parsed
