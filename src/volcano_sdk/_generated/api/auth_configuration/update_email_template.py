from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.email_template import EmailTemplate
from ...models.error import Error
from ...models.update_email_template_request import UpdateEmailTemplateRequest
from ...models.update_email_template_type import check_update_email_template_type
from ...models.update_email_template_type import UpdateEmailTemplateType
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    type_: UpdateEmailTemplateType,
    *,
    body: UpdateEmailTemplateRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/projects/{id}/email-templates/{type_}".format(id=quote(str(id), safe=""),type_=quote(str(type_), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | EmailTemplate | Error | None:
    if response.status_code == 200:
        response_200 = EmailTemplate.from_dict(response.json())



        return response_200

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | EmailTemplate | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    type_: UpdateEmailTemplateType,
    *,
    client: AuthenticatedClient,
    body: UpdateEmailTemplateRequest,

) -> Response[Any | EmailTemplate | Error]:
    """ Update email template

     Updates a custom email template. Custom email templates are a PRO-plan
    feature: requests from a FREE-plan project owner are rejected with 403
    (including after a PRO→FREE downgrade), so a FREE project cannot modify
    templates and always sends the built-in defaults.

    Args:
        id (UUID):
        type_ (UpdateEmailTemplateType):
        body (UpdateEmailTemplateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | EmailTemplate | Error]
     """


    kwargs = _get_kwargs(
        id=id,
type_=type_,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    type_: UpdateEmailTemplateType,
    *,
    client: AuthenticatedClient,
    body: UpdateEmailTemplateRequest,

) -> Any | EmailTemplate | Error | None:
    """ Update email template

     Updates a custom email template. Custom email templates are a PRO-plan
    feature: requests from a FREE-plan project owner are rejected with 403
    (including after a PRO→FREE downgrade), so a FREE project cannot modify
    templates and always sends the built-in defaults.

    Args:
        id (UUID):
        type_ (UpdateEmailTemplateType):
        body (UpdateEmailTemplateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | EmailTemplate | Error
     """


    return sync_detailed(
        id=id,
type_=type_,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    type_: UpdateEmailTemplateType,
    *,
    client: AuthenticatedClient,
    body: UpdateEmailTemplateRequest,

) -> Response[Any | EmailTemplate | Error]:
    """ Update email template

     Updates a custom email template. Custom email templates are a PRO-plan
    feature: requests from a FREE-plan project owner are rejected with 403
    (including after a PRO→FREE downgrade), so a FREE project cannot modify
    templates and always sends the built-in defaults.

    Args:
        id (UUID):
        type_ (UpdateEmailTemplateType):
        body (UpdateEmailTemplateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | EmailTemplate | Error]
     """


    kwargs = _get_kwargs(
        id=id,
type_=type_,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    type_: UpdateEmailTemplateType,
    *,
    client: AuthenticatedClient,
    body: UpdateEmailTemplateRequest,

) -> Any | EmailTemplate | Error | None:
    """ Update email template

     Updates a custom email template. Custom email templates are a PRO-plan
    feature: requests from a FREE-plan project owner are rejected with 403
    (including after a PRO→FREE downgrade), so a FREE project cannot modify
    templates and always sends the built-in defaults.

    Args:
        id (UUID):
        type_ (UpdateEmailTemplateType):
        body (UpdateEmailTemplateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | EmailTemplate | Error
     """


    return (await asyncio_detailed(
        id=id,
type_=type_,
client=client,
body=body,

    )).parsed
